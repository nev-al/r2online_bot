from pynput import keyboard
import os
import cv2 as cv
import numpy as np
import time as t
import pyautogui as ag


OFFSET_SCREEN = (415, 181)
SIZE_OF_SCREEN_RECOGNIZING = (*OFFSET_SCREEN, 1115, 605)
THRESHOLD_TO_RECOGNIZE = 50
TRIES_TO_LOOT_THE_DROP = 5
TRIES_TO_CHECK_DOTS_BEFORE_TURN = 5
SECS_UNTIL_SCRIPT_EXECUTION = 2

COUNTER_TO_NAME_SCREEN_SERIES = 0


def on_release(key):
    if key == keyboard.Key.esc:
        os._exit(0)


def get_scrn_series():
    img1 = cv.cvtColor(np.array(ag.screenshot(region=SIZE_OF_SCREEN_RECOGNIZING)), cv.COLOR_RGB2BGR)
    t.sleep(1)
    img2 = cv.cvtColor(np.array(ag.screenshot(region=SIZE_OF_SCREEN_RECOGNIZING)), cv.COLOR_RGB2BGR)
    difference = cv.subtract(cv.cvtColor(img1, cv.COLOR_BGR2GRAY), cv.cvtColor(img2, cv.COLOR_BGR2GRAY))
    _, difference = cv.threshold(difference, THRESHOLD_TO_RECOGNIZE, 255, cv.THRESH_BINARY)
    return paint_over_character(difference)


def paint_over_character(img: np.ndarray):
    coords = ((840 - OFFSET_SCREEN[0], 460 - OFFSET_SCREEN[1]), (1030 - OFFSET_SCREEN[0], 715 - OFFSET_SCREEN[1]))
    return cv.rectangle(img, coords[0], coords[1], 0, -1)


def mouse_move():
    t.sleep(SECS_UNTIL_SCRIPT_EXECUTION)
    counter = 0
    while True:
        coords = find_coords()
        if counter == TRIES_TO_CHECK_DOTS_BEFORE_TURN or len(coords) == 0:
            move_the_camera()
            counter = 0
        for i in range(0, len(coords)):
            ag.moveTo(OFFSET_SCREEN[0] + coords[i][1][0], OFFSET_SCREEN[1] + coords[i][1][1], duration=0.1)
            if check_obj_with_cursor() == 0:
                counter = 0
                break
            else:
                counter += 1


def find_coords():
    character_point = (960 - OFFSET_SCREEN[0], 600 - OFFSET_SCREEN[1])
    difference = get_scrn_series()
    ret, thresh = cv.threshold(difference, 15, 255, 0)
    contours1, hierarchy = cv.findContours(thresh, 1, 2)
    cv.drawContours(thresh, contours1, -1, 255, 10)
    contours2, hierarchy = cv.findContours(thresh, 1, 2)
    coords = list()
    for i in range(len(contours2)):
        cnt = contours2[i]
        area = cv.contourArea(cnt)
        if area >= 1000:
            M = cv.moments(cnt)
            cx, cy = int(M['m10'] / M['m00']), int(M['m01'] / M['m00'])
            coords.append([cx, cy])
    # make_screens_of_threshed(img)
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
    for i in range(TRIES_TO_LOOT_THE_DROP):
        ag.keyDown('e')
        ag.keyUp('e')
        t.sleep(0.5)

def move_the_camera():
    ag.keyDown('d')
    t.sleep(1)
    ag.keyUp('d')


def make_screens_of_threshed(difference):
    global COUNTER_TO_NAME_SCREEN_SERIES
    print(f'screened {COUNTER_TO_NAME_SCREEN_SERIES}')
    cv.imwrite(rf'C:\Users\user\PycharmProjects\r2_bot\pics\scr{COUNTER_TO_NAME_SCREEN_SERIES}.png', difference)
    COUNTER_TO_NAME_SCREEN_SERIES += 1


def apply_setting_from_file():
    global OFFSET_SCREEN, SIZE_OF_SCREEN_RECOGNIZING, THRESHOLD_TO_RECOGNIZE, TRIES_TO_LOOT_THE_DROP, \
        TRIES_TO_CHECK_DOTS_BEFORE_TURN, SECS_UNTIL_SCRIPT_EXECUTION
    if os.path.exists('settings.txt'):
        with open('settings.txt', 'rt') as fl:
            file_content = fl.read()
            s = file_content.split('\n')
            cleaned = s[1][s[1].index('(') + 1:s[1].index(')')].split(', ')
            OFFSET_SCREEN = tuple((int(cleaned[0]), int(cleaned[1])))
            SIZE_OF_SCREEN_RECOGNIZING = tuple((*OFFSET_SCREEN, int(cleaned[2]), int(cleaned[3])))
            THRESHOLD_TO_RECOGNIZE = int(s[2][s[2].index('=') + 1:])
            TRIES_TO_LOOT_THE_DROP = int(s[3][s[3].index('=') + 1:])
            TRIES_TO_CHECK_DOTS_BEFORE_TURN = int(s[4][s[4].index('=') + 1:])
            SECS_UNTIL_SCRIPT_EXECUTION = int(s[5][s[5].index('=') + 1:])
    else:
        apply_default_settings()


def apply_default_settings():
    global OFFSET_SCREEN, SIZE_OF_SCREEN_RECOGNIZING, THRESHOLD_TO_RECOGNIZE, TRIES_TO_LOOT_THE_DROP, \
                         TRIES_TO_CHECK_DOTS_BEFORE_TURN, SECS_UNTIL_SCRIPT_EXECUTION
    OFFSET_SCREEN = (415, 181)
    SIZE_OF_SCREEN_RECOGNIZING = (*OFFSET_SCREEN, 1115, 605)
    THRESHOLD_TO_RECOGNIZE = 50
    TRIES_TO_LOOT_THE_DROP = 5
    TRIES_TO_CHECK_DOTS_BEFORE_TURN = 10
    SECS_UNTIL_SCRIPT_EXECUTION = 2
    s = f'OFFSET_SCREEN={OFFSET_SCREEN}\nSIZE_OF_SCREEN_RECOGNIZING={SIZE_OF_SCREEN_RECOGNIZING}\n' \
        f'THRESHOLD_TO_RECOGNIZE={THRESHOLD_TO_RECOGNIZE}\nTRIES_TO_LOOT_THE_DROP={TRIES_TO_LOOT_THE_DROP}\n' \
        f'TRIES_TO_CHECK_DOTS_BEFORE_TURN={TRIES_TO_CHECK_DOTS_BEFORE_TURN}\n'\
        f'SECS_UNTIL_SCRIPT_EXECUTION={SECS_UNTIL_SCRIPT_EXECUTION}'
    with open('settings.txt', 'wt') as fl:
        print(s, end='', file=fl)


def main():
    apply_setting_from_file()
    listener = keyboard.Listener(
        on_release=on_release)
    listener.start()
    mouse_move()


if __name__ == '__main__':
    main()