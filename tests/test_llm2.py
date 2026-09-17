from pydantic import BaseModel, Field
from src.wrapper.config import MODEL
import src.wrapper.llm as llm


# 1. Define our structured blueprint
class RouterDecision(BaseModel):
  next_node: str = Field(
      description="The name of the next node to route execution to"
  )
  reasoning: str = Field(
      description="Brief explanation of why this node was selected"
  )
  confidence: float = Field(
      description="Confidence score between 0.0 and 1.0"
  )


# 2. Instantiate LLM
llm_client = llm.LLM()

# 3. Define prompts
system_instruction = (
    "You are an orchestration router for an e-commerce workflow. "
    "Select the most appropriate next node from: ['process_refund', 'track_package', 'human_support']."
)
user_query = "My package #54321 never showed up and tracking hasn't updated in 2 weeks. I want someone to look into it."

# 4. Call structured output
decision = llm_client.generate_structured_output(
    prompt=user_query,
    response_model=RouterDecision,
    system_prompt=system_instruction,
    model=MODEL.ROUTING_FAST,
)

# 5. Inspect the output
print("Parsed Object Type:", type(decision))
print("Next Node:", decision.next_node)
print("Reasoning:", decision.reasoning)
print("Confidence:", decision.confidence)