"""
AI Service Factory
Provides the appropriate AI service based on configuration
"""
import os
from typing import Union
from dotenv import load_dotenv

from .ai_agent_service import AIAgentService
from .gemini_service import GeminiService

load_dotenv()


def get_ai_service() -> Union[AIAgentService, GeminiService]:
    """
    Factory function to get the appropriate AI service based on configuration

    Returns:
        AIAgentService for OpenAI/OpenRouter
        GeminiService for Google Gemini
    """
    provider = os.getenv("AI_PROVIDER", "gemini").lower()

    if provider == "gemini":
        return GeminiService()
    elif provider in ["openai", "openrouter"]:
        return AIAgentService()
    else:
        # Default to Gemini
        return GeminiService()
