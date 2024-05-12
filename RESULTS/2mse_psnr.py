import cv2
import numpy as np

def mse_psnr(encoded_img, cover_img):
    encoded = cv2.imread(encoded_img)
    cover =   cv2.imread(cover_img)
    # Convert the images to grayscale (if necessary)
    gray_encoded = cv2.cvtColor(encoded, cv2.COLOR_BGR2GRAY)
    gray_cover = cv2.cvtColor(cover, cv2.COLOR_BGR2GRAY)

    # Calculate the Mean Squared Error (MSE)
    mse = np.mean((gray_cover - gray_encoded) ** 2)

    print(f"{cover_img}\nMSE: {mse}")

    if mse == 0:
        psnr = float('inf')
    else:
        max_pixel_value = 255.0
        psnr = 20 * np.log10(max_pixel_value / np.sqrt(mse))

    print(f"PSNR: {psnr} dB")

images_list=[('./GUI/bab.png',   './GUI/bab_ENHLSB.png'), ]

# images_list=[('baboon64base.png',   'baboon-64x64.png'), 
#              ('baboon128base.png',  'baboon-128x128.png'), 
#              ('baboon256base.png',  'baboon-256x256.png'), 
#              ('baboon512base.png',  'baboon-512x512.png'), ]

for encoded, cover in images_list:
    mse_psnr(encoded, cover)