import os


MAX_CHARS = 10000


def get_file_content(working_directory: str, file_path: str) -> str:
    wd_path = os.path.abspath(working_directory)
    path = os.path.abspath(os.path.join(wd_path, file_path))

    if not path.startswith(wd_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    contents: str = ""
    try:
        with open(path, "r") as file:
            contents = file.read(MAX_CHARS)

        if os.path.getsize(path) > MAX_CHARS:
            return f'{contents}[...File "{file_path}" truncated at {MAX_CHARS} characters]'
    except Exception as e:
        return f'Error: error reading contents of "{file_path}": {e}'

    return contents
