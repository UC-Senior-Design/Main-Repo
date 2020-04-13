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
    files = ioutils.get_all_file_info('./out')
    snaps = sorted(list(set(map(lambda file: int(file['snapIndex']), files))))

    line = {}
    cameras = ["0", "1", "3"]

    total = len(files)
    processed = 0
    found = 0
    for snap in snaps:
        line = {"action": "detect", "capture_index": snap, "cams": {}}
        for camera in cameras:
            file = next(file for file in files if int(file["snapIndex"]) == snap and file["camera"] == camera)
            pos = getLedPosition(file)
            line["cams"][camera] = pos
            processed += 1
            if pos is None:
                print('Failure on: {}'.format(file['path']))
            else:
                found += 1
            if (processed % 100 == 0):
                print("Processed {0} of {1}. Found {2} of {1} ({3:.2f}%)".format(processed, total, found, 100 * found / processed))
        ioutils.appendLineToNLJ('leds.ndjson', line)


run()
print('script done')
while True:
    cv2.waitKey(1)
    time.sleep(0.1)