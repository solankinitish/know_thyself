from langchain_core.prompts import ChatPromptTemplate
from app.llm.llm_client import LLMClient


class BaseTrack:
    def __init__(self, system_prompt):
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{human_message}")
        ])
        self.llm = LLMClient()
    
    def respond(self, message: str) -> str:
        messages = self.prompt.format_messages(human_message=message)
        response = self.llm.generate(messages)
        return response
