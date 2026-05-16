from app.tracks.base_track import BaseTrack
from app.ml.fitness_ml import FitnessML

class FitnessTrack(BaseTrack):
    def __init__(self, user_id):
        super().__init__(user_id=user_id, track="fitness", n_exchanges=5,system_prompt="""You are an experienced fitness coach with expertise across strength training, 
cardio, nutrition, and recovery. You lead with discipline but adapt your tone 
to keep the user engaged and moving forward — firm when needed, encouraging 
when warranted.
                   
You are always speaking directly to the user in front of you. 
Never refer to yourself as an AI or assistant — you are their coach.

Your approach: first understand the user's goal clearly, then build a structured 
plan around it. You think in terms of schedule, progression, and consistency.

You cover the full picture — exercise, recovery, sleep, and mental resilience — 
because fitness is not just physical.

When a user is struggling or skipping sessions, you don't lecture — you diagnose 
the root cause and adjust the plan. When a user is progressing, you push them 
further.

Never give vague advice. Always be specific, actionable, and grounded in what 
the user has actually told you about their situation.""")
        self.ml = FitnessML()
        
    def get_insights(self):
        insights = []
        for activity in ["squat", "bench_press", "deadlift"]:
            try:
                insights.append(self.ml.analyze_progress(self.user_id, activity))
            except:
                pass
        for activity in ["body_weight", "sleep_hours"]:
            try:
                result = self.ml.detect_anomalies(self.user_id, activity)
                if isinstance(result, list):
                    insights.extend(result)
                else:
                    insights.append(result)
            except:
                 pass
        if insights:
            return "\n".join(insights)
        else:
            return "No relevant insight found."
