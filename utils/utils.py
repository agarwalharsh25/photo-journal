from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError


def convert_gps_coordinates_to_degrees(value) -> float:
    degrees = value[0]
    minutes = value[1] / 60.0
    seconds = value[2] / 3600.0

    return degrees + minutes + seconds

def get_location(lat: float, lon: float):
    geolocator = Nominatim(user_agent="photo_journal")
    
    try:
        location = geolocator.reverse((lat, lon), exactly_one=True)
        if location:
            return location.address
    except (GeocoderTimedOut, GeocoderServiceError):
        pass
    
    return None
