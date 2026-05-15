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
        if not self.api_key:
            raise ValueError("PINECONE_API_KEY not found in environment variables")
        pc = Pinecone(api_key=self.api_key)
        self.index = pc.Index("knowthyself")
    
    def store(self, user_id, track, session_no, memory_type, content):
        if not content or not content.strip():
            return
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
            top_k=top_k * 2,
            include_metadata=True,
            filter={
                "user_id": {"$eq": user_id},
                "track": {"$eq": track}                
            }
        )
        if not results.matches:
            return []
        max_session = max(match.metadata["session_no"] for match in results.matches)
        scored_matches = []
        for i, match in enumerate(results.matches):
            final_score = match.score + (match.metadata["session_no"] / max_session) * 0.1
            if final_score >= 0.4:
                scored_matches.append((final_score, match))
        
        sorted_matches = sorted(scored_matches, key=lambda x: x[0], reverse=True)
        top_matches = [match for score, match in sorted_matches[:top_k]]

        return top_matches

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
