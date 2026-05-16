import pandas as pd


class CSVIngestor:

    def save_file(self, user_id, track, file_path):
        df = pd.read_csv(f"{file_path}")
        if all(col in df.columns for col in ["date", "body_weight", "exercise", "weight_kg"]):
            df.to_csv(f"data/{track}/{user_id}.csv")
            return "Done"
        else:
            return "Error: Required columns not present."
