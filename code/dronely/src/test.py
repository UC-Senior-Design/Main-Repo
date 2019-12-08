import numpy as np
import cv2
import time
import requests
import random
import csv


def find_led_center(hsv_image):
    in_lower_red_range = cv2.inRange(hsv_image, np.array([0, 100, 200]), np.array([[10, 255, 255]]))
    in_upper_red_range = cv2.inRange(hsv_image, np.array([170, 100, 200]), np.array([[180, 255, 255]]))
    in_red_range = cv2.bitwise_or(in_lower_red_range, in_upper_red_range)
    in_value_range = cv2.inRange(hsv_image, np.array([0, 0, 250]), np.array([0, 255, 255]))

    se1 = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    se2 = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    closing_kernel_red = np.ones((15, 15), np.uint8)
    closing_kernel = np.ones((10, 10), np.uint8)
    opening_kernel = np.ones((3, 3), np.uint8)
    in_red_range = cv2.morphologyEx(in_red_range, cv2.MORPH_CLOSE, closing_kernel_red, iterations=2)
    # in_red_range = cv2.morphologyEx(in_red_range, cv2.MORPH_OPEN, opening_kernel, iterations=1)
    in_value_range = cv2.morphologyEx(in_value_range, cv2.MORPH_CLOSE, closing_kernel, iterations=2)
    # in_value_range = cv2.morphologyEx(in_value_range, cv2.MORPH_OPEN, opening_kernel, iterations=1)

    cv2.dilate(in_red_range, None, dst=in_red_range, iterations=2)
    cv2.dilate(in_value_range, None, dst=in_value_range, iterations=1)

    cv2.imshow('red', in_red_range)
    cv2.imshow('value', in_value_range)

    best = cv2.bitwise_and(in_red_range, in_value_range)
    best = cv2.morphologyEx(best, cv2.MORPH_CLOSE, se1)
    best = cv2.morphologyEx(best, cv2.MORPH_OPEN, se2)

    contours, hierarchy = cv2.findContours(best, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if len(contours) != 0:
        biggest = max(contours, key=cv2.contourArea)
        moments = cv2.moments(biggest)
        cx = int(moments["m10"] / moments["m00"])
        cy = int(moments["m01"] / moments["m00"])
        return cx, cy
    return None


def get_next_point(lr, fr, ud):
    new_lr = lr + random.randint(-150, +150)
    new_fr = fr + random.randint(-150, +150)
    new_ud = ud + random.randint(-150, +150)
    if new_lr < 0 or new_fr < 0 or new_ud < 0 or new_lr > 7000 or new_fr > 1300 or new_ud > 1500:
        return get_next_point(lr, fr, ud)
    return new_lr, new_fr, new_ud


def move_flex(lr, fr, ud):
    json = {
        'jsonrpc': '2.0',
        'method': 'instrument.head.moveTo',
        'params': {
            'instrument_id': 'FLX0122030515',
            'target': {
                'left_right': lr,
                'front_rear': fr,
                'up_down': ud
            }
        },
        'id': 0
    }

    r = requests.post('http://localhost:55555/api', json=json)
    pass


# camera_paths = ['/dev/video2']
camera_paths = ['/dev/video2', '/dev/video4', '/dev/video6']
# camera_paths = ['/dev/video6']
cameras = []
for path in camera_paths:
    capture = cv2.VideoCapture(path)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    time.sleep(2)
    capture.set(cv2.CAP_PROP_CONTRAST, 180)
    capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    cameras.append(capture)

print('here we go')
last_capture = 0
current_pos = (0, 0, 0)

while (True):
    captures = []
    for camera_index in range(len(cameras)):
        camera = cameras[camera_index]
        _, capture = camera.read()
        captures.append(capture)

    if time.time() - last_capture > 1:
        last_capture = time.time()
        centers = list(map(lambda cap: find_led_center(cv2.cvtColor(cap, cv2.COLOR_BGR2HSV)), captures))
        print(centers)
        print(current_pos)

        with open('points_2.csv', mode='a') as employee_file:
            employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            employee_writer.writerow([time.time(), str(centers[0]), str(centers[1]), str(centers[2]), str(current_pos)])

        for cap_index in range(len(captures)):
            cap = captures[cap_index]
            if centers[cap_index] is not None:
                cv2.circle(cap, centers[cap_index], 20, (255, 0, 255), 3)
            small = cv2.resize(cap, (int(cap.shape[1] * 0.4), int(cap.shape[0] * 0.4)))
            cv2.imshow('cam: ' + str(cap_index), small)

        (current_pos) = get_next_point(*current_pos)
        move_flex(*current_pos)

    # for camera_index in range(len(cameras)):
    #     camera_path = camera_paths[camera_index]
    #     camera = cameras[camera_index]
    #
    #     # Capture frame-by-frame
    #     # _, frame1 = camera.read()
    #     # _, frame2 = camera.read()
    #     # _, frame3 = camera.read()
    #     # _, frame4 = camera.read()
    #     # frame = cv2.addWeighted(cv2.addWeighted(frame1, 0.5, frame2, 0.5, 0.0), 0.5, cv2.addWeighted(frame3, 0.5, frame4, 0.5, 0.0), 0.5, 0.0)
    #     _, frame = camera.read()
    #
    #     # Our operations on the frame come here
    #     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #     center = find_led_center(hsv)
    #     if center is not None:
    #         cv2.circle(frame, center, 20, (255,255,255), 3)
    #         cv2.putText(frame, str(center[0]) + ', ' + str(center[1]), (center[0] + 10, center[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,255))
    #
    #     # Display the resulting frame
    #     cv2.imshow(camera_path + '_raw', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
for camera in cameras:
    camera.release()
cv2.destroyAllWindows()
