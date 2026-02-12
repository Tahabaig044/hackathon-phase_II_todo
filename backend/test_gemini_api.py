"""
Test script to verify Gemini API configuration
Run this before starting the application to ensure API key is working
"""
import os
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

def test_gemini_api():
    """Test Gemini API connection and configuration"""

    print("=" * 60)
    print("Testing Gemini API Configuration")
    print("=" * 60)

    # Get configuration
    base_url = os.getenv("OPENAI_BASE_URL")
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("MODEL")

    print(f"\n[OK] Base URL: {base_url}")
    print(f"[OK] API Key: {api_key[:20]}..." if api_key else "[ERROR] API Key: Not found")
    print(f"[OK] Model: {model}")

    if not api_key:
        print("\n[ERROR] OPENAI_API_KEY not found in .env file")
        return False

    # Test API connection
    print("\n" + "-" * 60)
    print("Testing API Connection...")
    print("-" * 60)

    try:
        client = openai.OpenAI(
            base_url=base_url,
            api_key=api_key,
        )

        # Make a simple test request
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": "Say 'Hello, API is working!' in one sentence."}
            ],
            max_tokens=50,
            temperature=0.7
        )

        result = response.choices[0].message.content
        print(f"\n[SUCCESS] API Response:\n{result}")
        print("\n" + "=" * 60)
        print("[SUCCESS] Gemini API is configured correctly!")
        print("=" * 60)
        return True

    except openai.APIError as e:
        print(f"\n[ERROR] API Error: {str(e)}")
        print("\nPossible issues:")
        print("1. Invalid API key")
        print("2. API key doesn't have proper permissions")
        print("3. Network connectivity issues")
        return False

    except Exception as e:
        print(f"\n[ERROR] Unexpected Error: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        return False

if __name__ == "__main__":
    success = test_gemini_api()
    exit(0 if success else 1)
