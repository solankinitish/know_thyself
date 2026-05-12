from app.tracks.fitness_track import FitnessTrack
from app.tracks.habits_track import HabitTrack
from app.tracks.relationships_track import RelationshipTrack


fitness = FitnessTrack()
habit = HabitTrack()
relationship = RelationshipTrack()

print("=== FITNESS ===")
print(fitness.respond("I want to lose 10kg in 3 months, where do I start?"))

print("=== HABITS ===")
print(habit.respond("I keep starting habits but never stick to them past 2 weeks."))

print("=== RELATIONSHIPS ===")
print(relationship.respond("I feel distant from my partner but don't know how to bring it up."))
