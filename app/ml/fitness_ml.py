import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from scipy import stats
from app.utils.config import settings


class FitnessML:
    def __init__(self):
        self.model = LinearRegression()

    def analyze_progress(self, user_id, exercise):
        df = pd.read_csv(f"gs://{settings.gcs_bucket}/fitness/{user_id}.csv", skipinitialspace=True, on_bad_lines='skip')
        df_exercise = df[df['exercise'] == exercise].reset_index(drop=True)
        X = np.array(range(len(df_exercise))).reshape(-1, 1)
        y = df_exercise["weight_kg"].values
        self.model.fit(X, y)
        slope = self.model.coef_
        return f"The trend of {exercise} weight is increasing at {slope[0]:.2f} kg per session."

    def detect_anomalies(self, user_id, column):
        df = pd.read_csv(f"gs://{settings.gcs_bucket}/fitness/{user_id}.csv", skipinitialspace=True, on_bad_lines='skip')
        z_scores = stats.zscore(df[column])

        anomalies = []
        for i, score in enumerate(z_scores):
            if abs(score) > 2:
                anomalies.append(f"Row {i}: {df[column].iloc[i]} is anomalous (Z={score:.2f})")
        return anomalies if anomalies else "No anomalies detected."
