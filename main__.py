import math
import cv2
import csv

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

# Example usage:
latitude = 37.7749  # San Francisco, CA
longitude = -122.4194
altitude = 0  # in meters

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

# Example usage:
x = -2691472.950584264
y = -4293610.364859572
z = 3857878.924060788

latitude, longitude, altitude = ecef_to_geodetic(x, y, z)
print(f'Geodetic coordinates: latitude={latitude}, longitude={longitude}, altitude={altitude}')

def get_image_dimensions(image_path):
    img = cv2.imread(image_path)
    height, width, _ = img.shape
    return width, height

# Example usage:
image_path = 'data-1.png'
width, height = get_image_dimensions(image_path)
print(f'Image dimensions: Width={width}, Height={height} pixels')



def calculate_center_gps(top_right_lat, top_right_lon, bottom_left_lat, bottom_left_lon):
    center_lat = (top_right_lat + bottom_left_lat) / 2
    center_lon = (top_right_lon + bottom_left_lon) / 2
    return center_lat, center_lon

# Example usage:
top_right_lat = 37.7849  # Replace with actual top-right latitude
top_right_lon = -122.3994  # Replace with actual top-right longitude
bottom_left_lat = 37.7649  # Replace with actual bottom-left latitude
bottom_left_lon = -122.4194  # Replace with actual bottom-left longitude

center_lat, center_lon = calculate_center_gps(top_right_lat, top_right_lon, bottom_left_lat, bottom_left_lon)
print(f'Center GPS coordinates: Latitude={center_lat}, Longitude={center_lon}')





#__

def haversine(lat1, lon1, lat2, lon2):
    # Calculate the Haversine distance between two GPS coordinates
    R = 6371  # Radius of the Earth in kilometers

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat / 2)*2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)*2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance

def find_nearest_city(approx_lat, approx_lon, city_csv_path):
    min_distance = float('inf')
    nearest_city = None

    with open(city_csv_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            city_lat, city_lon = float(row['Latitude']), float(row['Longitude'])
            distance = haversine(approx_lat, approx_lon, city_lat, city_lon)

            if distance < min_distance:
                min_distance = distance
                nearest_city = row

    return nearest_city

# Example usage:
approx_lat = 27.7849  # Replace with your approximated latitude
approx_lon = 88.4194  # Replace with your approximated longitude
city_csv_path = 'data.csv'  # Replace with your actual CSV file path

nearest_city = find_nearest_city(approx_lat, approx_lon, city_csv_path)
print(f'Nearest City: {nearest_city["District Name"]}')