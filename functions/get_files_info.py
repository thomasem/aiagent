import os


def get_files_info(working_directory: str, directory: str | None = None) -> str:
    entries: list[str] = []
    wd_path = os.path.abspath(working_directory)
    path = os.path.abspath(os.path.join(wd_path, directory or ""))

    if not path.startswith(wd_path):
        return f'Error: cannot list "{directory}" as it is outside of the permitted working directory'
    if not os.path.isdir(path):
        return f'Error: "{directory}" is not a directory'

    try:
        for file in os.listdir(path):
            filepath = os.path.join(path, file)
            entries.append(
                f'{file}: file_size={os.path.getsize(filepath)} bytes, is_dir={os.path.isdir(filepath)}'
            )
    except Exception as e:
        return f'Error: error listing directory "{directory}": {e}'

    return "\n".join(entries)

