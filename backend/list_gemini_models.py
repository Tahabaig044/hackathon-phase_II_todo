"""
List available Gemini models for the configured API key
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

def list_available_models():
    """List all available Gemini models"""

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("[ERROR] OPENAI_API_KEY not found in .env file")
        return

    print("=" * 60)
    print("Listing Available Gemini Models")
    print("=" * 60)

    try:
        genai.configure(api_key=api_key)

        print("\nAvailable models:")
        print("-" * 60)

        for model in genai.list_models():
            if 'generateContent' in model.supported_generation_methods:
                print(f"\nModel: {model.name}")
                print(f"  Display Name: {model.display_name}")
                print(f"  Description: {model.description}")
                print(f"  Supported methods: {', '.join(model.supported_generation_methods)}")

        print("\n" + "=" * 60)

    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        print(f"Error type: {type(e).__name__}")

if __name__ == "__main__":
    list_available_models()
