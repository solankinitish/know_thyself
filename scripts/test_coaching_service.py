from app.tracks.fitness_track import FitnessTrack

coach = FitnessTrack(user_id="rahul")

# 5 exchanges to trigger summarization
responses= [
    "I want to lose 10 kg in 3 months.",
    "My current weight is 92kg.",
    "I can go to the gym 4 days a week.",
    "I've been struggling with sleep lately.",
    "What should my first week look life?"
]

for i, message in enumerate(responses):
    print(f"\nExchange {i+1}:")
    print(f"User: {message}")
    print(f"Coach: {coach.respond(message)[:200]}...")

print("\nCheck Pinecone for stored summary.")

# Session 2 - new instance simulates new session
coach = FitnessTrack(user_id="rahul")

print("Session 2, Exchange 1:")
print(coach.respond("What were my goals from last time?"))
