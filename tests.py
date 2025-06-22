from functions.run_python_file import run_python_file


if __name__ == "__main__":
    wd = "calculator"
    print(run_python_file(wd, "main.py"))
    print(run_python_file(wd, "tests.py"))
    print(run_python_file(wd, "../main.py"))
    print(run_python_file(wd, "nonexistent.py"))
