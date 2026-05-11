from app.llm.llm_client import LLMClient

client = LLMClient()
response = client.chat("What is the best way to build a habit?")
print(response)
