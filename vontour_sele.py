import cv2
import numpy as np
import math
import os

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
    center_lat = (top_right_lat + bottom_left_lat) / 2
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
    #cv2.putText(imgage, text, (cX - 320, cY - 13), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0, 255), 5)

def geodetic_to_ecef(latitude, longitude, altitude):
    # WGS84 ellipsoid parameters
    a = 6378137.0  # semi-major axis in meters
    f = 1 / 298.257223563  # flattening
    # Convert latitude and longitude to radians
    lat_rad = math.radians(latitude)
    lon_rad = math.radians(longitude)

    # Calculate N, the radius of curvature in the prime vertical
    N = a / math.sqrt(1 - f * (2 - f) * math.sin(lat_rad)**2)
    # Calculate ECEF coordinates
    x = (N + altitude) * math.cos(lat_rad) * math.cos(lon_rad)
    y = (N + altitude) * math.cos(lat_rad) * math.sin(lon_rad)
    z = (N * (1 - f**2) + altitude) * math.sin(lat_rad)
    return x, y, z


def ecef_to_geodetic(x, y, z):
    # WGS84 ellipsoid parameters
    a = 6378137.0  # semi-major axis in meters
    f = 1 / 298.257223563  # flattening
    # Calculate longitude
    lon_rad = math.atan2(y, x)
    # Calculate latitude
    p = math.sqrt(x*2 + y*2)
    lat_rad = math.atan2(z, p * (1 - f))
    # Iteratively calculate latitude using the corrected latitude
    while True:
        N = a / math.sqrt(1 - f * (2 - f) * math.sin(lat_rad)**2)
        new_lat_rad = math.atan2(z + N * f * math.sin(lat_rad), p)
        if abs(new_lat_rad - lat_rad) < 1e-10:
            break
        lat_rad = new_lat_rad

    # Calculate altitude
    alt = p / math.cos(lat_rad) - N
    # Convert latitude and longitude to degrees
    lat_deg = math.degrees(lat_rad)
    lon_deg = math.degrees(lon_rad)

    return lat_deg, lon_deg, alt
def co_ordinate_of_point_gps(center_gps_coordinate_xyz, center_coordinate_px, point_px,spatial_factor):
    x,y,z=center_gps_coordinate_xyz;
    cx_px,cy_px=center_coordinate_px;
    p,q=point_px; #where px==pixelss
    lat=float();
    lon=float();
    #sf_km=spatial_factor/(1000.0);# spatia factor in km
    dis_x=(p-cx_px)*spatial_factor;
    dis_y=(q-cy_px)*spatial_factor;
    print(dis_x,dis_y)

    final_cordinate_x=(x-dis_x);
    final_cordinate_y=(y-dis_y);
    lat,lon,alt=ecef_to_geodetic(final_cordinate_x, final_cordinate_y,z=0);
    return lat, lon, alt;





if __name__ == "__main__":
    spatial_factor=60;# 1px=60 meter
    top_right_lat = 29.6580  # Replace with actual top-right latitude
    top_right_lon = 78.4737  # Replace with actual top-right longitude
    bottom_left_lat = 27.7025  # Replace with actual bottom-left latitude
    bottom_left_lon = 75.9601  # Replace with actual bottom-left longitude
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    satellite_images_dir = os.path.join(current_dir, 'data','satellite_images')
    image_path = os.path.join(satellite_images_dir, 'snap.jpg')
    output_dir = os.path.join(current_dir, 'output','contour_results/')
    print(output_dir)

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Ensure satellite images directory exists
    os.makedirs(satellite_images_dir, exist_ok=True)


    sorted_centers_and_contours, image = find_bright_regions(image_path)
    height, width = image.shape # in pixels
    cntr_x, cntr_y=get_image_center(image);
    cntr_lat, cntr_lon=calculate_center_gps(top_right_lat, top_right_lon, bottom_left_lat, bottom_left_lon)

    # changing to xyz
    xc,yc,zc=geodetic_to_ecef(cntr_lat, cntr_lon,altitude=0);
    print(xc,yc,zc)

    


    # Print the sorted centers and corresponding contours
    for i, (center, contour) in enumerate(sorted_centers_and_contours):
        img_cpy=image.copy();
        cv2.drawContours(img_cpy, [contour], -1, (0, 255, 0), 4)
        cv2.circle(img_cpy, center, 7, (0, 255, 0), 2)
        cX,cY=center;


        text = f'RgnCntr ({cX},{cY})px'
        cv2.putText(img_cpy, text, (cX - 320, cY - 13), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0, 255), 5)
        mark_image_center(img_cpy,cntr_lat,cntr_lon);

        lat,lon,alt=co_ordinate_of_point_gps((xc,yc,zc),(cntr_x, cntr_y),center,spatial_factor);
        """
        cv2.imshow('Detected Bright Spots', img_cpy)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        """


        cv2.imwrite(f'{output_dir}{i}Bright Regions.jpg', img_cpy)
        print(lat, lon);
        
        
        print(f'Center {i}: {center}, Contour Area: {cv2.contourArea(contour)} Image size: {image.shape}')