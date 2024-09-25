import cv2 as cv
import numpy as np


def img_transform_test():
    img1 = cv.imread(r"C:\Users\user\Pictures\vision1.png", 0)
    img2 = cv.imread(r"C:\Users\user\Pictures\vision2.png", 0)
    difference = cv.subtract(img1, img2)
    cv.imwrite(r'pics\pic1.png', difference)
    img = cv.imread(r'C:\Users\user\PycharmProjects\r2_bot\pics\screen03.jpg', 0)
    # img1_gray = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
    # img2_gray = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)
    # difference_gray = cv.subtract(img1_gray, img2_gray)
    # cv.imwrite('pic1_gray.png', difference_gray)

    _, thres = cv.threshold(img, 180, 255, cv.THRESH_BINARY)
    cv.imwrite('only_white.png', thres)

    _, tresh1 = cv.threshold(difference, 10, 255, cv.THRESH_BINARY)
    cv.imwrite('thres1.png', tresh1)

    edges = cv.Canny(img, 200, 400)
    cv.imwrite(r'edges.png', edges)

    th3 = cv.adaptiveThreshold(difference, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2)
    cv.imwrite('adaptive_gaussian_thresh.png', th3)

    blurred = cv.GaussianBlur(tresh1, (5, 5), 50)
    cv.imwrite('blurred.png', blurred)

    _, thrashed_blur = cv.threshold(blurred, 10, 255, cv.THRESH_BINARY)
    cv.imwrite('thrashed_blur.png', thrashed_blur)

    contours, _ = cv.findContours(blurred, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cv.drawContours(blurred, contours, -1, (0, 255, 0), 2)
    cv.imwrite('blurred.png', blurred)

    contours, hierarchy = cv.findContours(tresh1, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    cv.drawContours(tresh1, contours, -1, (0, 200, 255), 1)
    cv.imwrite('thres1_contours.png', tresh1)

def hp_panel_searching():
    img_names_arr = 'img1.jpg', 'img2.jpg', 'img3.jpg', 'img4.jpg', 'img5.jpg'
    for j in range(5):
        img_rgb = cv.imread('pics\\' + img_names_arr[j])
        img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
        template = cv.imread('pics/templ2.jpg')
        h, w = template.shape[:2]
        res = cv.matchTemplate(img_rgb,template,cv.TM_CCOEFF_NORMED)
        threshold = 0.8
        flag = False
        if np.amax(res) > threshold:
            flag = True
        print(flag)

def hp_panel_searching1():
    img = cv.imread(cv.samples.findFile(r'C:\Users\user\PycharmProjects\r2_bot\pics\screen05.jpg'), 0)
    templ = cv.imread(cv.samples.findFile(r'C:\Users\user\PycharmProjects\r2_bot\pics\templ2.jpg'), 0)
    res = cv.matchTemplate(img, templ, cv.TM_CCOEFF_NORMED)
    threshold = 0.9
    flag = False
    if np.amax(res) > threshold:
        flag = True
    print(flag)