from app.memory.persistent_memory import PersistentMemory

memory = PersistentMemory()

# Store Many memories
memory.store("rahul", "fitness", 2, "session_summary",
             "User completed first week. Squat PR: 60kg. Sleep improved to 7 hours.")

memory.store("rahul", "fitness", 3, "session_summary",
             "User struggling with nutrition. Eating processed food. Weight stalled at 91kg.")

memory.store("rahul", "fitness", 4, "session_summary",
             "User hit new squat PR of 75kg. Energy levels high, sleep consistent at 8 hours.")

memory.store("rahul", "fitness", 5, "session_summary",
             "User increased volume on accessory lifts. Slight knee inflammation reported. Weight: 90.5kg.")

memory.store("rahul", "fitness", 6, "session_summary",
             "Recovery week (deload). Focused on mobility and foam rolling. Inflammation subsided.")

memory.store("rahul", "fitness", 7, "session_summary",
             "Nutrition back on track. Meal prepping initiated. Weight dropped to 89.5kg. Energy stable.")

memory.store("rahul", "fitness", 8, "session_summary",
             "Deadlift PR attempt successful at 100kg. Grip strength identified as a bottleneck.")

memory.store("rahul", "fitness", 9, "session_summary",
             "User prioritized protein intake (180g/day). Body composition changing; waist measurement down.")

memory.store("rahul", "fitness", 10, "session_summary",
             "Squat PR: 85kg. Noted 'grind' on final rep. Sleep dipped to 6 hours due to work stress.")

memory.store("rahul", "fitness", 11, "session_summary",
             "Overtraining symptoms emerged. Resting heart rate elevated. User advised to take two rest days.")

memory.store("rahul", "fitness", 12, "session_summary",
             "Consistency returned. Bench Press PR: 65kg. Sleep restored to 7.5 hours via cool room temp.")

memory.store("rahul", "fitness", 13, "session_summary",
             "User experimented with intermittent fasting. Weight: 88kg. Workouts feel sluggish in AM.")

memory.store("rahul", "fitness", 14, "session_summary",
             "Pivot to intra-workout carbs. Training intensity spiked. Squat form verified as 'excellent'.")

memory.store("rahul", "fitness", 15, "session_summary",
             "New Squat PR: 95kg. User feels 'strongest ever.' Sleep consistent at 8 hours.")

memory.store("rahul", "fitness", 16, "session_summary",
             "Minor setback: Social events led to high sodium intake. Water retention visible. Weight: 89kg.")



# Now retrieve with a specific query
results = memory.retrieve("rahul", "fitness", "What is the trend in my squat PR?", top_k=3)

for match in results:
    print(f"Session: {match.metadata['session_no']}")
    print(f"Score: {match.score}")
    print(f"Content: {match.metadata['content'][:100]}")
    print()
