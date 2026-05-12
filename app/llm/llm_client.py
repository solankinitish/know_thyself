from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate


class LLMClient:
    def __init__(self):
        self.llm = ChatOllama(model="mistral")
        self.prompt = ChatPromptTemplate.from_messages([
                        ("system", "You are a smart expert of the field about which the question is being asked, act accordingly."),
                        ("human", "{user_message}")
                    ])
        self.chain = self.prompt | self.llm
    
    def chat(self, message: str) -> str:
        response = self.chain.invoke({"user_message": message})
        return response.content
    
    def generate(self, messages: list) -> str:
        response = self.llm.invoke(messages)
        return response.content
