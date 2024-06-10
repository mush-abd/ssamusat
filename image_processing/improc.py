import cv2
import numpy as np

def find_bright_regions(image_path):
    # Read the image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Apply threshold to identify bright regions
    _, thresh = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY)

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


    return (sorted_centers_and_contours,image);

def get_image_center(image):
    height, width = image.shape
    center_x = width // 2
    center_y = height // 2
    return center_x, center_y


def calculate_center_gps(top_right_lat, top_right_lon, bottom_left_lat, bottom_left_lon):
    center_lat = (top_right_lat + bottom_left_lat) / 2 #approximate
    center_lon = (top_right_lon + bottom_left_lon) / 2
    return center_lat, center_lon


def mark_image_center(image, gps_lat, gps_lon):
    height, width= image.shape
    center_x = width // 2
    center_y = height // 2
    cv2.drawMarker(image, (center_x, center_y), (0, 0, 255), markerType=cv2.MARKER_CROSS, markerSize=16, thickness=2)
    text = f'GPS : ({gps_lat},{gps_lon})'
    text2=f'Pixel Coordinates: ({center_x}, {center_y})'
    cv2.putText(image, text, (center_x-300, center_y-100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 0), 5, cv2.LINE_AA)
    cv2.putText(image, text2, (center_x-300, center_y-40), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 0), 5, cv2.LINE_AA)


