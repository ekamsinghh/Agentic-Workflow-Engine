from pydantic import BaseModel, Field
from typing import Any, Callable # type-hints

class WorkflowState(BaseModel):
    run_id: str # idempotency key
    status: str = "initialized"
    # we want the default values of data and history to be empty dictionary and list but we can't simply write data: {} and history:[]
    # setting a default like history: list = [] is dangerous because all instances will share the exact same list in memory
    
    # dict[str, Any] means the keys must be strings, but values can be anything
    data: dict[str, Any] = Field(default_factory=dict)# field default_factory guarantees that each instance of the class will have its own separate dictionary or list whatsoever
    history : list[str] = Field(default_factory=list)

# Node class is not need to be written using pydantic cause we don't want to serialize it(meaning converting the object into text like json)
# WorkflowSate contains raw data and at some point it will be needed to save in database whereas as Node contains a python function which we don't want to be serialized
class Node:
    def __init__(self, name: str, operation: Callable[[WorkflowState],WorkflowState]):
        self.name = name
        self.operation = operation