import json
import os
import shutil
import logging

class MinecraftSound:
    def __init__(self, path, hash_value):
        self.path = path
        self.hash = hash_value

def process_objects_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    minecraft_sounds = []
    for key, value in data["objects"].items():
        if key.endswith(".ogg"):
            path = key
            hash_value = value["hash"]
            minecraft_sound = MinecraftSound(path, hash_value)
            minecraft_sounds.append(minecraft_sound)

    return minecraft_sounds

def find_file_in_org_directory(directory, target_file_name):
    for root, dirs, files in os.walk(directory):
        if target_file_name in files:
            return os.path.join(root, target_file_name)
    return None

def copy_file_to_files_directory(source_file, target_directory):
    shutil.copy(source_file, target_directory)

def setup_logging():
    logging.basicConfig(filename='errors.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_project():
    org_directory = 'org'
    files_directory = 'files'

    if not os.path.exists(org_directory):
        print("Error: The 'org' folder does not exist. Please create the 'org' folder with the necessary files.")
        exit()

    if os.path.exists(files_directory):
        # Remove all contents in the 'files' directory
        total_files = len(os.listdir(files_directory))
        for i, file_name in enumerate(os.listdir(files_directory), start=1):
            file_path = os.path.join(files_directory, file_name)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                print(f"\rCleaning 'files' directory: {i}/{total_files}", end='', flush=True)
            except Exception as e:
                print(f"Error cleaning 'files' directory: {str(e)}")
        print("\n'files' directory cleaned.\n")

    else:
        # Create the 'files' directory if it doesn't exist
        os.makedirs(files_directory)
        print("'files' directory created.")

def main():
    print("\nMinecraft Sound Converter\n")
    setup_logging()
    setup_project()

    file_path = 'objects.json'
    minecraft_sounds = process_objects_json(file_path)

    org_directory = 'org'
    files_directory = 'files'

    total_files = len(minecraft_sounds)

    for i, sound in enumerate(minecraft_sounds, start=1):
        file_name = sound.hash
        file_path_in_org = find_file_in_org_directory(org_directory, file_name)

        if file_path_in_org:
            target_directory = os.path.join(files_directory, os.path.dirname(sound.path))
            os.makedirs(target_directory, exist_ok=True)

            target_path_in_files = os.path.join(files_directory, sound.path)
            try:
                copy_file_to_files_directory(file_path_in_org, target_path_in_files)
                print(f"\rCopying files ({i}/{total_files})", end='', flush=True)
            except Exception as e:
                error_message = f"Error copying file for {sound.path}: {str(e)}"
                logging.error(error_message)
        else:
            error_message = f"No matching file found for {sound.path}"
            logging.error(error_message)

    print("\n\nCopy completed! The sound files can be found in the files directory.\n")

if __name__ == "__main__":
    main()
