import subprocess
import os
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a specified python file with given arguemnts.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to execute, relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="arguments to pass to the given python file."
            )
        },
        required=["file_path"]
    ),
)

def run_python_file(working_directory, file_path, args=None):
    abs_working_directory = os.path.abspath(working_directory)
    target_path = os.path.normpath(os.path.join(abs_working_directory, file_path))

    valid_target = os.path.commonpath([abs_working_directory, target_path]) == abs_working_directory

    if valid_target == False:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if os.path.isfile(target_path) == False:
        return f'Error: "{file_path}" does not exist or is not a regular file'
    if target_path.endswith(".py") == False:
        return f'Error: "{file_path}" is not a Python file'

    try:
        command = ["python", target_path]
        if args != None:
            command.extend(args)

        result = subprocess.run(command, capture_output=True, text=True, timeout=30) 

        output = ""
        if result.returncode != 0:
            output += f"Process exited with code {result.returncode}\n"
        if result.stderr == "" and result.stdout == "":
            output += f"No output produced\n"
        else:
            output += f"STDOUT: {result.stdout}\n"
            output += f"STDERR: {result.stderr}\n"

        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"