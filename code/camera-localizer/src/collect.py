import cv2
import time
import camera
import detect
import os
import flex
import json

camera_paths = [0, 1, 3]  # Indices of cameras passed to cv2.VideoCapture
cameras = []

# Load each camera
for path in camera_paths:
    capture = cv2.VideoCapture(path)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
    time.sleep(1)
    capture.set(cv2.CAP_PROP_CONTRAST, 180)
    capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    cameras.append(capture)
    print("Added new camera {}".format(path))

capture_index = 0
timestamp = time.time()

movements_since_home = 0
flex.home()
pos = flex.get_random_point_in_bounds()

out_file = "out/run_{}__flex_points.csv".format(timestamp)

def write_line(line):
    with open(out_file, mode='a') as f:
        f.write(json.dumps(line) + '\n')

# Capture video from each camera
while (True):
    if (movements_since_home > 100):
        flex.home()
        write_line({'action': 'home', 'pos': (0,0,0), 'capture_index': capture_index, 'time': time.time()})
        pos = flex.get_random_point_in_bounds()
        movements_since_home = 0
    else:
        pos = flex.get_random_nearby_point(pos, 200)
    flex.move_to(pos)
    movements_since_home += 1
    write_line({'action': 'move', 'pos': pos, 'capture_index': capture_index, 'time': time.time()})

    snaps = camera.capture_all_slow(cameras)
    for path, snap in zip(camera_paths, snaps):
        name = "Camera {}".format(path)
        if (snap is None or snap.size < 1):
            print('Bad capture on {}'.format(path))
            break

        path = "out/run_{}__cam_{}__snap_{}_{}.png".format(
            timestamp,
            path,
            capture_index,
            time.time()
        )
        cv2.imwrite(path, snap)

        cv2.imshow(name, snap)
        cv2.waitKey(1)

        # hsv = cv2.cvtColor(snap, cv2.COLOR_BGR2HSV)
        # led_center = detect.find_led(hsv, name)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    capture_index = capture_index + 1
    # time.sleep(0.2)

for camera in cameras:
    camera.release()
cv2.destroyAllWindows()