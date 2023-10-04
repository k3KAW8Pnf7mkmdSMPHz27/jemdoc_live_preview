import logging
import os
import shutil
import subprocess
from pathlib import Path
from typing import Union

logging.basicConfig(level=logging.INFO)


WORKING_DIR: Path = Path.cwd()
JEMDOC_DIR: Path = Path(os.environ.get("JEMDOC_DIR", "jemdoc_mathjax")).resolve()
PYTHON_INTERPRETER: str = os.environ.get("PYTHON_INTERPRETER", "python3")
JEMDOC_EXECUTABLE = os.environ.get("JEMDOC_EXECUTABLE", "jemdoc_mathjax/jemdoc")


def compile_jemdoc_file(file_path: Union[Path]):
    """Compile a single jemdoc file."""
    if JEMDOC_DIR in file_path.parents:
        return
    try:
        logging.info(f"Compiling {file_path}")
        subprocess.run(
            [
                PYTHON_INTERPRETER,
                JEMDOC_EXECUTABLE,
                file_path.name,
            ],
            cwd=WORKING_DIR,
            check=True,
        )
    except subprocess.CalledProcessError as processError:
        logging.error(f"Failed to compile {file_path}. Error {processError}")


def compile_all_jemdoc_files():
    """Compile all jemdoc files in the directory and subdirectories."""
    for file_path in WORKING_DIR.rglob("*.jemdoc"):
        compile_jemdoc_file(file_path)


def copy_default_css_file():
    """
    Check if any CSS file exists in the output directory.
    If not found, copy the default CSS file to that directory.

    Returns:
    - None
    """
    if not list(WORKING_DIR.glob("*.css")):
        jemdoc_css = JEMDOC_DIR / "css/jemdoc.css"
        logging.info(
            f"Did not find a css file in {WORKING_DIR}, attempting to copy the default one at {jemdoc_css}"
        )
        shutil.copy(jemdoc_css, WORKING_DIR / "jemdoc.css")


if __name__ == "__main__":
    WORKING_DIR.mkdir(exist_ok=True)
    copy_default_css_file()
    compile_all_jemdoc_files()
