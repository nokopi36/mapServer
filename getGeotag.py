from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import os


# 度分秒から10進数表記の緯度経度に変換
def get_decimal_from_dms(dms, ref):
    degrees = dms[0]
    minutes = dms[1] / 60.0
    seconds = dms[2] / 3600.0

    if ref in ["S", "W"]:
        degrees = -degrees
        minutes = -minutes
        seconds = -seconds

    return degrees + minutes + seconds


def get_and_save_all_images_exif(folder):
    for filename in os.listdir(folder):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            full_path = os.path.join(folder, filename)
            try:
                image = Image.open(full_path)
                image.verify()
                exif = image._getexif()

                if not exif:
                    print(f"No EXIF metadata found for {filename}")
                    continue

                geotags = {}
                for idx, tag in TAGS.items():
                    if tag == "GPSInfo":
                        if idx not in exif:
                            print(f"No EXIF geotagging found for {filename}")
                            continue

                        for key, val in GPSTAGS.items():
                            if key in exif[idx]:
                                geotags[val] = exif[idx][key]

                lat = get_decimal_from_dms(
                    geotags["GPSLatitude"], geotags["GPSLatitudeRef"]
                )
                lon = get_decimal_from_dms(
                    geotags["GPSLongitude"], geotags["GPSLongitudeRef"]
                )
                formatted_lat = "{:.6f}".format(lat)
                formatted_lon = "{:.6f}".format(lon)

                txt_filename = os.path.splitext(full_path)[0] + ".txt"
                with open(txt_filename, "w") as f:
                    f.write(f"{formatted_lat} {formatted_lon}\n")
            except Exception as e:
                print(f"Error processing {filename}: {e}")
