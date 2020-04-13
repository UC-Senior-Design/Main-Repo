from skimage.measure import compare_ssim
import cv2
import ioutils, detect
import os, time

def image_difference(before, after):
    # Convert images to grayscale
    before_gray = cv2.cvtColor(before, cv2.COLOR_BGR2GRAY)
    after_gray = cv2.cvtColor(after, cv2.COLOR_BGR2GRAY)

    # Compute difference using SSIM
    (similarity, diff) = compare_ssim(before_gray, after_gray, full=True)

    # compare_ssim returned the difference as floats between 0-1
    # We need to convert to ints between 0-255 for OpenCV
    diff = (diff * 255).astype("uint8")

    return similarity, diff

def get_contours(image):
    contours = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    return contours

min_area = 40
color_drone = (0, 255, 0)
color_other = (0, 0, 255)
def draw_all_contours(image, contours):
    if len(contours) == 0:
        return
    for c in contours:
        area = cv2.contourArea(c)
        if area > min_area:
            cv2.drawContours(image, [c], 0, (0, 255, 0), -1)
            
def label_image_contours(image, contours):
    if len(contours) == 0:
        return
    drone, drone_area = get_likely_drone_contour(contours)
    for c in contours:
        area = cv2.contourArea(c)
        if area > min_area:
            color = color_drone if area == drone_area else color_other
            
            x,y,w,h = cv2.boundingRect(c)
            image = cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
            
def hide_idiots(image):
    color = (255, 0, 0)
    image = cv2.rectangle(image, (0, 0), (100, 80), color, -1)
    image = cv2.rectangle(image, (100, 0), (150, 60), color, -1)
    return image


def get_likely_drone_contour(contours):
    if len(contours) > 50:  # too many contours means drone prolly out of frame
        print(len(contours))
        return None, 0
    drone = max(contours, key=cv2.contourArea) 
    return drone, cv2.contourArea(drone)

def create_new_background(old_background, new_image, old_rectangle):
    (x,y,w,h) = old_rectangle
    new_background = new_image.copy()
    new_background[y: y + h, x: x + w] = old_background[y: y + h, x: x + w]
    return new_background


def run():
    cameras = {
        "1": {
            "baseline": cv2.imread("./drone/run_1583703669.2115672__cam_1__snap_27_1583703677.618475.png"),
        },
        "2": {
            "baseline": cv2.imread("./drone/run_1583703669.2115672__cam_2__snap_28_1583703677.983904.png"),
        },
        "3": {
            "baseline": hide_idiots(cv2.imread("./drone/run_1583703669.2115672__cam_3__snap_28_1583703678.006104.png")),
        }
    }

    files = ioutils.get_all_file_info('./drone')
    snaps = sorted(list(set(map(lambda file: int(file['snapIndex']), files))))
    for snap in snaps:
        line = {"action": "detect", "capture_index": snap, "cams": {}}
        for camera in cameras.keys():
            file = next(file for file in files if int(file["snapIndex"]) == snap and file["camera"] == camera)
            baseline = cameras[camera]['baseline']
            image = cv2.imread('./drone/' + file['path'])
            if camera == "3":
                image = hide_idiots(image)
            (similarity, diff) = image_difference(baseline, image)

            diff_thresholded = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
            contours = get_contours(diff_thresholded)
            with_contours = image.copy()
            draw_all_contours(with_contours, contours)
            labelled_image = image.copy()
            label_image_contours(labelled_image, contours)

            x = (int(camera) - 1) * 300 + 50

            window_names = [
                "original_labelled",
                "baseline",
                "diff",
                "diff_thresholded",
                "contours"
            ]
            window_images = [
                labelled_image,
                baseline, 
                diff,
                diff_thresholded,
                with_contours
            ]

            detect.fit_windows(list(map(lambda x: x + camera, window_names)), window_images, x, 1100)
            drone_contour = get_likely_drone_contour(contours)[0]
            drone_rect = cv2.boundingRect(drone_contour)
            line["cams"][camera] = drone_rect
            cameras[camera]['baseline'] = create_new_background(cameras[camera]['baseline'], image, drone_rect)
        ioutils.appendLineToNLJ('drones.ndjson', line)
        time.sleep(0.1)
    
run()
cv2.waitKey(10)

