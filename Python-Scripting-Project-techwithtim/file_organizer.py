import os
import sys #access to command line arguments
import shutil


def get_unique_extensions(source):
    extensions = set()
    for root, dirs, files in os.walk(source):
        for filename in files:
            _, ext = os.path.splitext(filename)
            if ext:
                extensions.add(ext)
    return extensions
def make_folder_names(extensions):
    folder_map = {}
    for ext in extensions:
        folder_name = ext.replace(".", "") + "_files"  # e.g. ".py" → "py_files"
        folder_map[ext] = folder_name
    return folder_map

def make_dir(path, folders):
    if not os.path.exists(path):
        os.mkdir(path)

def move_files(source, target, folder_map):
    for root, dirs, files in os.walk(source):
        for filename in files:
            _, ext = os.path.splitext(filename)
            if ext in folder_map:
                folder_name = folder_map[ext]
                dest_folder = os.path.join(target, folder_name)
                if not os.path.exists(dest_folder):
                    os.mkdir(dest_folder)
                source_file = os.path.join(root, filename)
                dest_file = os.path.join(dest_folder, filename)
                shutil.copy(source_file, dest_file)    

def main(source, target):
    cwd = os.getcwd()
    source_path = os.path.join(cwd, source)
    target_path = os.path.join(cwd, target)
    exts = get_unique_extensions(source_path)
    print(exts)
    folders = make_folder_names(exts)
    print(folders)
    make_dir(target_path , folders)
    move_files(source, target, folders)
    

if __name__ == "__main__":
    args = sys.argv
    if len(args) != 3:
        raise Exception("You must pass a source and target directory - only.")

    source, target = args[1:]
    main(source, target)