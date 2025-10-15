from abc import ABC, abstractmethod
import base64
import os
from typing import List, Union

from dotenv import load_dotenv
from openai import AsyncOpenAI


class BaseLLMAPI(ABC):
    """Simple interface for LLM backends."""

    def __init__(self, system_instructions: str, model_name: str):
        self.system_instructions = system_instructions
        self.model_name = model_name

    @abstractmethod
    async def generate_content(self, contents: List[Union[str, dict]]) -> str:
        """Generate text from the given contents."""


class OpenRouterAPI(BaseLLMAPI):
    """Access LLMs via the OpenRouter aggregation API."""

    def __init__(
        self,
        system_instructions: str,
        model_name: str = "google/gemini-2.5-pro",
    ):
        super().__init__(system_instructions, model_name)
        load_dotenv()
        # Async client with HTTP/2 and connection reuse under the hood
        self.client = AsyncOpenAI(
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

    async def generate_content(self, contents: List[Union[str, dict]]) -> str:
        """
        Async text+image generation. Returns the model's text string.
        """
        resp = await self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": self.system_instructions},
                {"role": "user", "content": self._prepare_user_content(contents)},
            ],
        )
        # Defensive: sometimes content can be None; normalize to ""
        return resp.choices[0].message.content or ""
