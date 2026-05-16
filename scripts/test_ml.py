from app.ml.fitness_ml import FitnessML

ml = FitnessML()

print("=== Progress Analysis ===")
print(ml.analyze_progress("rahul", "squat"))

print("\n=== Anomaly Detection ===")
print(ml.detect_anomalies("rahul", "body_weight"))
print(ml.detect_anomalies("rahul", "sleep_hours"))
