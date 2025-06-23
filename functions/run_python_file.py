import os
import subprocess

from safety.working_directory import resolved_paths, within_working_directory


def run_python_file(working_directory: str, file_path: str) -> str:
    wd_path, path = resolved_paths(working_directory, file_path)

    if not within_working_directory(wd_path, path):
        return f'Error: Cannot execute "{file_path}" as it is outside of the permitted working directory'
    if not os.path.exists(path):
        return f'Error: File "{file_path}" not found'
    if not path.suffix == ".py":
        return f'Error: "{file_path}" is not a Python file'

    try:
        result = subprocess.run(
            ["python3", path],
            cwd=wd_path,
            capture_output=True,
            timeout=30.0
        )
    except Exception as e:
        return f'Error: executing python file: {e}'

    output: str = f'Ran "{file_path}"'

    if not result.stdout and not result.stderr:
        output = f'{output}\nNo output produced'
    else:
        output = f'{output}\nSTDOUT: "{result.stdout}"\nSTDERR: "{result.stderr}"'

    if result.returncode != 0:
        output = f'{output}\nProcess exited with status code {result.returncode}'

    return output

