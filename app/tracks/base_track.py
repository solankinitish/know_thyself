from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from app.llm.llm_client import LLMClient
from app.memory.session_memory import SessionMemory


class BaseTrack:
    def __init__(self, system_prompt):
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{human_message}")
        ])
        self.llm = LLMClient()
        self.memory = SessionMemory()
    
    def respond(self, message: str) -> str:
        messages = self.prompt.format_messages(
            history=self.memory.get_history(),
            human_message=message)
        response = self.llm.generate(messages)
        self.memory.add_interaction(message, response)
        return response
