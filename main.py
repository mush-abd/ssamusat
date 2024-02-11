import cv2
import os
import image_processing.improc as ip
import gps_utils.gpstran as gpst

if __name__ == "__main__":
    ip.mark_image_center()
    gpst.convert_gps_coordinates()
    pass
