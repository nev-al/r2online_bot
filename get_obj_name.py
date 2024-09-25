from PIL import Image
import pytesseract as tes
import cv2 as cv
import numpy as np


def get_text():
    img = cv.imread(r'C:\Users\user\PycharmProjects\r2_bot\pics\img6_gk.jpg', 0)
    _, thres = cv.threshold(img, 180, 255, cv.THRESH_BINARY)
    cv.imwrite('only_white.png', thres)

    tes.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
    img = r'C:\Users\user\PycharmProjects\r2_bot\only_white.png'
    s = tes.image_to_string(Image.open(img), lang='rus')

    s = s.split()
    print(s)
