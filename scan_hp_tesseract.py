from PIL import Image
import pytesseract as tes
import re


tes.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
hp_coords = (918, 1028, 997, 1051)


def get_hp_value(img):
    # img = r"C:\Users\user\Pictures\hp_value.png"
    hp_value = tes.image_to_string(img)
    pattern = re.compile(r'(\d*)\D*(\d*)')
    result = pattern.findall(hp_value)
    current_hp = int(result[0][0])
    max_hp = int(result[0][1])
    print(f'hp_value: {hp_value}, current_hp: {current_hp}, max_hp: {max_hp}')


def get_image(indx):
    img = Image.open(rf'C:\Users\user\PycharmProjects\r2_bot\pics\img{indx}.jpg')
    return img.crop(hp_coords)


for i in range(1, 6):
    get_hp_value(get_image(i))

