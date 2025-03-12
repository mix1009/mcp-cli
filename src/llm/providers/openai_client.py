# src/llm/providers/openai_client.py
import os
import logging
from typing import Any, Dict, List
from dotenv import load_dotenv

# openai
from openai import OpenAI

# llm imports
from llm.providers.base import BaseLLMClient

# Load environment variables
load_dotenv()

class OpenAILLMClient(BaseLLMClient):
    def __init__(self, model="gpt-4o-mini", api_key=None):
        # set the model
        self.model = model

        # set the api key
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.api_url = os.getenv("OPENAI_API_URL") or "https://api.openai.com/v1"

        # check for an api key
        if not self.api_key:
            raise ValueError("The OPENAI_API_KEY environment variable is not set.")
        
        # set the client as open ai
        self.client = OpenAI(api_key=self.api_key, base_url=self.api_url)

    def create_completion(self, messages: List[Dict], tools: List = None) -> Dict[str, Any]:
        try:
            # perform the completion
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools or [],
            )

            # return the response
            return {
                "response": response.choices[0].message.content,
                "tool_calls": getattr(response.choices[0].message, "tool_calls", []),
            }
        except Exception as e:
            # error
            logging.error(f"OpenAI API Error: {str(e)}")
            raise ValueError(f"OpenAI API Error: {str(e)}")
