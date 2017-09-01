import os
from os import path
import tempfile
import shutil


def get_filename(file_path, with_extension=True):
    name = path.basename(file_path)
    if not with_extension:
        name = name[:name.rfind('.')]
    return name


def file_exists(file_path):
    return path.exists(file_path)


def resolve_path(file_path):
    return path.abspath(file_path)


def resolve_subpath(folder_path, *child_paths):
    full_path = resolve_path(folder_path)
    for child_path in child_paths:
        full_path += path.sep + child_path
    return full_path


def make_folders(file_path, including_this=False):
    file_path = resolve_path(file_path)
    if including_this:
        file_path += path.sep
    folder_path = path.dirname(file_path)
    if not path.exists(folder_path):
        os.makedirs(folder_path)


def list_files(folder_path):
    return os.listdir(folder_path)


def get_parent(file_path):
    return path.dirname(resolve_path(file_path))


def get_temporary_file_path(prefix=None):
    file_path = tempfile.mkstemp(prefix=prefix)[1]
    os.remove(file_path)
    return file_path


def move_file(source, destination):
    make_folders(destination)
    shutil.move(source, destination)
