import os
import sys
from dotenv import load_dotenv

from google import genai
from google.genai import types


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    args = sys.argv[1:]
    if len(args) < 1:
        print("No prompt provided!")
        sys.exit(1)

    user_prompt, verbose = parse_args(args)
    if verbose:
        print(f"User prompt: {user_prompt}")
    client = genai.Client(api_key=api_key)
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]
    generate_content(client, messages, verbose)


def parse_args(args: list[str]) -> tuple[str, bool]:
    verbose = False
    for arg in args:
        if arg == "--verbose":
            verbose = True
            args.remove(arg)

    return " ".join(args), verbose


def generate_content(client: genai.Client, messages: list[types.Content], verbose=False):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages
    )

    print(response.text)
    if verbose:
        print_details(response)


def print_details(response: types.GenerateContentResponse):
    if response.usage_metadata is None:
        print("No response metadata is available. Nothing to print.")
        return
    print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
    print(f'Response tokens: {response.usage_metadata.candidates_token_count}')


if __name__ == "__main__":
    main()
