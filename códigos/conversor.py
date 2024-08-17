import os
import cv2 as cv

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
    ret, img = cv.threshold(img, 127,255, cv.THRESH_BINARY)
    return img


dirCensoBR = 'liv25477_v1_br/'
dirCensoCE = 'liv25477_v4_ce/'

#guarda todos os nomes dos arquivos da pasta em uma lista
filesBR = os.listdir(dirCensoBR)
filesCE = os.listdir(dirCensoCE)

num_filesBR = len(filesBR)
num_filesCE = len(filesCE)

#criando novas pastas no sistema para salvar as imagens editadas
new_folder = 'editado/'
new_folderBR = 'editado/liv25477_v1_br/'
new_folderCE = 'editado/liv25477_v4_ce/'
os.mkdir(new_folder)
os.mkdir(new_folderBR)
os.mkdir(new_folderCE)

for i in range(num_filesBR):
    img = cv.imread(dirCensoBR + filesBR[i], cv.IMREAD_GRAYSCALE)
    img = threshold(img)
    img = median(img)
    img = bilateral(img)
    cv.imwrite(new_folderBR + filesBR[i], img)


for i in range(num_filesCE):
    img = cv.imread(dirCensoCE + filesCE[i], cv.IMREAD_GRAYSCALE)
    img = threshold(img)
    img = median(img)
    img = bilateral(img)
    cv.imwrite(new_folderCE + filesCE[i], img)

