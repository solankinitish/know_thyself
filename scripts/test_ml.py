from app.memory.persistent_memory import PersistentMemory
from app.tracks.relationships_track import RelationshipsTrack

# Store test relationship memories
memory = PersistentMemory()

memory.store("rahul", "relationships", 1, "session_summary",
             "Issues: Partner feels neglected due to work commitments. Progress: User acknowledged the issue. Mood: User felt guilty but willing to change.")

memory.store("rahul", "relationships", 2, "session_summary",
             "Issues: Communication breakdown during arguments. Progress: User trying active listening. Mood: User felt hopeful but frustrated at times.")

# Test coaching response
coach = RelationshipsTrack(user_id="rahul")
print("=== Insights ===")
print(coach.get_insights())

print("\n=== Coaching Response ===")
print(coach.respond("We had another big argument last night about the same things."))
