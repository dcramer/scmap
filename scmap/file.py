import os

def init(path):
    global file_path
    file_path = path

old_open = open

def open(*path):
    path = '\\'.join(path)
    path = path.lower()
    path = path.split('\\')
    return old_open(os.path.join(file_path, *path))
