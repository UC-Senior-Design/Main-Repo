import cv2
import numpy as np

def get_red(hsv_image):
    in_lower_red_range = cv2.inRange(hsv_image, np.array([0, 90, 150]), np.array([[10, 255, 255]]))
    in_upper_red_range = cv2.inRange(hsv_image, np.array([170, 90, 90]), np.array([[180, 255, 255]]))
    return cv2.bitwise_or(in_lower_red_range, in_upper_red_range)
    
def get_bright(hsv_image):
    return cv2.inRange(hsv_image, np.array([0, 0, 200]), np.array([180, 50, 255]))

def find_led(hsv_image):
    dilation_kernel = np.ones((3, 3), np.uint8)
    closing_kernel = np.ones((10, 10), np.uint8)

    red = get_red(hsv_image)
    red = cv2.dilate(red, dilation_kernel, iterations = 1)
    red = cv2.morphologyEx(red, cv2.MORPH_CLOSE, closing_kernel, iterations=1)
    best = best_contour(red)
    if best is not None:
        return best

    bright = get_bright(hsv_image)
    bright = cv2.dilate(bright, dilation_kernel, iterations = 1)
    bright = cv2.morphologyEx(bright, cv2.MORPH_CLOSE, closing_kernel, iterations=1)
    return best_contour(bright)

def best_contour(hsv_image):
    contours, hierarchy = cv2.findContours(hsv_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if len(contours) != 0:
        biggest = max(contours, key=cv2.contourArea)
        moments = cv2.moments(biggest)
        cx = int(moments["m10"] / moments["m00"])
        cy = int(moments["m01"] / moments["m00"])
        return cx, cy

    return None

def showInMovedWindow(winname, img, x, y):
    cv2.namedWindow(winname)        # Create a named window
    cv2.moveWindow(winname, x, y)   # Move it to (x,y)
    cv2.imshow(winname,img)

# old function
def find_led_center(hsv_image):
    in_lower_red_range = cv2.inRange(hsv_image, np.array([0, 100, 200]), np.array([[10, 255, 255]]))
    in_upper_red_range = cv2.inRange(hsv_image, np.array([170, 100, 200]), np.array([[180, 255, 255]]))
    in_red_range = get_red(hsv_image)
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
    cv2.waitKey(1)
    cv2.imshow('value', in_value_range)
    cv2.waitKey(1)

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