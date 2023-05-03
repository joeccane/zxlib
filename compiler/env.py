import os
import sys
import subprocess
import importlib
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
def callSystemCMD(cmd, args: list, timeout=None, env=None):
    try:
        env_vars = os.environ.copy()
        if env:
            env_vars.update(env)
        result = subprocess.run([cmd, *args], capture_output=True, text=True, check=True, timeout=timeout, env=env_vars)
        return result.stdout
    except subprocess.TimeoutExpired as e:
        logging.error(f"Timeout calling {cmd}: {e}")
        return e
    except subprocess.CalledProcessError as e:
        logging.error(f"Error calling {cmd}: {e}")
        return e
    
def check_and_install_pipreqs():
    try:
        importlib.import_module('pipreqs')
    except ImportError:
        logging.info("pipreqs not found, installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pipreqs"])
        except subprocess.CalledProcessError as e:
            logging.error(f"Error installing pipreqs: {e}")
            sys.exit(1)

def create_requirements_file(project_folder):
    check_and_install_pipreqs()
    logging.info("Creating requirements.txt file...")
    try:
        subprocess.check_call([sys.executable, "-m", "pipreqs", project_folder])
    except subprocess.CalledProcessError as e:
        logging.error(f"Error creating requirements.txt: {e}")
        sys.exit(1)

def create_virtual_environment(venv_path):
    try:
        subprocess.check_call([sys.executable, "-m", "venv", venv_path])
        activate_path = os.path.join(venv_path, "Scripts", "activate" if sys.platform != "linux" else "activate.sh")
        deactivate_path = os.path.join(venv_path, "Scripts", "deactivate" if sys.platform != "linux" else "deactivate.sh")
        return activate_path, deactivate_path
    except subprocess.CalledProcessError as e:
        logging.error(f"Error creating virtual environment: {e}")
        sys.exit(1)


import os
import sys
import subprocess
import importlib
import logging
from typing import Tuple

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

class VirtualEnvironment:
    def __init__(self, venv_path: str):
        self.venv_path = venv_path
        self.activate_path, self.deactivate_path = self._create_virtual_environment(venv_path)

    def __enter__(self):
        self.activate()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.deactivate()

    def _create_virtual_environment(self, venv_path: str) -> Tuple[str, str]:
        try:
            subprocess.check_call([sys.executable, "-m", "venv", venv_path])
            activate_path = os.path.join(venv_path, "Scripts", "activate" if sys.platform != "linux" else "activate.sh")
            deactivate_path = os.path.join(venv_path, "Scripts", "deactivate" if sys.platform != "linux" else "deactivate.sh")
            return activate_path, deactivate_path
        except subprocess.CalledProcessError as e:
            logging.error(f"Error creating virtual environment: {e}")
            raise

    def activate(self):
        try:
            subprocess.check_call([self.activate_path], shell=True)
            logging.info(f"Activated virtual environment at '{self.venv_path}'.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error activating virtual environment: {e}")
            raise

    def deactivate(self):
        try:
            subprocess.check_call([self.deactivate_path], shell=True)
            logging.info(f"Deactivated virtual environment at '{self.venv_path}'.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error deactivating virtual environment: {e}")
            raise

# Usage example
if __name__ == "__main__":
    venv_path = os.path.join(os.path.abspath("."), "venv")
    with VirtualEnvironment(venv_path) as venv:
        # Your code here
        pass