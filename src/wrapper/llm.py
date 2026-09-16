import os

from dotenv import load_dotenv
from groq import Groq
from .config import MODEL

load_dotenv()

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