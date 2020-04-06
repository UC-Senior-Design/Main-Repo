import os, time, json, cv2, re
p = re.compile(r"run_(\d+\.\d+)__cam_(\d)__snap_(\d+)_(\d+.\d+).png")


def get_all_file_info(directory):
    def sort_key(file):
        return 'cam{}_time{}'.format(file['camera'], file['snapTime'])
    files = map(getFileInfo, os.listdir(directory))
    files = list(filter(lambda f: f is not None, files))
    files.sort(key=sort_key)
    return files

def getFileInfo(file):
    def sort_key():
        pass

    match = p.match(file)
    if match is None:
        return None
    return {
        "path": file,
        "run": match.group(1),
        "camera": match.group(2),
        "snapIndex": match.group(3),
        "snapTime": match.group(4),
    }

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