import math
import os

import pillow_avif  # noqa
from PIL import Image, UnidentifiedImageError


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)

    return f"{s} {size_name[i]}"


from_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "from"))
to_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "to"))

for filename in os.listdir(from_path):
    from_file = os.path.join(from_path, filename)
    to_file_jpeg = os.path.join(to_path, f"{filename}.jpeg")
    to_file_avif = os.path.join(to_path, f"{filename}.avif")
    # print(f"Converting {filename}")
    try:
        with Image.open(from_file) as im:
            im.thumbnail((1024, 900), Image.ANTIALIAS)
            im.save(to_file_jpeg, "jpeg", quality=70)
            im.save(to_file_avif, "avif", quality=50)
    except UnidentifiedImageError:
        continue

    before_size = convert_size(os.path.getsize(to_file_jpeg))
    after_size = convert_size(os.path.getsize(to_file_avif))
    print(f"Converted {filename} from {before_size} to {after_size}")
