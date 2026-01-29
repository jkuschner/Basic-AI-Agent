from config import *
import os

def get_file_content(working_directory, file_path):
    abs_working_directory = os.path.abspath(working_directory)
    target_path = os.path.normpath(os.path.join(abs_working_directory, file_path))

    valid_target = os.path.commonpath([abs_working_directory, target_path]) == abs_working_directory

    try:
        if valid_target == False:
            raise Exception(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
        if os.path.isdir(target_path):
            raise Exception(f'Error: File not found or is not a regular file: "{file_path}"')
    except Exception as e:
        print(e)
        return

    try:
        with open(target_path, "r") as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            
            return content
    except Exception as e:
        print(f"Error: {e}")