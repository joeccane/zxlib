import os
from pathlib import Path
import logging
from .env import callSystemCMD as syscall

def create_requirements_txt(project_path: str) -> None:
    try:
        syscall("pipreqs", [project_path, "--force"])
    except Exception as e:
        logging.error(f"Error generating requirements.txt: {e}")

def create_virtual_environment(venv_path: str) -> None:
    try:
        syscall("python", ["-m", "venv", venv_path])
    except Exception as e:
        logging.error(f"Error creating virtual environment: {e}")
