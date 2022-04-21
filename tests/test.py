import math
import os

from willow.image import Image, UnrecognisedImageFormatError

import willowavif  # noqa


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
    with open(os.path.join(from_path, filename), "rb") as f:
        try:
            i = Image.open(f)
        except UnrecognisedImageFormatError:
            continue
        size = i.get_size()
        r = 1024 / size[0]
        new_size = (int(size[0] * r), int(size[1] * r))
        i = i.resize(new_size)

        out_jpeg = os.path.join(to_path, f"{filename}.jpeg")
        out_avif = os.path.join(to_path, f"{filename}.avif")

        with open(out_jpeg, "wb") as f:
            i.save_as_jpeg(f)

        with open(out_avif, "wb") as f:
            i.save_as_avif(f)

        jpeg_size = convert_size(os.path.getsize(out_jpeg))
        avif_size = convert_size(os.path.getsize(out_avif))
        print(f"Converted {filename} from {jpeg_size} to {avif_size}")
