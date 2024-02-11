import cv2
import numpy as np

def find_bright_regions(image):
    # Convert image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply threshold to identify bright regions
    _, thresh = cv2.threshold(gray_image, 200, 255, cv2.THRESH_BINARY)

    # Find contours in the thresholded image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort contours by area in decreasing order
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    # Draw contours and find centers
    sorted_centers_and_contours = []
    for contour in contours:
        # Calculate the center of the contour
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            sorted_centers_and_contours.append(((cX, cY), contour))

    return sorted_centers_and_contours

def calculate_image_center(image):
    height, width, _ = image.shape
    image_center_x = width // 2
    image_center_y = height // 2
    return image_center_x, image_center_y

def mark_image_center(image, center_x, center_y):
    cv2.drawMarker(image, (center_x, center_y), (0, 0, 255), markerType=cv2.MARKER_CROSS, markerSize=16, thickness=2)
