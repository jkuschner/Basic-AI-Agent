import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

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

for _ in range(20):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0,
            tools=[available_functions])
    )

    if response.candidates:
        for candidate in response.candidates:
            if candidate.content:
                messages.append(candidate.content)

    metadata = response.usage_metadata
    if metadata == None:
        raise RuntimeError("Failed API Request")


    if args.verbose:
        print(f"User prompt: {args.prompt}")
        print(f"Prompt tokens: {metadata.prompt_token_count}")
        print(f"Response tokens: {metadata.candidates_token_count}")

    if response.function_calls:
        function_responses = []

        for function_call in response.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")
            function_call_result = call_function(function_call, verbose=args.verbose)
            if not function_call_result.parts:
                raise Exception(f"problem with calling function: {function_call.name} with args: {function_call.args}")
            if not function_call_result.parts[0].function_response:
                raise Exception(f"Missing function response when calling function: {function_call.name} with args: {function_call.args}")
            if not function_call_result.parts[0].function_response.response:
                raise Exception(f"Missing function response when calling function: {function_call.name} with args: {function_call.args}")
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")

            function_responses.append(function_call_result.parts[0])
        messages.append(types.Content(role="user", parts=function_responses))
    else:
        print(f"Response:\n{response.text}")
        exit(0)

print("Exceeded maximum number of AI conversation iterations")
exit(1)
