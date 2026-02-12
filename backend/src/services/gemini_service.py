"""
Gemini AI Service Adapter
Provides Google Gemini API integration with OpenAI-compatible interface
"""
import os
import json
import time
from typing import List, Dict, Any, Optional
import google.generativeai as genai
from dotenv import load_dotenv

from ..core.errors import AIServiceError
from ..core.logging import chat_logger

load_dotenv()


class GeminiService:
    """Service for Google Gemini AI integration"""

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY (Gemini API key) not found in environment")

        genai.configure(api_key=api_key)

        model_name = os.getenv("MODEL", "gemini-1.5-flash")
        self.model = genai.GenerativeModel(model_name)
        self.max_tokens = int(os.getenv("MAX_TOKENS", "1000"))
        self.temperature = float(os.getenv("TEMPERATURE", "0.7"))
        self.timeout = int(os.getenv("AI_TIMEOUT", "30"))

    def get_system_prompt(self) -> str:
        """Get the system prompt for the AI agent"""
        return """You are a helpful AI assistant for a todo list application.
You help users manage their tasks through natural language commands.

You can:
- Add new tasks
- Complete tasks
- List tasks
- Update task details
- Delete tasks
- Support both English and Roman Urdu inputs

When users ask you to do something with their tasks, use the available tools to execute the operations.
Be conversational, friendly, and helpful. Confirm actions and provide clear feedback."""

    def _convert_messages_to_gemini_format(
        self,
        messages: List[Dict[str, str]]
    ) -> tuple[str, List[Dict[str, str]]]:
        """
        Convert OpenAI-style messages to Gemini format
        Returns: (system_prompt, conversation_history)
        """
        system_prompt = self.get_system_prompt()
        history = []

        for msg in messages:
            role = msg.get("role")
            content = msg.get("content", "")

            if role == "system":
                system_prompt = content
            elif role == "user":
                history.append({"role": "user", "parts": [content]})
            elif role == "assistant":
                history.append({"role": "model", "parts": [content]})

        return system_prompt, history

    def _parse_tool_calls_from_response(self, response_text: str) -> List[Dict[str, Any]]:
        """
        Parse tool calls from Gemini response
        Gemini doesn't have native tool calling like OpenAI, so we need to parse from text
        """
        # For now, return empty list - tool calling would need custom implementation
        # This is a simplified version without tool support
        return []

    async def process_message(
        self,
        user_message: str,
        conversation_history: List[Dict[str, str]],
        user_id: str,
        db_session=None,
    ) -> Dict[str, Any]:
        """
        Process user message and generate AI response using Gemini.

        Args:
            user_message: The user's message
            conversation_history: Previous conversation messages
            user_id: The user ID for tool execution context
            db_session: Async database session for tool operations

        Returns:
            Dictionary with response and tool calls
        """
        start_time = time.time()

        try:
            # Convert messages to Gemini format
            system_prompt, history = self._convert_messages_to_gemini_format(
                conversation_history
            )

            # Start chat with history
            chat = self.model.start_chat(history=history)

            # Prepare the full prompt with system instructions
            full_prompt = f"{system_prompt}\n\nUser: {user_message}"

            # Generate response
            response = chat.send_message(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=self.max_tokens,
                    temperature=self.temperature,
                )
            )

            response_text = response.text
            tool_calls = []  # Gemini doesn't support tool calling in the same way

            # Calculate response time
            response_time = time.time() - start_time

            # Log performance
            chat_logger.log_performance(
                "ai_message_processing",
                response_time,
                {"user_id": user_id, "tool_calls": len(tool_calls)}
            )

            return {
                "response": response_text,
                "tool_calls": tool_calls,
                "response_time": response_time
            }

        except Exception as e:
            chat_logger.log_error("gemini_api_error", str(e), {"user_id": user_id})
            raise AIServiceError(f"Gemini API error: {str(e)}")

    def detect_language(self, text: str) -> str:
        """Detect if the input is English or Roman Urdu"""
        urdu_keywords = ["karo", "karna", "hai", "ka", "ko", "ke", "se", "mein", "aur"]
        text_lower = text.lower()
        urdu_count = sum(1 for word in urdu_keywords if word in text_lower)
        return "urdu" if urdu_count > 0 else "english"
