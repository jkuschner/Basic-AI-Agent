import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("prompt", type=str, help="Enter a prompt.")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [types.Content(role="user", parts=[types.Part(text=args.prompt)])]

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key == None:
    raise RuntimeError("Failed to get API Key")

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=messages
)

metadata = response.usage_metadata
if metadata == None:
    raise RuntimeError("Failed API Request")


if args.verbose:
    print(f"User prompt: {args.prompt}")
    print(f"Prompt tokens: {metadata.prompt_token_count}")
    print(f"Response tokens: {metadata.candidates_token_count}")

print(f"Response:\n{response.text}")