import typing
import os
import sys
from dotenv import load_dotenv

from google import genai
from google.genai import types

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file


working_directory = 'calculator'


system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Write or overwrite files
- Execute Python files with optional arguments

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""


functions = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}


schemas = {
    "get_files_info": types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                ),
            },
        ),
    ),
    "get_file_content": types.FunctionDeclaration(
        name="get_file_content",
        description="Gets content of file at the specified path, constrained to a working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The file to get the contents of, relative to the working directory.",
                )
            }
        )
    ),
    "write_file": types.FunctionDeclaration(
        name="write_file",
        description="Writes content to file at the specified path, constrained to a working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The file to write the contents to, relative to the working directory.",
                ),
                "contents": types.Schema(
                    type=types.Type.STRING,
                    description="The content to write.",

                )
            }
        )
    ),
    "run_python_file": types.FunctionDeclaration(
        name="run_python_file",
        description="Run Python file at specified path, constrained to a working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The Python file to run, relative to the working directory.",
                ),
                "args": types.Schema(
                    type = types.Type.STRING,
                    description="Arithmetic expression, such as 2 + 2."
                )
            }
        )
    ),
}


available_functions = types.Tool(
    function_declarations=[
        schemas["get_files_info"],
        schemas["get_file_content"],
        schemas["write_file"],
        schemas["run_python_file"],
    ]
)


def parse_args(args: list[str]) -> tuple[str, bool]:
    verbose = False
    for arg in args:
        if arg == "--verbose":
            verbose = True
            args.remove(arg)

    return " ".join(args), verbose


def get_response_from_result(result: types.Content) -> dict[str, typing.Any]:
    if not result.parts or len(result.parts) < 1:
        raise Exception("no results from function call")

    first_response = result.parts[0].function_response
    if not first_response:
        raise Exception("result has no output")

    response = first_response.response
    if not response:
        raise Exception("response is empty")
    return response


def candidates_content(response: types.GenerateContentResponse) -> list[types.Content]:
    content: list[types.Content] = []
    for candidate in response.candidates or []:
        if candidate.content:
            content.append(candidate.content)
    return content


def generate_content(client: genai.Client, messages: list[types.Content], verbose=False):
    should_break = False
    for _ in range(20):
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            )
        )
        messages.extend(candidates_content(response))
        fn_results: list[dict[str, typing.Any]] = []
        if response.function_calls:
            for call in response.function_calls:
                result = call_function(call, verbose)
                messages.append(result)
                fn_results.append(get_response_from_result(result))
            continue
        else:
            print(response.text)
            should_break = True

        if verbose:
            print_details(response, fn_results)

        if should_break:
            break

def print_details(response: types.GenerateContentResponse, fn_results: list[dict[str, typing.Any]]):
    if response.usage_metadata is None:
        print("No response metadata is available. Nothing to print.")
        return
    print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
    print(f'Response tokens: {response.usage_metadata.candidates_token_count}')

    for result in fn_results:
        print(f'-> {result}')


def call_function(function_call_part: types.FunctionCall, verbose: bool = False) -> types.Content:
    function_name = function_call_part.name or ""
    kwargs = function_call_part.args or {}
    if verbose:
        print(f'Calling function {function_name}({kwargs})')

    print(f' - Calling function: {function_name}')
    fn = functions.get(function_name)
    if not fn:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": fn(working_directory, **kwargs)},
            )
        ],
    )


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


if __name__ == "__main__":
    main()
