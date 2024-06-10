import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
import image_processing.improc as ip
import gps_utils.gpstran as gpst
import geopandas as gpd
import gps_utils.shape as shape
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

if __name__ == "__main__":
    spatial_factor = 30  # 1px=60 meter
    top_right_lat = 27.6283  # Replace with actual top-right latitude
    top_right_lon = 81.1576  # Replace with actual top-right longitude
    bottom_left_lat = 25.4026  # Replace with actual bottom-left latitude
    bottom_left_lon = 79.1869  # Replace with actual bottom-left longitude


    current_dir = os.path.dirname(os.path.abspath(__file__))
    satellite_images_dir = os.path.join(current_dir, 'data', 'satellite_images')
    image_path = os.path.join(satellite_images_dir, 'snap8.jpg')
    shape_path = os.path.join(current_dir, 'data', 'district_shapefiles', 'shapefiles')
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

    # changing to xyz
    xc, yc, zc = gpst.geodetic_to_ecef(cntr_lat, cntr_lon, altitude=0)
    print(f'ECEF Coordinates: {xc, yc, zc}')
    # x = 0

    shapefile_data = gpd.read_file(os.path.join(shape_path, 'india_dist.shp'))

    nearest_district = shapefile_data[shapefile_data.DISTRICT == 'Kanpur Nagar']
    print(nearest_district)

    # Print the sorted centers and corresponding contours
    lat_lon = []
    x = 0
    for i, (center, contour) in enumerate(sorted_centers_and_contours):
        x += 1
        # if cv2.contourArea(contour) < 10000:
        #     break
        img_cpy = image.copy()
        img_cpy_original = image.copy()

        cv2.drawContours(img_cpy, [contour], -1, (0, 255, 0), 4)
        cv2.circle(img_cpy, center, 7, (0, 255, 0), 2)
        cX, cY = center

        text = f'RgnCntr ({cX},{cY})px'
        cv2.putText(img_cpy, text, (cX - 320, cY - 13), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
        ip.mark_image_center(img_cpy, cntr_lat, cntr_lon)
        
        shapefile_data[shapefile_data.DISTRICT == 'Aligarh'].boundary.plot()
        plt.axis('off')
        x_lim = plt.xlim()
        y_lim = plt.ylim()
        # print(x_lim)
        # print(y_lim)

        # to overlap the contour with satellite image
        bg_x_lim = [bottom_left_lon, top_right_lon]
        bg_y_lim = [bottom_left_lat, top_right_lat]
        imbg = Image.open(r'D:\Projects\ssamusat\data\satellite_images\snap7.jpg')
        imfg = Image.open(r'D:\Projects\ssamusat\data\district_shapefiles\district_boundary_images\Aligarh.png')
        imbg_width, imbg_height = imbg.size
        print(f'Background image size : {imbg_width, imbg_height}')
        print(bg_x_lim[1] - bg_x_lim[0], (bg_y_lim[1]- bg_y_lim[0]))
        dppx, dppy = ((bg_x_lim[1] - bg_x_lim[0])/imbg_width), ((bg_y_lim[1]- bg_y_lim[0])/imbg_height)
        print(dppx, dppy)
        imfg_width = int((x_lim[1] - x_lim[0])/dppx)
        print(f'Foreground width: {imfg_width}')
        imfg_height = int((y_lim[1] - y_lim[0])/dppy)
        print(f'Foreground height: {imfg_height}')
        imfg_resized = imfg.resize((imfg_width, imfg_height), Image.LANCZOS)
        imbg.paste(imfg_resized, (2790 - int(imfg_width/2), 1570 - int(imfg_height/2)) , imfg_resized)
        imbg.save("overlay.png")

        image_ = cv2.imread('overlay.png')
        crop = image_[1570 - int(imfg_height/2): 1570 + int(imfg_height/2), 2790 - int(imfg_width/2): 2790 + int(imfg_width/2)]
        cv2.imwrite('overlay_cropped.png', crop)

        snap_resize = cv2.imread('D:\Projects\ssamusat\data\satellite_images\snap7.jpg')
        crop = snap_resize[1570 - int(imfg_height/2): 1570 + int(imfg_height/2), 2790 - int(imfg_width/2): 2790 + int(imfg_width/2)]
        cv2.imwrite('snap_resize.png', crop)

        image1 = Image.open(r'snap_resize.png')
        image2 = Image.open(r'D:\Projects\ssamusat\data\district_shapefiles\district_black_white\Aligarh.png')
        width, height = image1.size
        print(f'Binary image size: {width, height}')
        image2 = image2.resize((width, height), Image.LANCZOS)
        image2.save('aligarh_binary_resized.png')

        # perform biwise and to superimpose
        image1 = cv2.imread('aligarh_binary_resized.png')
        image2 = cv2.imread('snap_resize.png')
        bitwise__ = cv2.bitwise_and(image2, image1)
        cv2.imwrite("Aligarh_Bitwise.png", bitwise__)

        # Mask the image to only include pixels within the contour
        mask = np.zeros_like(image)
        cv2.drawContours(mask, [contour], -1, (255, 255, 255), -1)
        masked_image = cv2.bitwise_and(image, mask)

        # Extract gray levels from the masked image
        gray_pixels = masked_image[mask != 0]

        # Plot histogram
        hist, bins = np.histogram(gray_pixels, bins=256, range=[0, 256])
        plt.plot(hist, color='black')
        plt.xlabel('Pixel Intensity')
        plt.ylabel('Frequency')
        plt.title('Histogram of Gray Level Pixels within Contour')

        # Find the total number of pixels within the contour
        total_pixels_within_contour = cv2.countNonZero(mask)
        plt.annotate(f'Total Pixels: {total_pixels_within_contour}', xy=(0.05, 0.95), xycoords='axes fraction', fontsize=12, color='red')
        plt.show()


        # image_bitwise = cv2.imread('Aligarh_Bitwise.png', cv2.IMREAD_GRAYSCALE)
        # new_mask = np.zeros_like(image_bitwise)
        # gray_pixels = image_bitwise[new_mask != 0]

        # # Plot histogram
        # # plt.rcParams['figure.facecolor'] = 'white'
        # hist, bins = np.histogram(gray_pixels, bins=256, range=[0, 256])
        # # plt.axis('on')
        # plt.plot(hist, color='black')
        # plt.xlabel('Pixel Intensity')
        # plt.ylabel('Frequency')
        # plt.title('Histogram of Gray Level Pixels within Contour')

        # # Find the total number of pixels within the contour
        # total_pixels_within_contour = cv2.countNonZero(new_mask)
        # plt.annotate(f'Total Pixels: {total_pixels_within_contour}', xy=(0.05, 0.95), xycoords='axes fraction', fontsize=12, color='red')
        # plt.show()


        lat, lon, alt = gpst.co_ordinate_of_point_gps((xc, yc, zc), (cntr_x, cntr_y), center, spatial_factor)

        cv2.imwrite(os.path.join(output_dir, f'{i}Bright_Regions.jpg'), img_cpy)
        # print(lat, lon)
        lat_lon.append([lat, lon])
        print(f'Center {i}: {center}, Contour Area: {cv2.contourArea(contour)} Image size: {image.shape}')
        if x > 1:
            break

print(f'Coordinates of the center of the contour, {lat_lon[0]}')
print(f'Coordinates of the center of the district, {nearest_district.cen_y, nearest_district.cen_x}')



