from transformers import pipeline
from sentence_transformers import SentenceTransformer
import numpy as np


class RelationshipsML:
    def __init__(self):
        self.sentiment = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
    
    def sentiment_trend(self, memories: list) -> str:
        sentiments = []
        for i, memory in enumerate(memories):
            mood = memory.split("Mood:")[-1].strip()
            sentiment = self.sentiment(mood)
            label = sentiment[0]["label"]
            score = sentiment[0]["score"]
            sentiments.append((i+1, label, score))
        return sentiments

    def similarity_check(self, memories: list, current_message: str) -> str:
        curr = self.model.encode(current_message)

        similarities = []
        for i, memory in enumerate(memories):
            instance = self.model.encode(memory)
            
            # Cosine similarity
            dot = np.dot(curr, instance)
            norm_a = np.linalg.norm(curr)
            norm_b = np.linalg.norm(instance)
            cos_sim = dot / (norm_a * norm_b)
            similarities.append((i, cos_sim))
        best_idx, best_score =  max(similarities, key=lambda x: x[1])
        return memories[best_idx]
