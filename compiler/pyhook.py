import sys
import os
import tempfile
import subprocess
from argparse import ArgumentParser

def create_hook_script(batch_file_path):
    hook_script = f"""import subprocess
import os

# Set the path to your batch file
batch_file = "{batch_file_path}"

# Get the current working directory
current_directory = os.getcwd()

# Construct the full path to the batch file
batch_file_path = os.path.join(current_directory, batch_file)

# Run the batch file
subprocess.run(batch_file_path, shell=True)
"""
    return hook_script
def createParser():
    ap = ArgumentParser()
    ap.add_argument()
def compile_batch_script(batch_file_path, output_dir):
    # Create a temporary hook Python script
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as temp_file:
        temp_file.write(create_hook_script(batch_file_path))
        temp_hook_path = temp_file.name

    output_name = os.path.splitext(os.path.basename(batch_file_path))[0]
    output_path = os.path.join(output_dir, output_name)

    # Compile the hook script using PyInstaller
    subprocess.run(["pyinstaller", "--onefile", "-y", "-n", output_path, temp_hook_path])

    # Clean up the temporary hook script
    os.remove(temp_hook_path)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: compile-bat.py <batch_file_path> <output_directory>")
        sys.exit(1)

    batch_file_path = sys.argv[1]
    output_directory = sys.argv[2]

    compile_batch_script(batch_file_path, output_directory)
