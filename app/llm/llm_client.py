from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from app.utils.logger import get_logger
from app.utils.config import settings


class LLMClient:
    def __init__(self):
        self.logger = get_logger(__name__)
        self.llm = ChatOllama(model="mistral")
        self.prompt = ChatPromptTemplate.from_messages([
                        ("system", "You are a smart expert of the field about which the question is being asked, act accordingly."),
                        ("human", "{user_message}")
                    ])
        self.chain = self.prompt | self.llm
        self.groq = ChatGroq(
            api_key=settings.llm_api_key,
            model="llama-3.1-8b-instant"
        )
    
    def chat(self, message: str) -> str:
        response = self.chain.invoke({"user_message": message})
        return response.content
    
    def generate(self, messages: list) -> str:
        try:
            response = self.groq.invoke(messages)
            self.logger.info("Response from Groq.")
            # Token tracking
            usage = response.response_metadata.get("token_usage", {})
            self.logger.info(f"Tokens - Input: {usage.get('prompt_tokens', 0)}, Output: {usage.get('completion_tokens', 0)}")
            return response.content
        except Exception as e:
            self.logger.info(f"Groq failed: {e}, falling back to Ollama.")
            response = self.llm.invoke(messages)
        return response.content
