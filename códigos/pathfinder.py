import os

def find_file(filename):
    file_path = os.getcwd()
    file_path = file_path.replace("códigos", "planilhas")
    for files in os.listdir(file_path):
            if filename in files:
                file_path = os.path.join(file_path, filename)
                return file_path

