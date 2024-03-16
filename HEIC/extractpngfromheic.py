o_HEIC = './HEIC/output.heic'

import pillow_heif
from PIL import Image
import cv2
import numpy as np

heif_file = pillow_heif.open_heif(o_HEIC, convert_hdr_to_8bit=False, bgr_mode=True)
np_array = np.asarray(heif_file[1])
cv2.imwrite("./HEIC/output.png", np_array)