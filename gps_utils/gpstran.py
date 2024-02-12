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
