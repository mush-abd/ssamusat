import cv2
import os
import image_processing.improc as ip
import gps_utils.gpstran as gpst

if __name__ == "__main__":
    spatial_factor = 60  # 1px=60 meter
    top_right_lat = 29.6580  # Replace with actual top-right latitude
    top_right_lon = 78.4737  # Replace with actual top-right longitude
    bottom_left_lat = 27.7025  # Replace with actual bottom-left latitude
    bottom_left_lon = 75.9601  # Replace with actual bottom-left longitude

    current_dir = os.path.dirname(os.path.abspath(__file__))
    satellite_images_dir = os.path.join(current_dir, 'data', 'satellite_images')
    image_path = os.path.join(satellite_images_dir, 'snap.jpg')
    output_dir = os.path.join(current_dir, 'output', 'contour_results')
    print(output_dir)

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Ensure satellite images directory exists
    os.makedirs(satellite_images_dir, exist_ok=True)

    sorted_centers_and_contours, image = ip.find_bright_regions(image_path)
    height, width = image.shape  # in pixels
    cntr_x, cntr_y = ip.get_image_center(image)
    cntr_lat, cntr_lon = ip.calculate_center_gps(top_right_lat, top_right_lon, bottom_left_lat, bottom_left_lon)

    print(cntr_lat, cntr_lon)
    # changing to xyz
    xc, yc, zc = gpst.geodetic_to_ecef(cntr_lat, cntr_lon, altitude=2000000)
    print(xc, yc, zc)

    # Print the sorted centers and corresponding contours
    for i, (center, contour) in enumerate(sorted_centers_and_contours):
        img_cpy = image.copy()
        cv2.drawContours(img_cpy, [contour], -1, (0, 255, 0), 4)
        cv2.circle(img_cpy, center, 7, (0, 255, 0), 2)
        cX, cY = center

        text = f'RgnCntr ({cX},{cY})px'
        cv2.putText(img_cpy, text, (cX - 320, cY - 13), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
        ip.mark_image_center(img_cpy, cntr_lat, cntr_lon)

        print(f'hello {center}')
        lat, lon, alt = gpst.co_ordinate_of_point_gps((xc, yc, zc), (cntr_x, cntr_y), center, spatial_factor)

        cv2.imwrite(os.path.join(output_dir, f'{i}Bright_Regions.jpg'), img_cpy)
        print(lat, lon)
        print(f'Center {i}: {center}, Contour Area: {cv2.contourArea(contour)} Image size: {image.shape}')
