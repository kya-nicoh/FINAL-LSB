import cv2
import numpy as np
import os
import pillow_heif
from PIL import Image
from scipy.integrate import solve_ivp
from NTRU.NTRUencrypt import NTRUencrypt
from NTRU.NTRUdecrypt import NTRUdecrypt
from NTRU.NTRUutil import *

import tkinter as tk
from tkinter import *
from tkinter import filedialog, ttk, messagebox
from PIL import ImageTk, Image, ImageDraw
from tkcalendar import *

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

def lorenz_integration(image_name, height, width):
	## Lorenz system
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

		# Randomized Embedding
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
		# LORENZ PRINT ME
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
		cv2.imwrite(output_image, encoded_image)
		nplmageSuperSave = cv2.imread(output_image)
		end_time = time.time()
		elapsed_time = end_time - start_time
		
        # HEIC
		# output_image_heic = os.path.join(path, f"{filename}.heic")
		# def_HEIC = './HEIC/sample1.heic'
		# if pillow_heif.is_supported(def_HEIC):
		# 	heif_file = pillow_heif.open_heif(def_HEIC)
		# # heif_file = pillow_heif.from_pillow(Image.open(input_image))

		# heif_file.add_from_pillow(Image.open(output_image))
		# heif_file.save(output_image_heic, quality=-1)
		# heif_file = pillow_heif.open_heif(output_image_heic, convert_hdr_to_8bit=False, bgr_mode=True)
		# npImageSuperSave = np.asarray(heif_file[1])
		cv2.imwrite(output_image, nplmageSuperSave)

		# save the output image
		cv2.imwrite(output_image, encoded_image)
		print("[+] Saved encoded image.")

        # HEIC
		# print("number of images in file:", len(heif_file))
		# for img in heif_file:
		# 	print(img)
		
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


	root = Tk()
	root.title('Modified Least Significant Bit Algorithm')
	root.geometry("1200x900")
	root.resizable(0, 0)
	root.configure(background="#2F4155")

    # Create a notebook
	notebook = ttk.Notebook(root)
	notebook.pack(fill='both', expand=True)
	
	# Create frames for each page
	frame1 = tk.Frame(notebook, bg="#2F4155")
	frame2 = tk.Frame(notebook, bg="#2F4155")
	
	notebook.add(frame1, text='PATIENT RECORD Encoding')
	notebook.add(frame2, text='XRAY Verifying')
	
	mdf_LSB = tk.Label(frame1, text='PATIENT RECORD', padx=10, font=('Roboto',20), bg="#2F4155", fg = "white")
	mdf_LSB.grid(row=0, column=0, padx=0, pady=5, columnspan="10", sticky=W)
	# lbl_empty_status    = tk.Label(frame1, padx=20, pady=20, font=('Roboto',12), bg="#2F4155", fg = "white", wraplength=300)
	
	
	lbl_name    = tk.Label(frame1, text='Name:', padx=0, pady=0, font=('Roboto',12), bg="#2F4155", fg = "white")
	lbl_age  	= tk.Label(frame1, text='Age:', padx=0, pady=0,  font=('Roboto',12), bg="#2F4155", fg = "white")
	lbl_sex  	= tk.Label(frame1, text='Sex:', padx=0, pady=0,  font=('Roboto',12), bg="#2F4155", fg = "white")
	lbl_xray_id = tk.Label(frame1, text='X-RAY #:', padx=0, pady=0,  font=('Roboto',12), bg="#2F4155", fg = "white")
	lbl_com  	= tk.Label(frame1, text='Company:', padx=0, pady=0,  font=('Roboto',12), bg="#2F4155", fg = "white")

	etr_name = tk.StringVar()
	etr_age = tk.StringVar()
	etr_sex = tk.StringVar()
	etr_xray = tk.StringVar()
	etr_com = tk.StringVar()

	enter_name = tk.Entry(frame1, font=('Roboto', 12), textvariable=etr_name)
	enter_name.place(width=150,height=150) 
	enter_age = tk.Entry(frame1, font=('Roboto', 12), textvariable=etr_age)
	enter_age.place(width=150,height=150) 
	enter_sex = tk.Entry(frame1, font=('Roboto', 12), textvariable=etr_sex)
	enter_sex.place(width=150,height=150) 
	enter_xray_id = tk.Entry(frame1, font=('Roboto', 12), textvariable=etr_xray)
	enter_xray_id.place(width=150,height=150) 
	enter_com = tk.Entry(frame1, font=('Roboto', 12), textvariable=etr_com)
	enter_com.place(width=150,height=150) 

	show_pic            = tk.Label(frame1, bg='#2F4155')

	tk_blank_pic 		= Image.open('D:/OLD-sawcon/New-Documents/Github/lsb-test-ntru/GUI/blank.png')
	tk_blank_pic 		= tk_blank_pic.resize((800,800))
	tk_blank_pic = ImageTk.PhotoImage(tk_blank_pic)
	show_pic['image']  = tk_blank_pic

	def selectPic():
		global tk_img
		global tk_filename
		tk_filename = filedialog.askopenfilename(initialdir="/images", title="Select Image",
							filetypes=(("png images","*.png"),("jpg images","*.jpg"), ("bmp images","*.bmp")))
		tk_img = Image.open(tk_filename)
		tk_img = tk_img.resize((800,800))
		tk_img = ImageTk.PhotoImage(tk_img)
		show_pic['image'] = tk_img
		# save filename
		
	btn_browse = tk.Button(frame1, text='Select XRAY Image', bg='grey', fg='#ffffff', font=('Roboto',12), command=selectPic)

	def print_message():
		global tk_filename
		print(f"tk_filename: {tk_filename}")
		if etr_name.get().strip() == "" or etr_age.get().strip() == "" or etr_sex.get().strip() == "" or etr_xray.get().strip() == "" or etr_com.get().strip() == "":
			messagebox.showerror("Error", "Entry cannot be blank")
		elif tk_filename == "":
			messagebox.showerror("Error", "Select an XRAY image to embedd")
		else:
			str_name = etr_name.get()
			str_age = etr_age.get()
			str_sex = etr_sex.get()
			str_xray_id = etr_xray.get()
			str_com = etr_com.get()

			message = str(str_name) + ',' + str(str_age) + ',' + str(str_sex) + ',' + str(str_xray_id) + ',' + str(str_com)

			loc = str(tk_filename)

			print("input_image:", loc)
			# split the absolute path and the file
			path, file = os.path.split(loc)
			# split the filename and the image extension
			filename, ext = file.split(".")
			output_image = os.path.join(path, f"{filename}_ENHLSB.{ext}")
			# encode the data into the image
			encoded_image = encode(image_name=tk_filename, secret_data=message)
			cv2.imwrite(output_image, encoded_image)
			nplmageSuperSave = cv2.imread(output_image)

			# HEIC
			# output_image_heic = os.path.join(path, f"{filename}.heic")
			# def_HEIC = './HEIC/sample1.heic'
			# if pillow_heif.is_supported(def_HEIC):
			# 	heif_file = pillow_heif.open_heif(def_HEIC)
			# # heif_file = pillow_heif.from_pillow(Image.open(input_image))

			# heif_file.add_from_pillow(Image.open(output_image))
			# heif_file.save(output_image_heic, quality=-1)
			# heif_file = pillow_heif.open_heif(output_image_heic, convert_hdr_to_8bit=False, bgr_mode=True)
			# npImageSuperSave = np.asarray(heif_file[1])
			# cv2.imwrite(output_image, nplmageSuperSave)

			# HEIC
			# print("number of images in file:", len(heif_file))
			# for img in heif_file:
			# 	print(img)

			cv2.imwrite(output_image, encoded_image)
			print("[+] Saved encoded image.")

			messagebox.showinfo("Patient Data Status", f"Patient data of {etr_name.get()} has been encoded successfully")
			enter_name.delete(0, tk.END)
			enter_age.delete(0, tk.END)
			enter_sex.delete(0, tk.END)
			enter_xray_id.delete(0, tk.END)
			enter_com.delete(0, tk.END)
			tk_blank_pic 		= Image.open('D:/OLD-sawcon/New-Documents/Github/lsb-test-ntru/GUI/blank.png')
			tk_blank_pic 		= tk_blank_pic.resize((800,800))
			tk_blank_pic = ImageTk.PhotoImage(tk_blank_pic)
			show_pic['image']  = tk_blank_pic

	btn_embed = tk.Button(frame1, text='ENCODE patient data', bg='green', fg='#ffffff', font=('Roboto',12), command=print_message)



	show_pic.grid		(row=1, column=3, columnspan="20", rowspan="20", padx=10, pady=10)

	lbl_name.grid		(row=1, column=0, sticky=W, padx=10)
	enter_name.grid		(row=1, column=1, padx=(5,20), sticky=E)
	lbl_age.grid		(row=2, column=0, sticky=W, padx=10)
	enter_age.grid		(row=2, column=1, padx=(5,20), sticky=E)
	lbl_sex.grid		(row=3, column=0, sticky=W, padx=10)
	enter_sex.grid		(row=3, column=1, padx=(5,20), sticky=E)
	lbl_xray_id.grid	(row=4, column=0, sticky=W, padx=10)
	enter_xray_id.grid	(row=4, column=1, padx=(5,20), sticky=E)
	lbl_com.grid		(row=5, column=0, sticky=W, padx=10)
	enter_com.grid		(row=5, column=1, padx=(5,20), sticky=E)

	btn_browse.grid		(row=6, column=0, padx=10, pady=10, columnspan="1", sticky=E)
	btn_embed.grid		(row=6, column=1, columnspan="1", padx=10, pady=10, sticky=E)














	# ======================================================================================================

	mdf_LSB = tk.Label(frame2, text='X-RAY PATIENT RECORD', padx=10, font=('Roboto',20), bg="#2F4155", fg = "white")
	mdf_LSB.grid(row=0, column=0, padx=0, pady=5, columnspan="2")

	# VER_IMAGE_LOC_STR = tk.StringVar()

	# lbl_ver_status = tk.Label(frame2, text='Verification Status:', padx=20, pady=20,  font=('Roboto',12), bg="#2F4155", fg = "white")
	# lbl_ver_output = tk.Label(frame2, padx=20, pady=20, font=('Roboto',12), bg="#2F4155", fg = "white", wraplength=300)
	# enter_stego_img = tk.Entry(frame2, font=('Roboto', 12), textvariable=VER_IMAGE_LOC_STR)

	show_stego_img = tk.Label(frame2, bg='#2F4155')
	tk_blank_pic 		= Image.open('D:/OLD-sawcon/New-Documents/Github/lsb-test-ntru/GUI/blank.png')
	tk_blank_pic 		= tk_blank_pic.resize((800,800))
	tk_blank_pic = ImageTk.PhotoImage(tk_blank_pic)
	show_stego_img['image']  = tk_blank_pic

	f2_lbl_name    	= tk.Label(frame2, text='NAME:', padx=0, font=('Roboto',12), bg="#2F4155", fg = "white")
	f2_lbl_name_o = tk.Label(frame2, padx=0, font=('Roboto',12), bg="#2F4155", fg = "white")
	f2_lbl_age  	= tk.Label(frame2, text='Age:', padx=0,  font=('Roboto',12), bg="#2F4155", fg = "white")
	f2_lbl_age_o = tk.Label(frame2, padx=0, font=('Roboto',12), bg="#2F4155", fg = "white")
	f2_lbl_sex  	= tk.Label(frame2, text='Sex:', padx=0,  font=('Roboto',12), bg="#2F4155", fg = "white")
	f2_lbl_sex_o = tk.Label(frame2, padx=0, font=('Roboto',12), bg="#2F4155", fg = "white")
	f2_lbl_xray_id 	= tk.Label(frame2, text='X-RAY #:', padx=0,  font=('Roboto',12), bg="#2F4155", fg = "white")
	f2_lbl_xray_id_o = tk.Label(frame2, padx=0, font=('Roboto',12), bg="#2F4155", fg = "white")
	f2_lbl_com  	= tk.Label(frame2, text='Company:', padx=0,  font=('Roboto',12), bg="#2F4155", fg = "white")
	f2_lbl_com_o = tk.Label(frame2, padx=0, font=('Roboto',12), bg="#2F4155", fg = "white")

	def verify_secret():
		global tk_stego_img
		global tk_stego_filename
		tk_stego_filename = filedialog.askopenfilename(initialdir="/images", title="Select Image",
							filetypes=(("png images","*.png"),("jpg images","*.jpg"), ("bmp images","*.bmp")))

		# decode the secret data from the image
		loc = str(tk_stego_filename)
		print(f"loc: {loc}")

		file_name = loc.replace('.png', "") + "_dec.txt"
		
		if os.path.exists(file_name):
			tk_stego_img = Image.open(tk_stego_filename)
			tk_stego_img = tk_stego_img.resize((800,800))
			tk_stego_img = ImageTk.PhotoImage(tk_stego_img)
			show_stego_img['image'] = tk_stego_img
			# enter_stego_img.insert(0, filename)

			decoded_data = decode(loc)
			print(f"decoded: {decoded_data}")

			NTRUdecrypt.readPub()
			NTRUdecrypt.readPriv()

			NTRUdecrypt.decryptString(decoded_data)
			data = NTRUdecrypt.M
			
			split_data = data.split(',')
			name, age, sex, xray_id, com = split_data

			print("[+] Decoded data:", split_data)
			f2_lbl_name_o.config(text = name)
			f2_lbl_age_o.config(text = age)
			f2_lbl_sex_o.config(text = sex)
			f2_lbl_xray_id_o.config(text = xray_id)
			f2_lbl_com_o.config(text = com)
		else: 
			messagebox.showerror("Error", "Please Select an XRAY with a PATIENT Record")


	btn_stego_browse = tk.Button(frame2, text='Select XRAY Image', bg='grey', fg='#ffffff', font=('Roboto',12), command=verify_secret)

	# def ver_output():
	# 	global tk_stego_filename
	# 	# decode the secret data from the image
	# 	loc = str(tk_stego_filename)
	# 	print(f"loc: {loc}")
	# 	decoded_data = decode(loc)
	# 	print(f"decoded: {decoded_data}")

	# 	NTRUdecrypt.readPub()
	# 	NTRUdecrypt.readPriv()

	# 	NTRUdecrypt.decryptString(decoded_data)
	# 	data = NTRUdecrypt.M
		
	# 	split_data = data.split(',')
	# 	name, age, sex, xray_id, com = split_data

	# 	print("[+] Decoded data:", split_data)
	# 	# lbl_ver_output.config(text = name)

	# btn_ver_stego = tk.Button(frame2, text='Verifiy Stego Image', bg='green', fg='#ffffff', font=('Roboto',12), command=ver_output)


	# btn_ver_stego.grid(row=1, column=10, padx=10, pady=10, columnspan="2")
	show_stego_img.grid(row=1, column=0, columnspan="20", rowspan="20", padx=10, pady=10)
	
	
	btn_stego_browse.grid(row=1, column=20, padx=0, pady=10, columnspan="2")

	f2_lbl_name.grid(row=2, column=20, padx=10, sticky=W)
	f2_lbl_name_o.grid(row=2, column=21, columnspan="2", padx=10, sticky=W)

	f2_lbl_age.grid(row=3, column=20, padx=10, sticky=W)
	f2_lbl_age_o.grid(row=3, column=21, padx=10, sticky=W)

	f2_lbl_sex.grid(row=4, column=20, padx=10, sticky=W)
	f2_lbl_sex_o.grid(row=4, column=21, padx=10, sticky=W)

	f2_lbl_xray_id.grid(row=5, column=20, padx=10, sticky=W)
	f2_lbl_xray_id_o.grid(row=5, column=21, padx=10, sticky=W)

	f2_lbl_com.grid(row=6, column=20, padx=10, sticky=W)
	f2_lbl_com_o.grid(row=6, column=21, padx=10, sticky=W)
	
	root.mainloop()