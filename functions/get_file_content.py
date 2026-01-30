from config import *
from google.genai import types
import os

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Outputs the content of a specified file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to read from, relative to the working directory (default is the working directory itself)",
            ),
        },
        required=["file_path"]
    ),
)

def get_file_content(working_directory, file_path):
    abs_working_directory = os.path.abspath(working_directory)
    target_path = os.path.normpath(os.path.join(abs_working_directory, file_path))

    valid_target = os.path.commonpath([abs_working_directory, target_path]) == abs_working_directory

    if valid_target == False:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(target_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(target_path, "r") as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            
            return content
    except Exception as e:
        return f"Error: {e}"