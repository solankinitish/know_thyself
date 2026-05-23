from app.tracks.fitness_track import FitnessTrack
from app.tracks.habits_track import HabitsTrack
from app.tracks.relationships_track import RelationshipsTrack
from app.utils.logger import get_logger
import pandas as pd
import os


class CoachingService:
    def __init__(self):
        self.logger = get_logger(__name__)
        self.track_map = {
            "fitness": FitnessTrack,
            "habits": HabitsTrack,
            "relationships": RelationshipsTrack
        }
        self.active_coaches = {}
    
    def get_coach(self, user_id, track):
        if not user_id:
            raise ValueError("user_id is blank.")
        if track not in self.track_map:
            raise ValueError("Track not in Track Map.")
        # On first message
        if user_id not in self.active_coaches:
            track_class = self.track_map[track]
            self.active_coaches[user_id] = track_class(user_id=user_id)
        self.logger.info(f"Coach created for {user_id} on {track} track.")
        return self.active_coaches[user_id]

    def chat(self, user_id, track, message):
        if not message or not message.strip():
            raise ValueError("Message cannot be empty.")
        coach = self.get_coach(user_id, track)
        self.logger.info(f"Chat request from {user_id} on {track} track.")
        return coach.respond(message)

    def log_fitness(self, user_id, data):
        if not user_id:
            raise ValueError("user_id is blank.")
        if not data:
            raise ValueError("Data is empty.")
        
        df = pd.DataFrame([data])

        target_dir = os.path.join("data", "fitness")
        os.makedirs(target_dir, exist_ok=True)

        file_path = os.path.join(target_dir, f"{user_id}.csv")


        df.to_csv(file_path, mode="a", index=False, header=not os.path.exists(file_path), lineterminator="\n")
        self.logger.info(f"Data logged for {user_id}.")

    def log_habits(self, user_id, data):
        if not user_id:
            raise ValueError("user_id is blank.")
        if not data:
            raise ValueError("Data is empty.")
        
        df = pd.DataFrame([data])

        target_dir = os.path.join("data", "habits")
        os.makedirs(target_dir, exist_ok=True)

        file_path = os.path.join(target_dir, f"{user_id}.csv")

        df.to_csv(file_path, mode="a", index=False, header=not os.path.exists(file_path), lineterminator="\n")
        self.logger.info(f"Data logged for {user_id}.")
