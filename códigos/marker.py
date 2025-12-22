import os
import cv2 as cv
import pytesseract
import pathfinder as pf

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


dir_amostras = pf.set_dir("amostras")
files_amostras = os.listdir(dir_amostras)
num_files_amostras = len(files_amostras)
conf = '--psm 4 -c tessedit_char_whitelist=0123456789 tessedit_char_blacklist=abcdefghijklmnopqrstuvwxyz()[]{}|?.;, --tessdata-dir/usr/share/tesseract-ocr/tessdata_best-4.1.0'

destino = pf.set_dir("marcado")

for i in range(num_files_amostras):
    img = cv.imread(dir_amostras + files_amostras[i], cv.IMREAD_GRAYSCALE)
    img = marker(img)

    filename = files_amostras[i]
    filename, _ = os.path.splitext(filename)

    cv.imwrite(destino + filename + "_marked.png", img)
    text = pytesseract.image_to_string(img, lang='por+eng', config=conf)

    # Salva o texto em um arquivo .txt
    with open(destino + filename + ".txt", 'w') as f:
        f.write(text)

    remover_espacos(destino + filename + ".txt", destino + filename + "_filtrado.txt")