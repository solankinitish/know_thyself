from app.tracks.fitness_track import FitnessTrack

coach = FitnessTrack(user_id="rahul")

print("Insights being rejected:")
print(coach.get_insights())

print("\n=== Coaching Response ===")
print(coach.respond("How is my training progressing?"))
