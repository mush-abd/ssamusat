
import cv2
import os
font_size=4;
font_thickness=4;
def calculate_gps_from_pixel(center_gps, spatial_factor, pixel_displacement):
    center_lat, center_lon = center_gps
    lat_per_pixel = spatial_factor * 0.00001
    lon_per_pixel = spatial_factor * 0.00002 

    displacement_x, displacement_y = pixel_displacement

    new_lat = center_lat + displacement_y * lat_per_pixel
    new_lon = center_lon + displacement_x * lon_per_pixel

    return new_lat, new_lon

def detect_bright_spots(image_path, center_gps, spatial_factor, threshold_value=175, min_contour_area=50):
    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding
    _, binary_image = cv2.threshold(gray_image, threshold_value, 255, cv2.THRESH_BINARY)
   
    # Find contours
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter the contours based on minimum contour area
    filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area]
    
    
    
    # Calculate the total area of all detected bright spots in square pixels
    total_area_px = sum(cv2.contourArea(contour) for contour in filtered_contours)

    # Lists to store the areas of detected bright spots in square pixels
    bright_spot_areas_px = []

    # Calculate the area of each bright spot (circle) separately and print it on the image
    for i, contour in enumerate(filtered_contours):
        (x, y), radius = cv2.minEnclosingCircle(contour)

        center = (int(x), int(y))
        radius = int(radius)

        #cv2.putText(image, str(radius), (int(x) - 30, int(y) + radius + 15),
                        #cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0, 255), 4)
        if(radius>=30):
            cv2.circle(image, center, radius, (0, 255, 0), 10)  # Green circle

        # Calculate the area in square pixels
        area_px = cv2.contourArea(contour)
        bright_spot_areas_px.append(area_px)  # Add the area in square pixels to the list

        # Calculate the area in square kilometers using the spatial factor
        area_km2 = (area_px * (spatial_factor ** 2)) / 1000000.0  # Convert to square kilometers
        if(area_km2>=60):
            area_text = f"Area: {area_km2:.2f} sq. km"
            cv2.putText(image, area_text, (int(x) - 30, int(y) + radius + 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 4)  # Cyan-colored text for area in sq. km
        
       
    # Calculate the total area of detected bright spots in square kilometers
    total_area_km2 = (total_area_px * (spatial_factor ** 2)) / 1000000.0  # Convert to square kilometers
    total_area_text = f"Total Bright Spot Area: {total_area_km2:.2f} sq. km"
    cv2.putText(image, total_area_text, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 4)
    
    

    # Calculate the center coordinates of the image
    center_x, center_y = image.shape[1] // 2, image.shape[0] // 2
    # Draw a green circle at the center and annotate it with GPS
    cv2.circle(image, (center_x, center_y), 10, (0, 255, 255), font_thickness)
    center_annotation = f"Center GPS: {center_gps[0]:.6f}, {center_gps[1]:.6f}"
    cv2.putText(image, center_annotation, (center_x - 100, center_y - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), font_thickness)


    # Calculate the GPS coordinates of the center of the circle
    pixel_displacement = (int(x) - gray_image.shape[1] // 2, int(y) - gray_image.shape[0] // 2)
    gps_lat, gps_lon = calculate_gps_from_pixel(center_gps, spatial_factor, pixel_displacement)
    
    gps_text = f"GPS: {gps_lat:.6}, {gps_lon:.6f}"
    cv2.putText(image, gps_text, (int(x) - 30, int(y) + radius + 35),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), font_thickness)  # Print GPS coordinates on the image
    """       

    """
    return image

if __name__ == "__main__":
    center_gps = (28.68, 77.215)  # Example center GPS coordinates 
    spatial_factor = 250  # Adjust the spatial factor as needed 1pxel=30 meter
    x=detect_bright_spots("/home/bytebender/Desktop/Projects/ssamusat/data/snap.jpg", center_gps, spatial_factor)
    cv2.imwrite("/home/bytebender/out.jpg",x);

"""    
    for k in range(16, 19):   
        image_path = f"C:\\Users\\One-Exploit's\\Desktop\\1 Projects\\amu_sat\\sat_img\\sat{k}.png"
        processed_image = detect_bright_spots(image_path, center_gps, spatial_factor)
        output_path = f"C:\\Users\\One-Exploit's\\Desktop\\1 Projects\\amu_sat\\sat_out\\sat{k}.png"
        cv2.imwrite(output_path, processed_image)
"""



