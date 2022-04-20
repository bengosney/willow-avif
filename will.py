import os

import pillow_avif  # noqa
from willow.image import Image, UnrecognisedImageFormatError
from willow.plugins.pillow import PillowImage
from willow.registry import registry


def pillow_save_avif(image, filename, quality=50, **options):
    image.get_pillow_image().save(filename, "avif", quality=quality, **options)


registry.register_operation(PillowImage, "save_as_avif", pillow_save_avif)


from_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "from"))
to_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "tow"))

for filename in os.listdir(from_path):
    print(f"{filename}")
    with open(os.path.join(from_path, filename), "rb") as f:
        try:
            i = Image.open(f)
        except UnrecognisedImageFormatError:
            continue
        size = i.get_size()
        r = 1024 / size[0]
        new_size = (int(size[0] * r), int(size[1] * r))
        i = i.resize(new_size)

        print("saving")
        with open(os.path.join(to_path, f"{filename}.jpeg"), "wb") as f:
            i.save_as_jpeg(f)

        with open(os.path.join(to_path, f"{filename}.avif"), "wb") as f:
            i.save_as_avif(f)
