from app.tracks.fitness_track import FitnessTrack

coach = FitnessTrack()

print("Turn 1:")
print(coach.respond("I want to lose 10kg in 3 months."))

print("\nTurn 2:")
print(coach.respond("What should my first week look like?"))

print("\nTurn 3:")
print(coach.respond("What was my original goal again?"))
