import httpx
from typing import Optional

from app.core.config import settings


class LLMService:
    """
    Service to generate summaries using Llama3/OpenRouter or other LLM backends.
    """

    def __init__(self):
        self.provider = settings.LLM_PROVIDER.lower()
        self.model_name = settings.LLM_MODEL_NAME
        self.api_key = settings.LLM_API_KEY
        self.base_url = settings.LLM_BASE_URL

    async def generate_summary(self, text: str) -> str:
        """
        Generates a summary for the given text.
        """
        if not text:
            return "No content to summarize."

        if self.provider == "openrouter":
            return await self._generate_openrouter(text)
        elif self.provider == "ollama":
            return await self._generate_ollama(text)
        else:
            # Fallback: return first 200 characters
            return text[:200] + "..."

    async def _generate_openrouter(self, text: str) -> str:
        if not self.api_key or not self.base_url:
            raise ValueError("OpenRouter API key or base URL not configured.")

        url = f"{self.base_url}/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": f"Summarize this text:\n{text}"}],
        }

        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

    async def _generate_ollama(self, text: str) -> str:
        """
        Placeholder for Ollama local API integration.
        """
        # Example: return first 250 chars (replace with actual Ollama API call)
        return text[:250] + "..."
