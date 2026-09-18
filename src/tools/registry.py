import inspect
from typing import Any, Callable

# Mapping python data types to the json schema's
TYPE_MAP = {
    str: "string",
    int: "integer",
    float: "number",
    bool: "boolean",
    list: "array",
    dict: "object",
}

# Function to convert a python function to a json schema
def function_to_schema(func: Callable) -> dict:
    # using python'b built in module to extract the function signature and parameters
    sig = inspect.signature(func)
    properties = {}
    required = [] # non-default arguments

    for param_name, param in sig.parameters.items():

        # Setting default type to string if no matching key is found
        param_type = TYPE_MAP.get(param.annotation, "string")
        properties[param_name] = {"type": param_type}

        # If the parameter has no default value, it's required
        if param.default == inspect.Parameter.empty:
            required.append(param_name)

    return {
        "type": "function",
        "function": {
        "name": func.__name__,
        "description": func.__doc__ or "No description provided.",
        "parameters": {
            "type": "object",
            "properties": properties,
            "required": required,
        },
        },
    }

class ToolRegistry:

  def __init__(self):

    # Function name mapped to actual callable
    self._tools: dict[str, Callable] = {}
    # list of the schemas created
    self._schemas: list[dict] = []

  def register(self, func: Callable) -> Callable:
    name = func.__name__
    if name in self._tools:
      raise ValueError(f"Tool with name '{name}' is already registered.")

    self._tools[name] = func
    self._schemas.append(function_to_schema(func))
    return func

  def tool(self) -> Callable:
    """Decorator syntax: @registry.tool()"""

    def decorator(func: Callable) -> Callable:
      return self.register(func)

    return decorator

  def get_schemas(self) -> list[dict]:
    return self._schemas

  def execute(self, name: str, **kwargs) -> Any:
    if name not in self._tools:
      return {
        "status": "error",
        "error": f"Tool '{name}' not found in registry.",
      }

    try:
      # Sandboxed execution: call the target function
      result = self._tools[name](**kwargs)
      return {"status": "success", "result": result}
    except TypeError as e:
      # Common when LLM passes wrong argument names/counts
      return {
        "status": "error",
        "error": f"Invalid arguments for tool '{name}': {e}",
      }
    except Exception as e:
      # Catches any internal tool runtime exception
      return {
        "status": "error",
        "error": f"Tool '{name}' failed with error: {e}",
      }


# Global default instance
registry = ToolRegistry()