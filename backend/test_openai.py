import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Check if API key exists
api_key = os.getenv("OPENAI_API_KEY")
print(f"API Key exists: {bool(api_key)}")
print(f"API Key preview: {api_key[:10] if api_key else 'None'}...")

# Test client initialization with explicit key
try:
    client = OpenAI(api_key=api_key)
    print("Client created successfully")

    # Test if we can list models
    models = client.models.list()
    print(f"Successfully connected to OpenAI API. Found {len(models.data)} models")

    # Check if gpt-4o-mini is available
    gpt4o_mini_available = any(model.id == "gpt-4o-mini" for model in models.data)
    print(f"gpt-4o-mini available: {gpt4o_mini_available}")

except Exception as e:
    print(f"Error connecting to OpenAI API: {e}")