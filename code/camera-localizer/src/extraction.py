import os
import re
import cv2
import detect
import time
import random
import ioutils

def getLedPosition(fileInfo):
    img = cv2.imread('./out/' + fileInfo['path'])
    if img is None:
        print('bad image: ' + fileInfo['path'])
        return None
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    point = detect.find_led(hsv)

    # detect.showInMovedWindow("raw", img, 100, 800)
    # cv2.imshow('raw', img)
    # cv2.waitKey(1)
    return point


def run():
    files = map(ioutils.getFileInfo, os.listdir('./out'))
    files = list(filter(lambda f: f is not None, files))
    random.shuffle(files)
    total = len(files)
    processed = 0
    found = 0
    for file in files:
        pos = getLedPosition(file)
        processed += 1
        if pos is None:
            print('Failure on: {}'.format(file['path']))
        else:
            found += 1
        if (processed % 100 == 0):
            print("Processed {0} of {1}. Found {2} of {1} ({3:.2f}%)".format(processed, total, found, 100 * found / processed))
        # if (file['camera'] == '3'):
        #     time.sleep(1)

run()
print('script done')
while True:
    cv2.waitKey(1)
    time.sleep(0.1)