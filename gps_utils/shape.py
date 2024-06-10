# import geopandas as gpd
import numpy as np
from math import sqrt

def find_nearest_district(shapefile_data, cen_X, cen_Y):

    nearest_district = shapefile_data.DISTRICT[1]
    print(nearest_district)
    nearest_X, nearest_Y = shapefile_data.cen_x[1], shapefile_data.cen_y[1]
    nearest_distance = sqrt((nearest_X - cen_X)**2 + (nearest_Y - cen_Y)**2)
    print(f'nearest {nearest_distance}')
    for i in range(len(shapefile_data['DISTRICT'])):
            new_distance = sqrt((shapefile_data.cen_x[i] - cen_X)**2 + ((shapefile_data.cen_y[i])- cen_Y)**2)
            if new_distance < nearest_distance:
                nearest_X = cen_X
                nearest_Y = cen_Y
                nearest_district = shapefile_data.DISTRICT[i]
                print(f'{i}, {nearest_district}')
                nearest_distance = new_distance
                print(f'{i}, {nearest_distance}')

    print(nearest_X, nearest_Y, nearest_district)      