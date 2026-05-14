import os
import numpy as np
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone

load_dotenv()


class PersistentMemory:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.api_key = os.getenv("PINECONE_API_KEY")
        pc = Pinecone(api_key=self.api_key)
        self.index = pc.Index("knowthyself")
    
    def store(self, user_id, track, session_no, memory_type, content):
        unique_id = f"{user_id}_{track}_{session_no}_{memory_type}"
        embeddings = self.model.encode(content).tolist()
        metadata = {
            "user_id": user_id,
            "track": track,
            "session_no": session_no,
            "memory_type": memory_type,
            "content": content
        }
        self.index.upsert(
            vectors=[
                ({"id": unique_id, "values": embeddings, "metadata": metadata})
            ]
        )

    def retrieve(self, user_id, track, query, top_k=3):
        embeddings = self.model.encode(query).tolist()

        results = self.index.query(
            vector=embeddings,
            top_k=top_k,
            include_metadata=True,
            filter={
                "user_id": {"$eq": user_id},
                "track": {"$eq": track}                
            }
        )
        return results

    def get_session_history(self, user_id, track):
        vector = np.zeros(384).tolist()
        results = self.index.query(
            vector=vector,
            top_k=100,
            include_metadata=True,
            filter={
                "user_id": {"$eq": user_id},
                "track": {"$eq": track}
            }
        )
        return results
