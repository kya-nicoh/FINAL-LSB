import cv2
import numpy as np
import os

from scipy.integrate import solve_ivp

from NTRU.NTRUencrypt import NTRUencrypt
from NTRU.NTRUdecrypt import NTRUdecrypt
from NTRU.NTRUutil import *

NTRUdecrypt = NTRUdecrypt()
NTRUdecrypt.setNpq(N=107,p=3,q=64,df=15,dg=12,d=5)

if os.path.exists("key.pub"):
	print("Private Key Exists")
else:
	print("Private key does not exist..\nGenerating Public and Private Keys")
	NTRUdecrypt.genPubPriv()
	
NTRUdecrypt.readPub()
NTRUdecrypt.readPriv()
NTRUencrypt = NTRUencrypt()

global pix_loc_xy

def to_bin(data):
	"""Convert `data` to binary format as string"""
	if isinstance(data, str):
		return ''.join([ format(ord(i), "08b") for i in data ])
	elif isinstance(data, bytes) or isinstance(data, np.ndarray):
		return [ format(i, "08b") for i in data ]
	elif isinstance(data, int) or isinstance(data, np.uint8):
		return format(data, "08b")
	else:
		raise TypeError("Type not supported.")


# LORENZ GENERATOR -> Generate (size of image nums total of pix) without duplicates
def lorenz_chaos_system(t, xyz, sigma=10, rho=28, beta=8/3):
	x, y, z = xyz
	dxdt = sigma * (y - x)
	dydt = x * (rho - z) - y
	dzdt = x * y - beta * z
	return [dxdt, dydt, dzdt]

# width of pic
def lorenz_integration(image_name, height, width):
	## Solve the Lorenz system
	initial_conditions = [1.0, 1.0, 1.0]

	t_span = (0, 100)
	t_eval = np.linspace(*t_span, num=10000)
	sol = solve_ivp(lorenz_chaos_system, t_span, initial_conditions, t_eval=t_eval)

	# Use the solution as seeds for generating random numbers
	random_seeds = sol.y[:, ::100].flatten()  # Extract every 100th value
	np.random.seed(int(random_seeds[0]))

	## Generate random integers within a specified range (size of the image) - 3
	lower_bound = 0
	# TODO 512 - 3 (Change this to depend on the size of the image)
	upper_bound_x = width - 3
	upper_bound_y = height - 3
	
	global pix_loc_xy
	pix_loc_xy = [(x, y) for x in range(0, upper_bound_x) for y in range(0, upper_bound_y)]
	random.shuffle(pix_loc_xy)

	file_name = image_name.replace('.png', "") + "_ENHLSB_dec.txt"
	with open(file_name, "w") as file: 
		for item in pix_loc_xy: file.write(f"{item[0]}, {item[1]}\n")


