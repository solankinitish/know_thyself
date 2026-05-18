from sklearn.cluster import KMeans
import pandas as pd
import numpy as np


class HabitsML:
    def __init__(self):
        self.model = KMeans(n_clusters=3)

    def cluster_habits(self, user_id):
        df = pd.read_csv(f"data/habits/{user_id}.csv", skipinitialspace=True)

        habits = df["habit"].unique()

        feature_list = []
        for habit in habits:
            df_habit = df[df["habit"] == habit].copy()
            c_rate = np.sum(df_habit["completed"]) / len(df_habit)
            avg_score = np.mean(df_habit["score"])
            feature_list.append([c_rate, avg_score])
        self.model.fit(feature_list)
        labels = self.model.labels_

        # compute mean completion rate per cluster
        cluster_rates = {}
        for i, habit in enumerate(habits):
            cluster = labels[i]
            if cluster not in cluster_rates:
                cluster_rates[cluster] = []
            cluster_rates[cluster].append(feature_list[i][0])
        
        cluster_means = {c: np.mean(rates) for c, rates in cluster_rates.items()}
        sorted_clusters = sorted(cluster_means, key=cluster_means.get)

        label_map = {
            sorted_clusters[0]: "low consistency",
            sorted_clusters[1]: "medium consistency",
            sorted_clusters[2]: "high consistency"
        }
        
        # map each habit to its cluster label
        result = {habit: label_map[label] for habit, label in zip(habits, labels)}
        return habits, result

    def streak_score(self, user_id, habit):
        df = pd.read_csv(f"data/habits/{user_id}.csv", skipinitialspace=True)
        
        df_habit = df[df["habit"] == habit].copy()
        df_habit["date"] = pd.to_datetime(df_habit["date"])
        today = pd.Timestamp.today()
        df_habit['days_ago'] = (today - df_habit["date"]).dt.days

        min_days = df_habit["days_ago"].min()
        df_habit["days_ago_normalized"] = df_habit["days_ago"] - min_days
        
        score = np.sum(df_habit["completed"] * np.exp(-0.1 * df_habit["days_ago_normalized"]))
        return score
