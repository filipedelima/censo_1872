import os
import cv2 as cv
import numpy as np
import pytesseract
import pathfinder as pf

def median(img):
    return cv.medianBlur(img, 3)

def gaussian(img):
    return cv.GaussianBlur(img, (3, 3), 0)

def bilateral(img):
    return cv.bilateralFilter(img,3,75,75)

def laplacian(img):
    lap = cv.Laplacian(img, cv.CV_64F)
    return np.uint8(np.absolute(lap))

def threshold(img):
    ret, img = cv.threshold(img, 15,255, cv.THRESH_BINARY)
    return img

def erosion(img):
    kernel = np.ones((3,3), np.uint8)
    erosion = cv.erode(img, kernel, iterations = 1)
    return erosion

def marker(img):
    h, _, = img.shape

    img_bgr = cv.cvtColor(img, cv.COLOR_GRAY2BGR)

    conf = '--psm 4 -c tessedit_char_whitelist=0123456789 tessedit_char_blacklist=abcdefghijklmnopqrstuvwxyz()[]{}|?.;, --tessdata-dir/usr/share/tesseract-ocr/tessdata_best-4.1.0'
    
    bound_rects = pytesseract.image_to_boxes(img, config=conf, lang='por+eng')    

    for b in bound_rects.splitlines():
        b = b.strip().split(' ')
        img = cv.rectangle(img_bgr, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (255, 0, 0), 2)
        
    #cv.imwrite("marked.png", img_bgr)
    return img_bgr

def remover_espacos(arquivo_entrada, arquivo_saida):
    with open(arquivo_entrada, 'r') as f:
        linhas = f.readlines()
    linhas_filtradas = []
    for linha in linhas:
        linha = linha.strip()  # remove espaços em branco no início e no fim da linha
        linha = ' '.join(linha.split())  # remove espaços extras entre palavras
        if linha != '':
            linhas_filtradas.append(linha + '\n')  # adiciona a linha filtrada à lista
    with open(arquivo_saida, 'w') as f:
        f.writelines(linhas_filtradas)


def marcado(origem, destino):
    dir_amostras = pf.set_dir(origem)
    #files_amostras = os.listdir(dir_amostras)

    files_amostras = [
        arquivo for arquivo in os.listdir(dir_amostras)
        if os.path.isfile(os.path.join(dir_amostras, arquivo)) and not arquivo.endswith(('.txt', '_marked.png'))
    ]

    num_files_amostras = len(files_amostras)
    destino = pf.set_dir(destino)
    
    for i in range(num_files_amostras):
        img = cv.imread(dir_amostras + files_amostras[i], cv.IMREAD_GRAYSCALE)
        text = pytesseract.image_to_string(img, lang='por+eng', config=conf)
        img = marker(img)

        filename = files_amostras[i]
        filename, _ = os.path.splitext(filename)

        cv.imwrite(destino + filename + "_marked.png", img)

        # Salva o texto em um arquivo .txt
        with open(destino + filename + ".txt", 'w') as f:
            f.write(text)

        remover_espacos(destino + filename + ".txt", destino + filename + "_filtrado.txt")


def erosao(origem, destino):
    dir_amostras = pf.set_dir(origem)
    #files_amostras = os.listdir(dir_amostras)

    files_amostras = [
        arquivo for arquivo in os.listdir(dir_amostras)
        if os.path.isfile(os.path.join(dir_amostras, arquivo)) and not arquivo.endswith(('.txt', '_marked.png'))
    ]

    num_files_amostras = len(files_amostras)
    destino = pf.set_dir(destino)

    for i in range(num_files_amostras):
        img = cv.imread(dir_amostras + files_amostras[i], cv.IMREAD_GRAYSCALE)
        img = erosion(img)
        
        filename = files_amostras[i]
        filename, _ = os.path.splitext(filename)

        cv.imwrite(destino + filename + "_erosão.png", img)
        text = pytesseract.image_to_string(img, lang='por+eng', config=conf)
        img = marker(img)
        cv.imwrite(destino + filename + "_erosão_marked.png", img)

        with open(destino + filename + "_erosão.txt", 'w') as f:
            f.write(text)
        remover_espacos(destino + filename + "_erosão.txt", destino + filename + "_erosão_filtrado.txt")


def limiarizacao(origem, destino):
    dir_amostras = pf.set_dir(origem)
    #files_amostras = os.listdir(dir_amostras)

    files_amostras = [
        arquivo for arquivo in os.listdir(dir_amostras)
        if os.path.isfile(os.path.join(dir_amostras, arquivo)) and not arquivo.endswith(('.txt', '_marked.png'))
    ]

    num_files_amostras = len(files_amostras)
    destino = pf.set_dir(destino)

    for i in range(num_files_amostras):
        img = cv.imread(dir_amostras + files_amostras[i], cv.IMREAD_GRAYSCALE)
        img = threshold(img)
        
        filename = files_amostras[i]
        filename, _ = os.path.splitext(filename)

        cv.imwrite(destino + filename + "_limiarização.png", img)
        text = pytesseract.image_to_string(img, lang='por+eng', config=conf)
        img = marker(img)
        cv.imwrite(destino + filename + "_limiarização_marked.png", img)


        with open(destino + filename + "_limiarização.txt", 'w') as f:
            f.write(text)
        remover_espacos(destino + filename + "_limiarização.txt", destino + filename + "_limiarização_filtrado.txt")

def conversor(origem, destino):
    dir_amostras = pf.set_dir(origem)
    #files_amostras = os.listdir(dir_amostras)

    files_amostras = [
        arquivo for arquivo in os.listdir(dir_amostras)
        if os.path.isfile(os.path.join(dir_amostras, arquivo)) and not arquivo.endswith(('.txt', '_marked.png'))
    ]

    num_files_amostras = len(files_amostras)
    destino = pf.set_dir(destino)

    for i in range(num_files_amostras):
        img = cv.imread(dir_amostras + files_amostras[i], cv.IMREAD_GRAYSCALE)
        img = threshold(img)
        img = median(img)
        img = bilateral(img)
        
        filename = files_amostras[i]
        filename, _ = os.path.splitext(filename)

        cv.imwrite(destino + filename + "_conversor.png", img)
        text = pytesseract.image_to_string(img, lang='por+eng', config=conf)
        img = marker(img)
        cv.imwrite(destino + filename + "_conversor_marked.png", img)

        with open(destino + filename + "_conversor.txt", 'w') as f:
            f.write(text)
        remover_espacos(destino + filename + "_conversor.txt", destino + filename + "_conversor_filtrado.txt")

#dir_amostras = pf.set_dir("amostras")
#files_amostras = os.listdir(dir_amostras)
#num_files_amostras = len(files_amostras)
conf = '--psm 4 -c tessedit_char_whitelist=0123456789 tessedit_char_blacklist=abcdefghijklmnopqrstuvwxyz()[]{}|?.;, --tessdata-dir/usr/share/tesseract-ocr/tessdata_best-4.1.0'

marcado("amostras", "marcado")
erosao("amostras", "erosão")
limiarizacao("amostras", "limiarização")
conversor("amostras", "conversor")
erosao("limiarização", "limiarização_erosão")
limiarizacao("erosão", "erosão_limiarização")    