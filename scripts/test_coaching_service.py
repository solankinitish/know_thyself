from app.tracks.habits_track import HabitsTrack

coach = HabitsTrack(user_id="rahul")

print("=== Insights ===")
print(coach.get_insights())

print("\n=== Coaching Response ===")
print(coach.respond("How are my habits looking?"))
