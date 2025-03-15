from PIL import Image, ExifTags
import base64
from io import BytesIO
import utils.utils as utils
from typing import Optional, Dict, Any

def load_image(image_path) -> Optional[Image.Image]:
    try:
        return Image.open(image_path)

    except Exception as e:
        print(f"Error loading image: {e}")
        return None
    
def preprocess_image(image: Image.Image, max_size: int = 1600) -> Image.Image:
    img = image.copy()

    if img.mode != "RGB":
        img = img.convert("RGB")

    width, height = img.size
    if width > max_size or height > max_size:
        aspect_ratio = width / height

        if width > height:
            new_width = max_size
            new_height = int(max_size / aspect_ratio)
        else:
            new_height = max_size
            new_width = int(max_size * aspect_ratio)

        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    return img

def convert_image_to_base64(image: Image.Image) -> str:
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    
    return img_str

def extract_image_metadata(image: Image.Image) -> Dict[str, str]:
    image_metadata = {}
    
    try:
        exif_data = image._getexif()
        if not exif_data:
            return image_metadata

        for tag, value in exif_data.items():
            tag_name = ExifTags.TAGS.get(tag, tag)
            
            if tag_name == "DateTimeOriginal":
                image_metadata["date_time"] = value

            elif tag_name == "GPSInfo":
                gps_info = {}
                for sub_tag, sub_value in value.items():
                    sub_tag_name = ExifTags.GPSTAGS.get(sub_tag, sub_tag)
                    gps_info[sub_tag_name] = sub_value

                gps_latitude = gps_info.get("GPSLatitude")
                gps_latitude_ref = gps_info.get("GPSLatitudeRef")
                gps_longitude = gps_info.get("GPSLongitude")
                gps_longitude_ref = gps_info.get("GPSLongitudeRef")

                if not all([gps_latitude, gps_latitude_ref, gps_longitude, gps_longitude_ref]):
                    return image_metadata

                latitude = utils.convert_gps_coordinates_to_degrees(gps_latitude)
                if gps_latitude_ref == "S":
                    latitude = -latitude
                longitude = utils.convert_gps_coordinates_to_degrees(gps_longitude)
                if gps_longitude_ref == "W":
                    longitude = -longitude

                location = utils.get_location(latitude, longitude)
                if location:
                    image_metadata["location"] = location

    except Exception as e:
        print(f"Error extracting EXIF data: {e}")
    
    return image_metadata
