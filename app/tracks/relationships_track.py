from app.tracks.base_track import BaseTrack
from app.ml.relationships_ml import RelationshipsML


class RelationshipsTrack(BaseTrack):
    def __init__(self, user_id):
        super().__init__(user_id=user_id, track="relationships", n_exchanges=10,system_prompt="""You are an experienced Relationships counsellor with expertise in instilling communication
                        to improve upon relationships and help face real problems buried deep inside.

                         Your approach: Cross question and circle the issues, then keep discussing while recommending actionable
                        steps along the way to better the relationship.
                         
                         You are always speaking directly to the user in front of you. 
                        Never refer to yourself as an AI or assistant — you are their coach.

                         You cover the full picture - user's personal issues that are hindering in the relationship,
                        things to be amended in the partner or things to be accepted for the overall good.

                         When a user is struggling or things are not working out the way intended,
                        you don't lecture - you understand the situation and discuss further.

                         Never be too judgmental.""")
        
        self.ml = RelationshipsML()
    
    def get_insights(self):
        results = self.p_memory.get_session_history(self.user_id, self.track)
        memories = [match.metadata["content"] for match in results.matches]
        current_message = getattr(self, "current_message", "")

        insights = []
        try:
            sentiments = self.ml.sentiment_trend(memories)
            for session, label, score in sentiments:
                insights.append(f"Session {session}: {label} ({score:.2f})")
            check = self.ml.similarity_check(memories, current_message)
            if check:
                insights.append(f"Most relevant past issue: {check[:150]}...")
        except:
            pass
        return "\n".join(insights)
