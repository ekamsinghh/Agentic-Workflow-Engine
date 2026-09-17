import os

from dotenv import load_dotenv
from groq import Groq
from .config import MODEL
from typing import Type, TypeVar
from pydantic import BaseModel

load_dotenv()

# T stands for "any subclass of BaseModel"
T = TypeVar("T", bound=BaseModel)

class LLM:
    def __init__(self): # Create one client object and reuse it for all API requests
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError(
                "GROQ_API_KEY not found in environment variables. "
                "Ensure you have a .env file containing GROQ_API_KEY = gsk_..."
            )
        self.client = Groq(
            api_key = api_key
        ) # python object to communicate with the groq api

    def generate_text(self, prompt: str, model: str = MODEL.DEFAULT, max_tokens: int = 1000) -> str:
        response_string = ""
        try:
            res = self.client.chat.completions.create(
                messages = [
                    {
                        "role" : "user",
                        "content" : prompt
                    }
                ],
                model = model,
                max_tokens = max_tokens
            )
            # Extracting the response message
            response_string = res.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"Groq API call failed: {e}") from e #error chaining to the original exception

        return response_string

    def generate_structured_output(self, prompt: str, response_model: Type[T], model: str = MODEL.DEFAULT, system_prompt: str | None = None) -> T: #Whatever specific class blueprint you pass in as response_model, that exact same class type will come out of this function
        messages = []
        if( system_prompt ):
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        # adding user's prompt
        messages.append({
            "role": "user",
            "content" : prompt
        })
        schema = response_model.model_json_schema()

        # Enforce strict mode requirement for Groq's constrained decoder
        schema["additionalProperties"] = False
        try:
            res = self.client.chat.completions.create(
                model=model,
                messages=messages,
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": response_model.__name__,
                        "strict": True,
                        "schema": schema,
                    },
                },
            )
            raw_json = res.choices[0].message.content
            return response_model.model_validate_json(raw_json)
        
        except Exception as e:
            raise RuntimeError(f"Failed to generate structured output: {e}") from e
