import cv2
import matplotlib.pyplot as plt



def grayscale(image_name):
    # Load the image
    image_gray = cv2.imread(image_name, cv2.IMREAD_GRAYSCALE)
    # Calculate the histogram
    histogram = cv2.calcHist([image_gray], [0], None, [256], [0, 256])
    # Plot the histogram
    plt.figure()
    plt.title(image_name.replace('.png', ""))
    plt.xlabel("Pixel Value")
    plt.ylabel("Frequency")
    plt.plot(histogram, color='black')
    plt.xlim([0, 256])
    plt.show()

def rgb(image_name):
    # Load the image
    image = cv2.imread(image_name)
    # Convert the image to RGB (if it's in BGR format)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Split the image into its channels
    r, g, b = cv2.split(image_rgb)
    # Calculate the histograms for each channel
    hist_r = cv2.calcHist([r], [0], None, [256], [0, 256])
    hist_g = cv2.calcHist([g], [0], None, [256], [0, 256])
    hist_b = cv2.calcHist([b], [0], None, [256], [0, 256])

    # Plot the histograms
    plt.figure()
    plt.title(image_name.replace('.png', ""))
    plt.xlabel("Bins")
    plt.ylabel("# of Pixels")
    plt.plot(hist_r, color='red', label='Red')
    plt.plot(hist_g, color='green', label='Green')
    plt.plot(hist_b, color='blue', label='Blue')
    plt.xlim([0, 256])
    plt.legend()
    plt.show()

# images_list=['baboon-64x64.png',   'baboon-64x64_ENHLSB.png', 
#              'baboon-128x128.png', 'baboon-128x128_ENHLSB.png', 
#              'baboon-256x256.png', 'baboon-256x256_ENHLSB.png', 
#              'baboon-512x512.png', 'baboon-512x512_ENHLSB.png', ]

# images_list=['lena64base.png',   'lena-64x64_ENHLSB.png', 
#              'lena128base.png', 'lena-128x128_ENHLSB.png', 
#              'lena256base.png', 'lena-256x256_ENHLSB.png', 
#              'lena512base.png', 'lena-512x512_ENHLSB.png', ]
    
images_list=['baboon64base.png',   'baboon-64x64_ENHLSB.png', ]

for images in images_list:
    # grayscale(images)
    rgb(images)