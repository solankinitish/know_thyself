import warnings
from langchain._api import LangChainDeprecationWarning
warnings.filterwarnings("ignore", category=LangChainDeprecationWarning)
from langchain.memory import ConversationSummaryBufferMemory
from langchain_groq import ChatGroq
from app.utils.config import settings


class SessionMemory:
    def __init__(self, max_token_limit=1000):
        self.llm = ChatGroq(
            api_key=settings.llm_api_key,
            model="llama-3.1-8b-instant"
        )
        self.memory = ConversationSummaryBufferMemory(
            llm=self.llm,
            max_token_limit=max_token_limit,
            return_messages=True
        )
            
    def get_history(self):
        history = self.memory.load_memory_variables({})
        return history['history']

    def add_interaction(self, human_message, ai_response):
        self.memory.save_context({"input": human_message}, {"output": ai_response})

    def clear(self):
        self.memory.clear()
