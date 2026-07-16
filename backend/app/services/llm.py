from functools import lru_cache

from groq import Groq

from app.core.config import settings


class LLMConfigError(RuntimeError):
    """Raised when the LLM provider is not configured correctly."""


@lru_cache
def get_client() -> Groq:
    if not settings.groq_api_key:
        raise LLMConfigError(
            "GROQ_API_KEY is not set. Please add it to your .env file."
        )

    return Groq(api_key=settings.groq_api_key)


def generate_answer(prompt: str) -> str:
    client = get_client()

    try:
        response = client.chat.completions.create(
            model=settings.llm_model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0.2,
            max_tokens=512,
        )

        return response.choices[0].message.content.strip()

    except Exception as exc:
        raise LLMConfigError(f"Failed to generate answer: {exc}") from exc