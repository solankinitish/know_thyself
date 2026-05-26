import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    def __init__(self):
        self.app_name = os.getenv("APP_NAME", "App")
        self.debug = os.getenv("DEBUG", "False").lower() == "true"
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.memory_api_key = os.getenv("PINECONE_API_KEY")
        self.llm_api_key = os.getenv("GROQ_API_KEY")
        self.llm_provider = os.getenv("LLM_PROVIDER", "groq")
        self.gcs_bucket = os.getenv("GCS_BUCKET", "knowthyself-data")

        self.fitness_n_exchanges = int(os.getenv("FITNESS_N_EXCHANGES", 5))
        self.habits_n_exchanges = int(os.getenv("HABITS_N_EXCHANGES", 3))
        self.relationships_n_exchanges = int(os.getenv("RELATIONSHIPS_N_EXCHANGES", 10))


settings = Settings()
