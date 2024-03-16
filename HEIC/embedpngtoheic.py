PNG =      './HEIC/bab.png' # RGBA
EN_PNG =   './HEIC/bab_ENHLSB.png' # RGB
HEIC =     './HEIC/bab.heic'

sample_HEIC = './HEIC/sample1.heic'

import pillow_heif
from PIL import Image
import cv2
import numpy as np
# if already made HEIC
if pillow_heif.is_supported(sample_HEIC):
    heif_file = pillow_heif.open_heif(sample_HEIC)

# if making from scratch
# heif_file = pillow_heif.from_pillow(Image.open(PNG))

heif_file.add_from_pillow(Image.open(EN_PNG))

heif_file.save("./HEIC/output.heic", quality=-1)

# regular extract from heic to png 
heif_file = pillow_heif.open_heif("./HEIC/output.heic", convert_hdr_to_8bit=False, bgr_mode=True)
npImageSuperSave = np.asarray(heif_file[1])
cv2.imwrite("./HEIC/output.png", npImageSuperSave)

# get png then change name (save to different folder then easily retrieve)
nplmageSuperSave = cv2.imread(EN_PNG)
cv2.imwrite("./HEIC/output.png", nplmageSuperSave)

print("number of images in file:", len(heif_file))
for img in heif_file:
    print(img)
