import math

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

def convert_gps_coordinates(gps_center_xyz, image_center_px, point_px, spatial_factor):
    x, y, z = gps_center_xyz
    cx_px, cy_px = image_center_px
    p, q = point_px

    dis_x = (p - cx_px) * spatial_factor
    dis_y = (q - cy_px) * spatial_factor

    final_cordinate_x = (x - dis_x)
    final_cordinate_y = (y - dis_y)
    lat, lon, alt = ecef_to_geodetic(final_cordinate_x, final_cordinate_y, z=0)

    return lat, lon, alt
