import os

from safety.working_directory import resolved_paths, within_working_directory


def get_files_info(working_directory: str, directory: str | None = None) -> str:
    wd_path, path = resolved_paths(working_directory, directory or "")

    if not within_working_directory(wd_path, path):
        return f'Error: cannot list "{directory}" as it is outside of the permitted working directory'
    if not os.path.isdir(path):
        return f'Error: "{directory}" is not a directory'

    entries: list[str] = []
    try:
        for file in os.listdir(path):
            filepath = os.path.join(path, file)
            entries.append(
                f'{file}: file_size={os.path.getsize(filepath)} bytes, is_dir={os.path.isdir(filepath)}'
            )
    except Exception as e:
        return f'Error: error listing directory "{directory}": {e}'

    return "\n".join(entries)

