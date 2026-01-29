import os

def get_files_info(working_directory, directory="."):
    abs_working_directory = os.path.abspath(working_directory)
    target_directory = os.path.normpath(os.path.join(abs_working_directory, directory))

    valid_target_directory = os.path.commonpath([abs_working_directory, target_directory]) == abs_working_directory

    try:
        if valid_target_directory == False:
            raise Exception(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        if os.path.isdir(target_directory) == False:
            raise Exception(f'Error: "{directory}" is not a directory')
    except Exception as e:
        print(e)
        return

    for entry in os.listdir(target_directory):
        try:
            fullpath = os.path.join(target_directory, entry)
            print(f"\t- {entry}: file_size={os.path.getsize(fullpath)}, is_dir={os.path.isdir(fullpath)}")
        except OSError:
            print(f"Error: file {fullpath} cannot be found or does not exist.")
        except Exception as e:
            print(f"Error: {e}")