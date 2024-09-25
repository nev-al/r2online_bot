import cv2 as cv
import numpy as np
import time as t
import pyautogui as ag


OFFSET_SCREEN = (415, 181)
SIZE_OF_SCREEN_RECOGNIZING = (*OFFSET_SCREEN, 1115, 605)

COUNTER_TO_NAME_SCREEN_SERIES = 0


def get_scrn_series():
    img1 = cv.cvtColor(np.array(ag.screenshot(region=SIZE_OF_SCREEN_RECOGNIZING)), cv.COLOR_RGB2BGR)
    t.sleep(1)
    img2 = cv.cvtColor(np.array(ag.screenshot(region=SIZE_OF_SCREEN_RECOGNIZING)), cv.COLOR_RGB2BGR)
    difference = cv.subtract(cv.cvtColor(img1, cv.COLOR_BGR2GRAY), cv.cvtColor(img2, cv.COLOR_BGR2GRAY))
    _, difference = cv.threshold(difference, 50, 255, cv.THRESH_BINARY)
    return paint_over_character(difference)


def paint_over_character(img: np.ndarray):
    coords = ((875 - OFFSET_SCREEN[0], 460 - OFFSET_SCREEN[1]), (1030 - OFFSET_SCREEN[0], 715 - OFFSET_SCREEN[1]))
    return cv.rectangle(img, coords[0], coords[1], 0, -1)


def mouse_move():
    t.sleep(3)
    counter = 0
    while True:
        coords = find_coords()
        if counter == 10 or len(coords) == 0:
            move_the_camera()
            counter = 0
        for i in range(0, len(coords), 10):
            ag.moveTo(OFFSET_SCREEN[0] + coords[i][1][0], OFFSET_SCREEN[1] + coords[i][1][1], duration=0.1)
            if check_obj_with_cursor() == 0:
                counter = 0
                break
            else:
                counter += 1


def find_coords():
    character_point = (960 - OFFSET_SCREEN[0], 600 - OFFSET_SCREEN[1])
    difference = get_scrn_series()
    # make_screens_of_threshed(difference)
    coords = list()
    print(t.asctime())
    for i in range(difference.shape[0]):
         for j in range(difference.shape[1]):
             if difference[i][j] != 0:
                 coords.append([j, i])
    print(t.asctime())
    distances = list()
    for i in range(len(coords)):
        distances.append([np.sqrt((coords[i][0] - character_point[0]) ** 2 + (coords[i][1] - character_point[1]) ** 2),
                          (coords[i][0], coords[i][1])])
    distances.sort()
    return distances


def check_obj_with_cursor():
    scr = ag.screenshot()
    img_rgb = cv.cvtColor(np.array(scr), cv.COLOR_RGB2GRAY)
    template = cv.imread(cv.samples.findFile(r'C:\Users\user\PycharmProjects\r2_bot\pics\templ2.jpg'), 0)
    res = cv.matchTemplate(img_rgb, template, cv.TM_CCOEFF_NORMED)
    threshold = 0.9
    if np.amax(res) > threshold:
        ag.mouseDown(button='left')
        ag.mouseDown(button='right')
        ag.mouseUp(button='left')
        ag.mouseUp(button='right')
        ag.moveTo(950, 250)
        while is_there_mob_hp_after_attack_started():
            t.sleep(1)
        loot_the_drop()
        return 0
    else:
        return 1

def is_there_mob_hp_after_attack_started():
    scr = ag.screenshot(region=(857, 919, 206, 41))
    img = cv.cvtColor(np.array(scr), cv.COLOR_RGB2GRAY)
    template = cv.imread(cv.samples.findFile(r'C:\Users\user\PycharmProjects\r2_bot\pics\templ1.jpg'), 0)
    res = cv.matchTemplate(img, template, cv.TM_CCOEFF_NORMED)
    threshold = 0.9
    if np.amax(res) > threshold:
        return True
    else:
        return False

def loot_the_drop():
    for i in range(5):
        ag.keyDown('e')
        ag.keyUp('e')
        t.sleep(0.5)

def move_the_camera():
    ag.keyDown('d')
    t.sleep(1)
    ag.keyUp('d')

def make_screens_of_threshed(difference):
    global COUNTER_TO_NAME_SCREEN_SERIES
    cv.imwrite(rf'C:\Users\user\PycharmProjects\r2_bot\pics\scr{COUNTER_TO_NAME_SCREEN_SERIES}.png', difference)
    COUNTER_TO_NAME_SCREEN_SERIES += 1


def main():
    mouse_move()


if (__name__ == '__main__'):
    main()