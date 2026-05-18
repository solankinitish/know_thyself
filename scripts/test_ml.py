from app.ml.habits_ml import HabitsML

ml = HabitsML()

print("=== Cluster Habits ===")
print(ml.cluster_habits("rahul"))

print("\n=== Streak Scores ===")
for habit in ["gym", "reading", "medication", "hydration"]:
    print(f"{habit}: {ml.streak_score('rahul', habit):.3f}")
