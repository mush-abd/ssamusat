[1mdiff --git a/gps_utils/gpstran.py b/gps_utils/gpstran.py[m
[1mindex 196cf60..7f24f69 100644[m
[1m--- a/gps_utils/gpstran.py[m
[1m+++ b/gps_utils/gpstran.py[m
[36m@@ -74,6 +74,6 @@[m [mdef co_ordinate_of_point_gps(center_gps_coordinate_xyz, center_coordinate_px, po[m
 [m
     final_cordinate_x=(x-dis_x);[m
     final_cordinate_y=(y-dis_y);[m
[31m-    print(final_cordinate_x, final_cordinate_y)[m
[32m+[m[32m    # print(final_cordinate_x, final_cordinate_y)[m
     lat,lon,alt=ecef_to_geodetic(final_cordinate_x, final_cordinate_y,z);[m
     return lat, lon, alt;[m
[1mdiff --git a/image_processing/improc.py b/image_processing/improc.py[m
[1mindex b89c413..dd5ee89 100644[m
[1m--- a/image_processing/improc.py[m
[1m+++ b/image_processing/improc.py[m
[36m@@ -48,4 +48,6 @@[m [mdef mark_image_center(image, gps_lat, gps_lon):[m
     text = f'GPS : ({gps_lat},{gps_lon})'[m
     text2=f'Pixel Coordinates: ({center_x}, {center_y})'[m
     cv2.putText(image, text, (center_x-300, center_y-100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 0), 5, cv2.LINE_AA)[m
[31m-    cv2.putText(image, text2, (center_x-300, center_y-40), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 0), 5, cv2.LINE_AA)[m
\ No newline at end of file[m
[32m+[m[32m    cv2.putText(image, text2, (center_x-300, center_y-40), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 0), 5, cv2.LINE_AA)[m
[32m+[m
[32m+[m[32mdef get_image_center_gps()[m
\ No newline at end of file[m
[1mdiff --git a/main.py b/main.py[m
[1mindex 9585965..f3c0df3 100644[m
[1m--- a/main.py[m
[1m+++ b/main.py[m
[36m@@ -31,9 +31,12 @@[m [mif __name__ == "__main__":[m
     # changing to xyz[m
     xc, yc, zc = gpst.geodetic_to_ecef(cntr_lat, cntr_lon, altitude=2000000)[m
     print(xc, yc, zc)[m
[31m-[m
[32m+[m[32m    # x = 0[m
     # Print the sorted centers and corresponding contours[m
     for i, (center, contour) in enumerate(sorted_centers_and_contours):[m
[32m+[m[32m        # x += 1[m
[32m+[m[32m        if cv2.contourArea(contour) < 4000:[m
[32m+[m[32m            break[m
         img_cpy = image.copy()[m
         cv2.drawContours(img_cpy, [contour], -1, (0, 255, 0), 4)[m
         cv2.circle(img_cpy, center, 7, (0, 255, 0), 2)[m
[36m@@ -43,9 +46,13 @@[m [mif __name__ == "__main__":[m
         cv2.putText(img_cpy, text, (cX - 320, cY - 13), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)[m
         ip.mark_image_center(img_cpy, cntr_lat, cntr_lon)[m
 [m
[31m-        print(f'hello {center}')[m
[32m+[m[32m        # print(f'hello {center}')[m
         lat, lon, alt = gpst.co_ordinate_of_point_gps((xc, yc, zc), (cntr_x, cntr_y), center, spatial_factor)[m
 [m
         cv2.imwrite(os.path.join(output_dir, f'{i}Bright_Regions.jpg'), img_cpy)[m
         print(lat, lon)[m
         print(f'Center {i}: {center}, Contour Area: {cv2.contourArea(contour)} Image size: {image.shape}')[m
[32m+[m
[32m+[m[32m        # if x == 5:[m
[32m+[m[32m        #     break[m
[41m+[m
