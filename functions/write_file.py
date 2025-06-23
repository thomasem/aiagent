import os

from safety.working_directory import resolved_paths, within_working_directory


def write_file(working_directory: str, file_path: str, contents: str) -> str:
    wd_path, path = resolved_paths(working_directory, file_path)

    if not within_working_directory(wd_path, path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    try:
        dir = os.path.dirname(path)
        if not os.path.exists(dir):
            os.makedirs(dir)
        with open(path, 'w') as file:
            file.write(contents)
    except Exception as e:
        return f'Error: error writing to "{file_path}": {e}'

    return f'Successfully wrote to "{file_path}" ({len(contents)} characters written)'
