PNG =      './HEIC/bab.png' # RGBA
EN_PNG =   './HEIC/bab_ENHLSB.png' # RGB
HEIC =     './HEIC/bab.heic'

sample_HEIC = './HEIC/sample1.heic'

from PIL import Image

def get_bit_depth(image_path):
    with Image.open(image_path) as img:
        print(f"The bit depth of the image is: {img.mode}")

get_bit_depth(PNG)