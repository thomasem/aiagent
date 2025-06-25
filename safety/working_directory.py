import pathlib


def resolved_paths(working_directory: str, file_path: str) -> tuple[pathlib.Path, pathlib.Path]:
    wd_path = pathlib.Path(working_directory).resolve()
    path = (wd_path / (file_path)).resolve()
    return wd_path, path


def within_working_directory(working_directory: pathlib.Path, path: pathlib.Path) -> bool:
    return path.resolve().is_relative_to(working_directory.resolve())

