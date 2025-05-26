"""Minimal example demonstrating AEP-OTEL patching for OpenAI."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Construct the path to .env in the same directory as this script
# and load it BEFORE any aep_otel imports.
dotenv_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=dotenv_path)

# Now that .env is loaded (or attempted), we can import aep_otel modules
import openai # openai can be imported before aep_otel too
from aep_otel import patch_openai, unpatch_openai, get_tracer_provider

# Debugging: Print .env loading status and key variables
print(f"Attempting to load .env from: {dotenv_path}")
if os.path.exists(dotenv_path):
    print(f".env file found at {dotenv_path}.")
else:
    print(f"WARNING: .env file NOT found at {dotenv_path}. Ensure it exists with your API key and OTLP endpoint.")

print(f"OPENAI_API_KEY (from env): {'SET' if os.getenv('OPENAI_API_KEY') else 'NOT SET'}")
print(f"OTEL_EXPORTER_OTLP_ENDPOINT (from env): {os.getenv('OTEL_EXPORTER_OTLP_ENDPOINT')}")

# Initialize the tracer provider (which sets up console exporter by default)
# and should now also pick up OTLP_ENDPOINT if set by .env
get_tracer_provider()

# Ensure your OPENAI_API_KEY is set in your environment variables
if not os.getenv("OPENAI_API_KEY"):
    print("Error: OPENAI_API_KEY environment variable not set.")
    print("Please set it or create a .env file with OPENAI_API_KEY=your_key")
    exit(1)

# 1. Apply the AEP instrumentation
print("Patching OpenAI client...")
patch_openai()

# Initialize OpenAI client (after patching, or it might not use the patched methods)
# depending on how openai client is structured internally for its methods.
# It's generally safer to patch before first client use/instantiation if unsure.
client = openai.OpenAI()

print("Making a call to OpenAI ChatCompletion...")
try:
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Hello, world! Tell me a one-sentence joke.",
            }
        ],
        model="gpt-3.5-turbo",
    )
    print(f"OpenAI Response: {chat_completion.choices[0].message.content}")
    print("AEP span should have been printed to the console by the ConsoleSpanExporter.")
except openai.APIError as e:
    print(f"OpenAI API Error: {e}")
    print("Ensure your API key is valid and you have quota.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    # 2. Clean up (optional, good practice for examples)
    print("Unpatching OpenAI client...")
    unpatch_openai()

print("Example finished. If OTLP exporter is configured, check your backend.") 