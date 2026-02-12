"""
Test script to verify Gemini API configuration with native SDK
Run this before starting the application to ensure API key is working
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

def test_gemini_native():
    """Test Gemini API connection using native Google SDK"""

    print("=" * 60)
    print("Testing Gemini API Configuration (Native SDK)")
    print("=" * 60)

    # Get configuration
    api_key = os.getenv("OPENAI_API_KEY")
    model_name = os.getenv("MODEL", "gemini-1.5-flash")

    print(f"\n[OK] API Key: {api_key[:20]}..." if api_key else "[ERROR] API Key: Not found")
    print(f"[OK] Model: {model_name}")

    if not api_key:
        print("\n[ERROR] OPENAI_API_KEY not found in .env file")
        return False

    # Test API connection
    print("\n" + "-" * 60)
    print("Testing API Connection...")
    print("-" * 60)

    try:
        # Configure Gemini
        genai.configure(api_key=api_key)

        # Create model
        model = genai.GenerativeModel(model_name)

        # Make a simple test request
        response = model.generate_content(
            "Say 'Hello, Gemini API is working!' in one sentence.",
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=50,
                temperature=0.7,
            )
        )

        result = response.text
        print(f"\n[SUCCESS] API Response:\n{result}")
        print("\n" + "=" * 60)
        print("[SUCCESS] Gemini API is configured correctly!")
        print("=" * 60)
        print("\nYou can now start the backend server:")
        print("  cd backend")
        print("  uvicorn main:app --reload --port 8000")
        return True

    except Exception as e:
        print(f"\n[ERROR] API Error: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        print("\nPossible issues:")
        print("1. Invalid API key")
        print("2. API key doesn't have proper permissions")
        print("3. Network connectivity issues")
        print("4. Model name is incorrect")
        print("\nVerify your API key at: https://aistudio.google.com/app/apikey")
        return False

if __name__ == "__main__":
    success = test_gemini_native()
    exit(0 if success else 1)
