import src.wrapper.llm as llm
from src.wrapper.config import MODEL

llm_client = llm.LLM()  # Create an instance of the LLM class
result = llm_client.generate_text("Explain what is an agentic workflow engine in not more than two sentences",MODEL.ROUTING_FAST)
print(result)