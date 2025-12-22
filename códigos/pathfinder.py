import os

def find_file(filename, folder):
    file_path = os.getcwd()
    file_path = file_path.replace("códigos", folder)
    for files in os.listdir(file_path):
            if filename in files:
                file_path = os.path.join(file_path, filename)
                return file_path


def set_dir(folder):
    path = os.getcwd()
    if os.path.exists(path + "/" + folder) == True:
        path = os.path.join(path, folder)
        path += "/"
    else:
        path += "/" + folder + "/"
        os.mkdir(path)
    return path