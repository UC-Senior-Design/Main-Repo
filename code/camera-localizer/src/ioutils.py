import os, time, json, cv2

def save_image(image, run_id, camera_name, capture_index):
    path = os.path(
        "out",
        "run_{}".format(run_id),
        "cam_{}".format(camera_name),
        "capture_{:02d}_{}.png".format(capture_index, time.time())
    )
    os.makedirs(path.parent, exist_ok=True)
    cv2.imshow(path, image)


# Encode an object as JSON, then append that JSON as a new
# line in a newline-separated JSON file.
def appendLineToNLJ(path, object):
    line = json.dumps(object)
    with open(path, "a") as file:
        file.write(line + "\n")