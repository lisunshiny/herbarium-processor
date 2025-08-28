import base64
import os
from abc import ABC, abstractmethod
from typing import List, Union

import requests
import google.generativeai as genai
from dotenv import load_dotenv
from openai import OpenAI


class BaseLLMAPI(ABC):
    """Simple interface for LLM backends."""

    def __init__(self, system_instructions: str, model_name: str):
        self.system_instructions = system_instructions
        self.model_name = model_name

    @abstractmethod
    def generate_content(self, contents: List[Union[str, dict]]) -> str:
        """Generate text from the given contents."""


class GeminiAPI(BaseLLMAPI):
    """Direct access to Google's Gemini API."""

    def __init__(self, system_instructions: str, model_name: str = "gemini-2.5-pro"):
        super().__init__(system_instructions, model_name)
        load_dotenv()
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel(
            model_name, system_instruction=system_instructions
        )

    def generate_content(self, contents: List[Union[str, dict]]) -> str:
        response = self.model.generate_content(contents=contents)
        return response.candidates[0].content.parts[0].text.strip()


class OpenRouterAPI(BaseLLMAPI):
    """Access LLMs via the OpenRouter aggregation API."""

    BASE_URL = "https://openrouter.ai/api/v1"

    def __init__(
        self,
        system_instructions: str,
        model_name: str = "google/gemini-2.5-pro",
    ):
        super().__init__(system_instructions, model_name)
        load_dotenv()
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY"),
        )

    def _prepare_user_content(self, contents: List[Union[str, dict]]):
        user_content = []
        for idx, part in enumerate(contents):
            if isinstance(part, str):
                print(f"[DEBUG] Text part {idx}: {part}")
                user_content.append({"type": "text", "text": part})
            elif isinstance(part, dict) and "data" in part:
                mime = part.get("mime_type", "image/jpeg")
                b64 = base64.b64encode(part["data"]).decode("utf-8")
                data_url = f"data:{mime};base64,{b64}"
                print(
                    f"[DEBUG] Image part {idx}: mime={mime}, size={len(part['data'])} bytes"
                )
                # Print only the first 80 chars of the base64 string to avoid huge logs
                print(f"[DEBUG] Image data_url prefix: {data_url[:80]}...")

                user_content.append({"type": "image_url", "image_url": data_url})
        return user_content

    def generate_content(self, contents: List[Union[str, dict]]) -> str:
        completion = self.client.chat.completions.create(
            extra_body={},
            model=self.model_name,
            messages=[
                {"role": "system", "content": self.system_instructions},
                {"role": "user", "content": self._prepare_user_content(contents)},
            ],
        )
        return completion.choices[0].message.content
