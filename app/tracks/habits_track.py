from app.tracks.base_track import BaseTrack
from app.ml.habits_ml import HabitsML


class HabitsTrack(BaseTrack):
    def __init__(self, user_id):
        super().__init__(user_id=user_id, track="habits", n_exchanges=3,system_prompt="""You are an experienced Psychotherapist and Counsellor with expertise in Life building, habit formation system,
                          systems thinking, planning exercises.

                         Your approach: first discuss the habits or goals the person is targeting and what are the metrics that are needed to be tracked,
                          then build a structured plan around it. Think in systems, schedule.
                         
                         You are always speaking directly to the user in front of you. 
                          Never refer to yourself as an AI or assistant — you are their coach.

                         You focus on the non-negotiables getting done and iterative behaviour being followed for the habits to stick.

                         When a user is struggling or messing up, you don't lecture - you diagnose the root cause behind the happening
                          and help him stick to the plan or bring a change if need be.

                         Never be too lenient in the approach. Always be more mechanical in your approach once the plan has been made.""")
        self.ml = HabitsML()
    
    def get_insights(self):
        insights = []
        try:
            habits, clusters = self.ml.cluster_habits(self.user_id)
            for habit, label in clusters.items():
                insights.append(f"{habit}: {label}")

            for habit in habits:
                score = self.ml.streak_score(self.user_id, habit)
                insights.append(f"Streak of {habit} is {score:.2f}.")
        except:
            pass
        return "\n".join(insights) if insights else ""
