import os
import subprocess


def run_python_file(working_directory: str, file_path: str) -> str:
    wd_path = os.path.abspath(working_directory)
    path = os.path.abspath(os.path.join(wd_path, file_path))

    if not path.startswith(wd_path):
        return f'Error: Cannot execute "{file_path}" as it is outside of the permitted working directory'
    if not os.path.exists(path):
        return f'Error: File "{file_path}" not found'
    if not path.endswith(".py"):
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

