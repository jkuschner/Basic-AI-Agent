import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    abs_working_directory = os.path.abspath(working_directory)
    target_directory = os.path.normpath(os.path.join(abs_working_directory, directory))

    valid_target_directory = os.path.commonpath([abs_working_directory, target_directory]) == abs_working_directory

    if valid_target_directory == False:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if os.path.isdir(target_directory) == False:
        return f'Error: "{directory}" is not a directory'

    result = []
    for entry in os.listdir(target_directory):
        try:
            file_dict = {}
            fullpath = os.path.join(target_directory, entry)
            print(f"\t- {entry}: file_size={os.path.getsize(fullpath)}, is_dir={os.path.isdir(fullpath)}")
            file_dict["file_size"] = os.path.getsize(fullpath)
            file_dict["is_dir"] = os.path.isdir(fullpath)
            file_dict["name"] = entry
            result.append(file_dict)
        except OSError:
            return f"Error: file {fullpath} cannot be found or does not exist."
        except Exception as e:
            return f"Error: {e}"
    return result