def encode(image_name, secret_data):
	NTRUencrypt.readPub()
	NTRUencrypt.setM([1,-1,0,0,0,0,0,1,-1])
	NTRUencrypt.encrypt()

	print(f"data before: {secret_data}")
	NTRUencrypt.encryptString(secret_data)
	NTRU_secret_data = NTRUencrypt.Me
	# print(f"DATA Entered: {NTRU_secret_data}")

	# ==========================
	# NTRUdecrypt.decryptString(NTRU_secret_data)
	# decoded_data = NTRUdecrypt.M
	# print("[+] Decoded data:", decoded_data)
	# ==========================

	# read the image
	image = cv2.imread(image_name)
	# maximum bytes to encode
	n_bytes = image.shape[0] * image.shape[1] * 3 // 8
	print("[*] Maximum bytes to encode:", n_bytes)
	if len(NTRU_secret_data) > n_bytes:
		raise ValueError("[!] Insufficient bytes, need bigger image or less data.")
	print("[*] Encoding data...")
	# add stopping criteria
	NTRU_secret_data += "====="
	print(f"secret data: {NTRU_secret_data}")
	data_index = 0
	# convert data to binary
	binary_secret_data = to_bin(NTRU_secret_data)
	# size of data to hide
	data_len = len(binary_secret_data)
	print(f'Data about to encode: {data_len}')
	
	height, width, channels = image.shape
	lorenz_integration(image_name, height, width)
	
	binary_data = ""

	pixel_count = 0
	for x, y in pix_loc_xy:
		pixel = image[x, y]
		# convert RGB values to binary format
		r, g, b = to_bin(pixel)
		# modify the least significant bit only if there is still data to store
		if data_index < data_len:
			# least significant red pixel bit
			pixel[0] = int(r[:-1] + binary_secret_data[data_index], 2)
			binary_data += binary_secret_data[data_index]
			data_index += 1
		if data_index < data_len:
			# least significant green pixel bit
			pixel[1] = int(g[:-1] + binary_secret_data[data_index], 2)
			binary_data += binary_secret_data[data_index]
			data_index += 1
		if data_index < data_len:
			# least significant blue pixel bit
			pixel[2] = int(b[:-1] + binary_secret_data[data_index], 2)
			binary_data += binary_secret_data[data_index]
			data_index += 1

		# print(f'pixel #{pixel_count} ({x},{y}): \t{pixel}')
		pixel_count+=1
		# if data is encoded, just break out of the loop
		if data_index >= data_len:
			print('Data Encoded, skip this pixel')
			break
	
	extracted_data = ""
	pixel_count = 0
	for x, y in pix_loc_xy:
		pixel = image[x, y]
		# print(f'pixel #{pixel_count} ({x},{y}): \t{pixel}')
		pixel_count+=1
		r, g, b = to_bin(pixel)
		extracted_data += r[-1]
		extracted_data += g[-1]
		extracted_data += b[-1]

	secret_all_bytes = [ binary_secret_data[i: i+8] for i in range(0, len(binary_secret_data), 8) ]
	all_bytes = [ binary_data[i: i+8] for i in range(0, len(binary_data), 8) ]

	extracted_bytes = [ extracted_data[i: i+8] for i in range(0, len(extracted_data), 8) ]
	# print(f"actual :   {secret_all_bytes}")
	# print(f"encoded:   {all_bytes}")
	# print(f"extracted: {extracted_bytes}")

	# convert from bits to characters
	decoded_data = ""
	for byte in extracted_bytes:
		decoded_data += chr(int(byte, 2))
		if decoded_data[-5:] == "=====":
			break
	# print(f"decoded: {decoded_data[:-5]}")
	return image

def decode(image_name):
	print("[+] Decoding...")
	# read the image
	image = cv2.imread(image_name)
	binary_data = ""

	pix_loc_xy = []
	file_name = image_name.replace('.png', "") + "_dec.txt"
	with open(file_name, "r") as file:
		for line in file:
			values = line.strip().split(',')
			pix_loc_xy.append((int(values[0]), int(values[1])))

	for x, y in pix_loc_xy:
		pixel = image[x, y]
		# print(f'pixel ({x},{y}): \t{pixel}')
		r, g, b = to_bin(pixel)
		binary_data += r[-1]
		binary_data += g[-1]
		binary_data += b[-1]

	# print(binary_data)
	# split by 8-bits
	all_bytes = [ binary_data[i: i+8] for i in range(0, len(binary_data), 8) ]
	# convert from bits to characters
	decoded_data = ""
	for byte in all_bytes:
		decoded_data += chr(int(byte, 2))
		# print(decoded_data)
		if decoded_data[-5:] == "=====":
			break
	return decoded_data[:-5]

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description="Steganography encoder/decoder, this Python scripts encode data within images.")
	parser.add_argument("-t", "--text", help="The text data to encode into the image, this only should be specified for encoding")
	parser.add_argument("-e", "--encode", help="Encode the following image")
	parser.add_argument("-d", "--decode", help="Decode the following image")
	parser.add_argument("-G", "--genpubpriv", help="Generate a new Public and Private Key", action="store_true")
	
	args = parser.parse_args()
	secret_data = args.text
	if args.genpubpriv:
		NTRUdecrypt.genPubPriv()
	if args.encode:
		# if the encode argument is specified
		import time
		start_time = time.time()

		input_image = args.encode
		print("input_image:", input_image)
		# split the absolute path and the file
		path, file = os.path.split(input_image)
		# split the filename and the image extension
		filename, ext = file.split(".")
		output_image = os.path.join(path, f"{filename}_ENHLSB.{ext}")
		# encode the data into the image
		encoded_image = encode(image_name=input_image, secret_data=secret_data)
		# save the output image (encoded image)
		cv2.imwrite(output_image, encoded_image)
		print("[+] Saved encoded image.")

		end_time = time.time()
		elapsed_time = end_time - start_time
		print("Elapsed time:", elapsed_time, "seconds")
	if args.decode:
		input_image = args.decode
		
		# decode the secret data from the image
		decoded_data = decode(input_image)
		print(f"decoded: {decoded_data}")

		NTRUdecrypt.readPub()
		NTRUdecrypt.readPriv()

		NTRUdecrypt.decryptString(decoded_data)
		data = NTRUdecrypt.M

		print("[+] Decoded data:", data)
		