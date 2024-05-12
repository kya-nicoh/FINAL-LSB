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
from datetime import datetime

import ast

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

NTRUdecrypt = NTRUdecrypt()
NTRUdecrypt.setNpq(N=107,p=3,q=64,df=15,dg=12,d=5)

email_from = 'workthynicoh@gmail.com'
pswd = ""

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
	root = tk.Tk()
	root.geometry('1280x720')
	root.title('canvas login test')
	root.configure(bg="#fff")
	root.resizable(False,False)

	login_frame = tk.Frame(root, bg='#fff')
	login_frame.pack()
	login_frame.pack_propagate(False)
	login_frame.configure(width=1280, height=720)

	backdrop_png = Image.open("LOGIN.png")
	backdrop_img = ImageTk.PhotoImage(backdrop_png)
	backdrop_label = tk.Label(login_frame, image=backdrop_img)
	backdrop_label.pack()
	backdrop_label.place(x=0, y=0)

	heading1 = tk.Label(login_frame, text='DIGITAL IMAGE SIGNATURE SYSTEM', fg='#5C5959', bg='white', font=('Poppins', 14))
	heading1.place(x=200,y=210)

	heading1 = tk.Label(login_frame, text='Digital Signer', fg='#3D8CBF', bg='white', font=('Poppins', 64, 'bold'))
	heading1.place(x=100,y=110)
	# TODO ADD DROP SHADOW

	# OTHER BUTTONS
	login_about_btn = tk.Button(login_frame, text="ABOUT", font=('Microsoft YaHei UI Light', 10), fg='#000000', bd=0, bg='#fff')
	login_about_btn.place(x=840, y=40)

	contact_btn = tk.Button(login_frame, text="CONTACT", font=('Microsoft YaHei UI Light', 10), fg='#000000', bd=0, bg='#79B0D3')
	contact_btn.place(x=1050, y=40)

	privacy_btn = tk.Button(login_frame, text="PRIVACY STATEMENT", font=('Microsoft YaHei UI Light', 10), fg='#000000', bd=0, bg='#79B0D3')
	privacy_btn.place(x=700, y=675)

	terms_btn = tk.Button(login_frame, text="TERMS AND SERVICES", font=('Microsoft YaHei UI Light', 10), fg='#000000', bd=0, bg='#79B0D3')
	terms_btn.place(x=900, y=675)

	manual_btn = tk.Button(login_frame, text="USER MANUAL", font=('Microsoft YaHei UI Light', 10), fg='#000000', bd=0, bg='#79B0D3')
	manual_btn.place(x=1100, y=675)

	# LOGIN PROPER ===============================================================================================================================
	login_proper_frame = Frame(login_frame, width=350, height=350, bg='#79B0D3')
	login_proper_frame.place(x=800, y=200)

	heading=Label(login_proper_frame, text="LOG IN", fg='#386F93', bg='#79B0D3', font=('Microsoft YahHei UI Light', 25, 'bold'))
	heading.place(x=25, y=5)
	# TODO ADD DROP SHADOW

	user_lbl = Label(login_proper_frame, text="Email", fg='#5C5959', bg='#79B0D3', font=("Microsoft YahHei UI Light", 9))
	user_lbl.place(x=25, y=60)

	user_png = Image.open("Email Rectangle.png")
	user_img = ImageTk.PhotoImage(user_png)
	user_label = tk.Label(login_proper_frame, image=user_img, bg='#79B0D3', width=350, height=50)
	user_label.pack()
	user_label.place(x=0, y=80)

	email = Entry(login_proper_frame, width=25, fg='black', border=0, bg='#fff', font=("Microsoft YahHei UI Light", 11))
	email.place(x=30, y=98)

	password_lbl = Label(login_proper_frame, text="Password", fg='#5C5959', bg='#79B0D3', font=("Microsoft YahHei UI Light", 9))
	password_lbl.place(x=25, y=140)

	password_png = Image.open("Email Rectangle.png")
	password_img = ImageTk.PhotoImage(password_png)
	password_label = tk.Label(login_proper_frame, image=password_img, bg='#79B0D3', width=350, height=50)
	password_label.pack()
	password_label.place(x=0, y=160)

	password = Entry(login_proper_frame, width=25, fg='black', border=0, bg='#fff', font=("Microsoft YahHei UI Light", 11), show="*")
	password.place(x=30, y=178)

	import pyrebase
	firebaseConfig = {

	}
	firebase = pyrebase.initialize_app(firebaseConfig)
	auth = firebase.auth()
	storage = firebase.storage()

	def sign_in():
		e_email = email.get()
		pswrd = password.get()
		
		try:
			user = auth.sign_in_with_email_and_password(e_email, pswrd)
			email.delete(0, 'end')
			password.delete(0, 'end')

			login_frame.pack_forget()
			sign_up_frame.pack_forget()
			ribbon_frame.pack(side=tk.TOP)
			options_frame.pack(side=tk.LEFT)
			main_frame.pack()
		except Exception as e:
			messagebox.showerror("Invalid!", "invalid username or password")

	Button(login_proper_frame, width=39, pady=7, text='Sign In', bg='#3D8CBF', fg='white', border=0, command=sign_in).place(x=35, y=250)
	# TODO ADD DROP SHADOW

	def forgot_pass():
		# make popup window then enter email
		screen = Toplevel(root, bg='#128931')
		screen.title("Forgot password")
		screen.geometry("350x350")
		screen.config(bg="white")
		screen.resizable(False, False)
		
		heading=Label(screen, text="Forgot password", fg='#000', bg='#fff', font=('Microsoft YahHei UI Light', 20))
		heading.place(x=33, y=10)

		forgot_email_lbl = Label(screen, text="Enter your remembered email address", fg='#000', bg='#fff', font=("Microsoft YahHei UI Light", 9))
		forgot_email_lbl.place(x=25, y=60)

		email_to_png = Image.open("Email Rectangle.png")
		email_to_img = ImageTk.PhotoImage(email_to_png)
		email_to_label = tk.Label(screen, image=email_to_img, bg='#fff', width=350, height=50)
		email_to_label.place(x=0, y=80)

		screen.email_to_img = email_to_img

		forgot_email = Entry(screen, width=25, fg='black', border=0, bg='#fff', font=("Microsoft YahHei UI Light", 11))
		forgot_email.place(x=30, y=98)
		
		tk.Button(screen, width=39, pady=7, text='Send', bg='#57a1f8', fg='white', border=0, command=lambda: auth.send_password_reset_email(forgot_email.get())).place(x=35, y=230)

		screen.mainloop()
		screen.destroy()

	forgot_pass_btn = Button(login_proper_frame, text="Forgot password?", fg='black', bd=0, bg='#79B0D3', font=('Microsoft YaHei UI Light', 7), 
						command=lambda: forgot_pass())
	forgot_pass_btn.place(x=245, y=210)
	

	register_btn=Button(login_proper_frame, text="Don't have an account yet?", fg='black', bd=0, bg='#79B0D3', font=('Microsoft YaHei UI Light', 7), 
						command=lambda: switch_to_sign_up())
	register_btn.place(x=115, y=290)

	# SIGNUP PROPER ===========================================================================================================================
	def switch_to_sign_up():
		login_frame.pack_forget()
		sign_up_frame.pack_forget()
		main_frame.pack_forget()
		ribbon_frame.pack_forget()
		options_frame.pack_forget()
		sign_up_frame.pack()

	sign_up_frame = tk.Frame(root, bg='#fff')
	sign_up_frame.pack()
	sign_up_frame.pack_propagate(False)
	sign_up_frame.configure(width=1280, height=720)

	sign_png = Image.open("signup.png")
	sign_img = ImageTk.PhotoImage(sign_png)
	sign_label = tk.Label(sign_up_frame, image=sign_img)
	sign_label.pack()
	sign_label.place(x=0, y=0)

	heading2 = tk.Label(sign_up_frame, text='Digital Signer', fg='#3D8CBF', bg='white', font=('Poppins', 45, 'bold'))
	heading2.place(x=120,y=20)
	# TODO ADD DROP SHADOW

	# OTHER BUTTONS
	login_about_btn = tk.Button(sign_up_frame, text="ABOUT", font=('Microsoft YaHei UI Light', 10), fg='#000000', bd=0, bg='#fff')
	login_about_btn.place(x=840, y=40)

	contact_btn = tk.Button(sign_up_frame, text="CONTACT", font=('Microsoft YaHei UI Light', 10), fg='#000000', bd=0, bg='#fff')
	contact_btn.place(x=1050, y=40)

	privacy_btn = tk.Button(sign_up_frame, text="PRIVACY STATEMENT", font=('Microsoft YaHei UI Light', 10), fg='#000000', bd=0, bg='#79B0D3')
	privacy_btn.place(x=700, y=675)

	terms_btn = tk.Button(sign_up_frame, text="TERMS AND SERVICES", font=('Microsoft YaHei UI Light', 10), fg='#000000', bd=0, bg='#79B0D3')
	terms_btn.place(x=900, y=675)

	manual_btn = tk.Button(sign_up_frame, text="USER MANUAL", font=('Microsoft YaHei UI Light', 10), fg='#000000', bd=0, bg='#79B0D3')
	manual_btn.place(x=1100, y=675)


	signup_proper_frame = Frame(sign_up_frame, width=350, height=525, bg='#fff')
	signup_proper_frame.place(x=475, y=80)

	heading=Label(signup_proper_frame, text="Registration", fg='#3D8CBF', bg='#fff', font=('Microsoft YahHei UI Light', 30, 'bold'))
	heading.place(x=50, y=5)
	# TODO ADD DROP SHADOW

	sign_user_lbl = Label(signup_proper_frame, text="Email", fg='#5C5959', bg='#fff', font=("Microsoft YahHei UI Light", 9))
	sign_user_lbl.place(x=25, y=60)
	sign_user_png = Image.open("Email Rectangle.png")
	sign_user_img = ImageTk.PhotoImage(user_png)
	sign_user_label = tk.Label(signup_proper_frame, image=user_img, bg='#fff', width=350, height=50)
	sign_user_label.pack()
	sign_user_label.place(x=0, y=80)
	sign_user = Entry(signup_proper_frame, width=25, fg='black', border=0, bg='#fff', font=("Microsoft YahHei UI Light", 11))
	sign_user.place(x=30, y=98)

	sign_first_lbl = Label(signup_proper_frame, text="First Name", fg='#5C5959', bg='#fff', font=("Microsoft YahHei UI Light", 9))
	sign_first_lbl.place(x=25, y=140)
	sign_first_png = Image.open("Email Rectangle.png")
	sign_first_img = ImageTk.PhotoImage(password_png)
	sign_first_label = tk.Label(signup_proper_frame, image=password_img, bg='#fff', width=350, height=50)
	sign_first_label.pack()
	sign_first_label.place(x=0, y=160)
	sign_first = Entry(signup_proper_frame, width=25, fg='black', border=0, bg='#fff', font=("Microsoft YahHei UI Light", 11))
	sign_first.place(x=30, y=178)

	sign_last_lbl = Label(signup_proper_frame, text="Last Name", fg='#5C5959', bg='#fff', font=("Microsoft YahHei UI Light", 9))
	sign_last_lbl.place(x=25, y=220)
	sign_last_png = Image.open("Email Rectangle.png")
	sign_last_img = ImageTk.PhotoImage(password_png)
	sign_last_label = tk.Label(signup_proper_frame, image=password_img, bg='#fff', width=350, height=50)
	sign_last_label.pack()
	sign_last_label.place(x=0, y=240)
	sign_last = Entry(signup_proper_frame, width=25, fg='black', border=0, bg='#fff', font=("Microsoft YahHei UI Light", 11))
	sign_last.place(x=30, y=258)

	sign_password_lbl = Label(signup_proper_frame, text="Password", fg='#5C5959', bg='#fff', font=("Microsoft YahHei UI Light", 9))
	sign_password_lbl.place(x=25, y=300)
	sign_password_png = Image.open("Email Rectangle.png")
	sign_password_img = ImageTk.PhotoImage(password_png)
	sign_password_label = tk.Label(signup_proper_frame, image=password_img, bg='#fff', width=350, height=50)
	sign_password_label.pack()
	sign_password_label.place(x=0, y=320)
	sign_password = Entry(signup_proper_frame, width=25, fg='black', border=0, bg='#fff', font=("Microsoft YahHei UI Light", 11), show="*")
	sign_password.place(x=30, y=338)

	sign_cpassword_lbl = Label(signup_proper_frame, text="Confirm Password", fg='#5C5959', bg='#fff', font=("Microsoft YahHei UI Light", 9))
	sign_cpassword_lbl.place(x=25, y=380)
	sign_cpassword_png = Image.open("Email Rectangle.png")
	sign_cpassword_img = ImageTk.PhotoImage(password_png)
	sign_cpassword_label = tk.Label(signup_proper_frame, image=password_img, bg='#fff', width=350, height=50)
	sign_cpassword_label.pack()
	sign_cpassword_label.place(x=0, y=400)
	sign_cpassword = Entry(signup_proper_frame, width=25, fg='black', border=0, bg='#fff', font=("Microsoft YahHei UI Light", 11), show="*")
	sign_cpassword.place(x=30, y=418)


	def sign_in_back():
		login_frame.pack()
		sign_up_frame.pack_forget()
		main_frame.pack_forget()
		ribbon_frame.pack_forget()
		options_frame.pack_forget()
		sign_up_frame.pack_forget()

	def sign_up():
		username = sign_user.get()
		f_name = sign_first.get()
		l_name = sign_last.get()
		password = sign_password.get()
		c_password = sign_cpassword.get()

		if username == '' or f_name == '' or l_name == '' or password == '' or c_password == '':
			messagebox.showerror('Invalid', 'All parameters must be filled up')
		elif password == c_password:
			try:
				user = auth.create_user_with_email_and_password(username, c_password)

				login_frame.pack()
				sign_up_frame.pack_forget()
				main_frame.pack_forget()
				ribbon_frame.pack_forget()
				options_frame.pack_forget()
				sign_up_frame.pack_forget()

				messagebox.showinfo('Sign Up', 'Successfully sign up')

			except Exception as e:
				messagebox.showerror('Invalid', 'Warning weak password')
				print(e)
		else:
			messagebox.showerror('Invalid', 'Passwords must be the same')

	Button(signup_proper_frame, width=39, pady=7, text='Sign Up', bg='#3D8CBF', fg='white', border=0, command=lambda: sign_up()).place(x=35, y=460)
	# TODO ADD DROP SHADOW
	ihaveacc = tk.Label(signup_proper_frame, text='I have an account', fg='black', bg='white', font=('Microsoft YaHei UI Light', 9))
	ihaveacc.place(x=95, y=500)

	signin= Button(signup_proper_frame, width=6, text='Sign in', border=0, bg='white', cursor='hand2', fg='#57a1f8', command=lambda: sign_in_back())
	signin.place(x=200, y=500)



# MAIN FRAME ===================================================================================================================================================

	ribbon_frame = tk.Frame(root, bg='#fff')
	ribbon_frame.pack(side=tk.TOP)
	ribbon_frame.pack_propagate(False)
	ribbon_frame.configure(width=1280, height=55)
	Frame(ribbon_frame, width=1280, height=1, bg='#AAA69D').place(x=0, y=54)
	# TODO ADD DROP SHADOW

	options_frame = tk.Frame(root, bg='#3D8CBF')
	options_frame.pack(side=tk.LEFT)
	options_frame.pack_propagate(False)
	options_frame.configure(width=200, height=720)
	
	main_frame = tk.Frame(root)
	main_frame.pack()
	main_frame.pack_propagate(False)
	main_frame.configure(width=1080, height=720)

	logout_png = Image.open("logout - icon.png")
	logout_img = ImageTk.PhotoImage(logout_png)
	logout_label = tk.Label(options_frame, image=logout_img, bg='#3D8CBF', width=30, height=35)
	logout_label.place(x=125, y=618)
	
	root.logout_img = logout_img

	logo_lbl = tk.Label(ribbon_frame, text="DIGITAL SIGNER", font=('Inria Sans', 20), fg='#696969', bd=0, bg='#fff')
	logo_lbl.place(x=60, y=10)
	logo_png = Image.open("main_logo.png")
	logo_img = ImageTk.PhotoImage(logo_png)
	logo_label = tk.Label(ribbon_frame, image=logo_img, bg='#fff', width=30, height=35)
	logo_label.pack()
	logo_label.place(x=20, y=10)

	brush_color = "black"
	brush_size = 3
	draw_history = []


	def draw(event):
		x1, y1 = (event.x - brush_size), (event.y - brush_size)
		x2, y2 = (event.x + brush_size), (event.y + brush_size)
		draw_history.append(canvas.create_rectangle(x1, y1, x1 + brush_size, y1 + brush_size, fill=brush_color, outline=brush_color))

	def change_color(color):
		global brush_color
		brush_color = color

	def change_brush_size(size):
		global brush_size
		brush_size = size

	def clear_canvas():
		canvas.delete("all")
		draw_history.clear()

	def save_as_png():
		# Create a blank image with the same size as the canvas
		img = Image.new("RGB", (canvas.winfo_width(), canvas.winfo_height()), "white")

		# Create a drawing context
		draw = ImageDraw.Draw(img)

		# Iterate through the draw_history and draw each rectangle onto the image
		for item in draw_history:
			coords = canvas.coords(item)
			x1, y1, x2, y2 = coords
			draw.rectangle([x1, y1, x2, y2], fill=brush_color, outline=brush_color)

		# Save the image as PNG
		img.save("digital_sig.png")
		print("digital_sig.png")

	def hide_indicators():
		sign_indicate.config(bg='#3D8CBF')
		verify_indicate.config(bg='#3D8CBF')
		about_indicate.config(bg='#3D8CBF')

	def indicate(lb, page):
		hide_indicators()
		lb.config(bg='#fff')
		delete_page()
		page()

	def delete_page():
		for frame in main_frame.winfo_children():
			frame.destroy()

	def sign_page():
		sign_frame = tk.Frame(main_frame, bg='#fff')
		sign_frame.pack(side=tk.LEFT)
		sign_frame.pack_propagate(False)
		sign_frame.configure(width=1080, height=720)
		
		global canvas
		canvas = tk.Canvas(sign_frame, bg="white", width=512, height=512)
		canvas.place(x=80, y=40)
		canvas.bind("<B1-Motion>", draw)

		# ----------------------------------------------------------------------------------------------------------------------
		frame = tk.Frame(sign_frame, width=350, height=500, bg ="white")
		frame.place(x=650, y=80)

		heading = tk.Label(frame, text="Sign E-Signature", fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
		heading.place(x=45, y=5)

		def on_enter(e):
			author.delete(0, 'end')

		def on_leave(e):
			cauthor=author.get()
			if cauthor == '':
				author.insert(0, 'Author')

		author = tk.Entry(frame, width=25, fg='black', border=0, bg='white', font=("Microsoft YahHei UI Light", 11))
		author.place(x=30, y=80)
		author.insert(0, 'Author')
		author.bind('<FocusIn>', on_enter)
		author.bind('<FocusOut>', on_leave)
		tk.Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)
		
		def on_enter(e):
			receiver.delete(0, 'end')

		def on_leave(e):
			creceiver=receiver.get()
			if creceiver == '':
				receiver.insert(0, 'Receiver')

		receiver = tk.Entry(frame, width=25, fg='black', border=0, bg='white', font=("Microsoft YahHei UI Light", 11))
		receiver.place(x=30, y=150)
		receiver.insert(0, 'Receiver')
		receiver.bind('<FocusIn>', on_enter)
		receiver.bind('<FocusOut>', on_leave)
		tk.Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)
		
		def on_enter(e):
			purpose.delete(0, 'end')

		def on_leave(e):
			cpurpose=purpose.get()
			if cpurpose == '':
				purpose.insert(0, 'Purpose')

		purpose = tk.Entry(frame, width=25, fg='black', border=0, bg='white', font=("Microsoft YahHei UI Light", 11))
		purpose.place(x=30, y=220)
		purpose.insert(0, 'Purpose')
		purpose.bind('<FocusIn>', on_enter)
		purpose.bind('<FocusOut>', on_leave)
		tk.Frame(frame, width=295, height=2, bg='black').place(x=25, y=247)

		def pick_date(e):
			global cal, date_window
			date_window = Toplevel()
			date_window.grab_set()
			date_window.title("Choose date of validity")
			date_window.geometry('250x220+590+370')
			date_window.resizable(False,False)

			cal = Calendar(date_window, selectmode='day', date_pattern="mm/dd/y")
			cal.place(x=0, y=0)

			submit_btn = Button(date_window, text="Select", command=grab_date)
			submit_btn.place(x=80, y=190)

		def grab_date():
			date.delete(0, END)
			date.insert(0, cal.get_date())
			date_window.destroy()

		date = Entry(frame, width=25, fg='black', border=0, bg='white', font=("Microsoft YahHei UI Light", 11))
		date.place(x=30, y=290)
		date.insert(0, 'Enter date of validity')
		date.bind("<1>", pick_date)
		Frame(frame, width=295, height=2, bg='black').place(x=25, y=317)

		def sign_only():
			if date.get().strip() == 'Enter date of validity' or author.get().strip() == 'Author' or purpose.get().strip() == 'Purpose' or receiver.get().strip() == 'Receiver':
				messagebox.showerror("Error", "Entry cannot be blank")
			else: 
				save_as_png()
				str_author = author.get()
				str_receiver = receiver.get()
				str_purpose = purpose.get()
				str_date = date.get()	

				message = str(str_author) + ',' + str(str_receiver) + ',' + str(str_purpose) + ',' + str(str_date)
					
				loc = str('D:/OLD-sawcon/New-Documents/Github/lsb-test-ntru/digital_sig.png')
				print("input_image:", loc)
				path, file = os.path.split(loc)
				# split the filename and the image extension
				filename, ext = file.split(".")
				output_image = os.path.join(path, f"{filename}_ENHLSB.{ext}")
				# encode the data into the image
				encoded_image = encode(image_name=loc, secret_data=message)
				cv2.imwrite(output_image, encoded_image)
				nplmageSuperSave = cv2.imread(output_image)

				cv2.imwrite(output_image, encoded_image)
				print("[+] Saved encoded image.")

				tk.messagebox.showinfo("E-signature Data Status", f"E-Signature of {str_author} has been successfully signed!")
				author.delete(0, tk.END)
				author.insert(0, 'Author')
				receiver.delete(0, tk.END)
				receiver.insert(0, 'Receiver')
				purpose.delete(0, tk.END)
				purpose.insert(0, 'Purpose')
				date.delete(0, tk.END)
				date.insert(0, 'Enter date of validity')
				canvas.delete("all")
				draw_history.clear()

		def sign_w_email():
			if date.get().strip() == 'Enter date of validity' or author.get().strip() == 'Author' or purpose.get().strip() == 'Purpose' or receiver.get().strip() == 'Receiver':
				messagebox.showerror("Error", "Entry cannot be blank")
			else: 
				sign_only()

				screen = Toplevel(root, bg='#128931')
				screen.title("Send via e-mail")
				screen.geometry("350x350")
				screen.config(bg="white")
				screen.resizable(False, False)
				
				heading=Label(screen, text="Sign and Send e-mail", fg='#000', bg='#fff', font=('Microsoft YahHei UI Light', 20))
				heading.place(x=33, y=10)

				user_lbl = Label(screen, text="Send e-mail to", fg='#000', bg='#fff', font=("Microsoft YahHei UI Light", 9))
				user_lbl.place(x=25, y=60)

				email_to_png = Image.open("Email Rectangle.png")
				email_to_img = ImageTk.PhotoImage(email_to_png)
				email_to_label = tk.Label(screen, image=email_to_img, bg='#fff', width=350, height=50)
				email_to_label.place(x=0, y=80)

				screen.email_to_img = email_to_img

				email_to = Entry(screen, width=25, fg='black', border=0, bg='#fff', font=("Microsoft YahHei UI Light", 11))
				email_to.place(x=30, y=98)

				
				subject_lbl = Label(screen, text="Subject", fg='#000', bg='#fff', font=("Microsoft YahHei UI Light", 9))
				subject_lbl.place(x=25, y=140)

				subject_to_png = Image.open("Email Rectangle.png")
				subject_to_img = ImageTk.PhotoImage(email_to_png)
				subject_to_label = tk.Label(screen, image=email_to_img, bg='#fff', width=350, height=50)
				subject_to_label.place(x=0, y=160)

				screen.subject_to_img = subject_to_img

				subject_to = Entry(screen, width=25, fg='black', border=0, bg='#fff', font=("Microsoft YahHei UI Light", 11))
				subject_to.place(x=30, y=178)
				
				tk.Button(screen, width=39, pady=7, text='Send', bg='#57a1f8', fg='white', border=0, command=lambda: send_emails(email_to.get(), subject_to.get(), screen)).place(x=35, y=230)

				screen.mainloop()

		def send_emails(email_to, subject, screen):
			email_to = str(email_to)
			subject = str(subject)
			# print(f'str_email: {email_to}\n str_subjecto: {subject}')
			body = f"""
				E-Signature generated and signed using the Digital Signer
			"""

			msg = MIMEMultipart()
			msg['From'] = email_from
			msg['To'] = email_to
			msg['Subject'] = subject

			msg.attach(MIMEText(body, 'plain'))

			filename = 'D:/OLD-sawcon/New-Documents/Github/lsb-test-ntru/digital_sig_ENHLSB.png'

			attachment = open(filename, 'rb')

			attachment_package = MIMEBase('application', 'octet-stream')
			attachment_package.set_payload((attachment).read())
			encoders.encode_base64(attachment_package)
			attachment_package.add_header('Content-Disposition', "attachment; filename= " + filename)
			msg.attach(attachment_package)

			text = msg.as_string()

			TIE_server = smtplib.SMTP("smtp.gmail.com", 587)
			TIE_server.starttls()
			TIE_server.login(email_from, pswd)

			TIE_server.sendmail(email_from, email_to, text)

			TIE_server.quit()
			messagebox.showinfo("Email Success", "Email has been sent!")
			screen.destroy()
			

		tk.Button(frame, width=39, pady=7, text='Sign and send via e-mail', bg='#FCCF64', fg='black', border=0, command=sign_w_email).place(x=35, y=360)
		tk.Button(frame, width=39, pady=7, text='Sign only', bg='#57a1f8', fg='white', border=0, command=sign_only).place(x=35, y=400)

		tk.Button(sign_frame, width=15, pady=5, text='Clear', bg='#FC6464', fg='white', border=0, command=clear_canvas).place(x=485, y=40)
		tk.Button(sign_frame, width=3, pady=5, text='', bg='#6485FC', fg='white', border=0, command=lambda: change_color("blue")).place(x=80, y=40)
		tk.Button(sign_frame, width=3, pady=5, text='', bg='#64FC73', fg='white', border=0, command=lambda: change_color("green")).place(x=107, y=40)
		tk.Button(sign_frame, width=3, pady=5, text='', bg='#FC6464', fg='white', border=0, command=lambda: change_color("red")).place(x=134, y=40)
		tk.Button(sign_frame, width=3, pady=5, text='', bg='#000000', fg='white', border=0, command=lambda: change_color("black")).place(x=161, y=40)


	def verify_page():
		verify_frame = tk.Frame(main_frame, bg='#fff')
		verify_frame.pack(side=tk.LEFT)
		verify_frame.pack_propagate(False)
		verify_frame.configure(width=1080, height=720)

		def verify_img():
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
				tk_stego_img = tk_stego_img.resize((512,512))
				tk_stego_img = ImageTk.PhotoImage(tk_stego_img)
				stego_img['image'] = tk_stego_img
				stego_img.configure(bg='black')
				# enter_stego_img.insert(0, filename)

				decoded_data = decode(loc)
				print(f"decoded: {decoded_data}")

				NTRUdecrypt.readPub()
				NTRUdecrypt.readPriv()

				NTRUdecrypt.decryptString(decoded_data)
				data = NTRUdecrypt.M
				
				split_data = data.split(',')
				author, receiver, purpose, date = split_data

				print("[+] Decoded data:", split_data)
				v_author.config(text = author)
				v_receiver.config(text = receiver)
				v_purpose.config(text = purpose)
				v_date.config(text = date)
				# if date is later than today then show error

				# date format %m/%d/%y
				date_obj = datetime.strptime(date, "%m/%d/%Y").date()
				today = datetime.now().date()

				if date_obj < today:
					messagebox.showerror("Signature Expired!", f"WARNING, the signature you sumitted has been expired since {date}")
				else:
					messagebox.showinfo("Signature Valid!", f"The signature you submitted is still valid until {date}")

			else: 
				messagebox.showerror("Error", "Please Select an w-sign with a digital signature")

		frame2 = Frame(verify_frame, width=350, height=500, bg ="white")
		frame2.place(x=50, y=70)

		v_heading=Label(frame2, text="Verify E-Signature", fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
		v_heading.place(x=35, y=5)
		Button(frame2, width=39, pady=7, text='Enter an e-signature', bg='#FCCF64', fg='black', border=0, command=verify_img).place(x=35, y=80)

		v_author = Label(frame2, text="Author", fg='black', border=0, bg='white', font=("Microsoft YahHei UI Light", 11))
		v_author.place(x=30, y=150)
		Frame(frame2, width=295, height=2, bg='black').place(x=25, y=177)

		v_receiver = Label(frame2, text="Receiver", fg='black', border=0, bg='white', font=("Microsoft YahHei UI Light", 11))
		v_receiver.place(x=30, y=204)
		Frame(frame2, width=295, height=2, bg='black').place(x=25, y=231)

		v_purpose = Label(frame2, text="Purpose", fg='black', border=0, bg='white', font=("Microsoft YahHei UI Light", 11))
		v_purpose.place(x=30, y=258)
		Frame(frame2, width=295, height=2, bg='black').place(x=25, y=281)

		v_date = Label(frame2, text="Date of validity", fg='black', border=0, bg='white', font=("Microsoft YahHei UI Light", 11))
		v_date.place(x=30, y=312)
		Frame(frame2, width=295, height=2, bg='black').place(x=25, y=342)

		def clear_img():
			stego_img.configure(image='')
			stego_img.configure(bg='#fff')
			v_author.config(text = 'Author')
			v_receiver.config(text = 'Receiver')
			v_purpose.config(text = 'Purpose')
			v_date.config(text = 'Date of validity')
			

		clear = Button(frame2, width=6, text='Clear', border=0, bg='white', cursor='hand2', fg='#57a1f8', command=clear_img)
		clear.place(x=150, y=360)

		stego_img = tk.Label(verify_frame, bg='#fff')
		stego_img.place(x=450, y=50)


	def about_page():
		about_frame = tk.Frame(main_frame, bg='#fff')
		about_frame.pack()
		about_frame.pack_propagate(False)
		about_frame.configure(width=1080, height=720)

		frame2 = tk.Frame(about_frame, width=950, height=500, bg ="#F3F3F3")
		frame2.pack()
		frame2.place(x=70, y=50)

		question_png = Image.open("questionmark.png")
		question_img = ImageTk.PhotoImage(question_png)
		question_label = tk.Label(frame2, image=question_img, bg='#f3f3f3')
		question_label.place(x=649, y=80)

		about_frame.question_img = question_img

		welcome_lbl = tk.Label(frame2, text="ABOUT", font=('Inria Sans', 35), fg='#3D8CBF', bd=0, bg='#F3F3F3')
		welcome_lbl.place(x=400, y=30)

		text_samp = 'Digital Image Signature is a mathematical scheme of ' \
			'\nverifying the authenticity of digital messages, in this ' \
			'\ncase an image. A sender encrypts the message using ' \
			'\ntheir public key generates a public key which is received ' \
			'\nand decrypted by the recipient using a private key.' \
			'\nThis system uses a modified least significant bit' \
			'\nalgorithm that utilizes NTRU to encrypt the secret' \
			'\nmessage, and Lorenz Chaos System to randomize' \
			'\nthe position of the secret message in the signature.' \
			# '\n' \

		lorem_lbl = tk.Label(frame2, text=text_samp, font=('Monda', 18), fg='#000', bd=0, bg='#F3F3F3', width=45)
		lorem_lbl.place(x=30, y=155)



	def logout_page():
		try:
			auth.current_user = None
			print("Logged out successfully")
			options_frame.pack_forget()
			ribbon_frame.pack_forget()
			main_frame.pack_forget()
			sign_up_frame.pack_forget()
			login_frame.pack()
		except Exception as e:
			print("Error:", e)
		

	welcome_lbl = tk.Label(options_frame, text="Welcome, Admin!", font=('Monda', 16), fg='#fff', bd=0, bg='#3D8CBF')
	welcome_lbl.place(x=20, y=20)

	sign_btn = tk.Button(options_frame, text="Sign", font=('Microsoft YaHei UI Light', 16, 'bold'), fg='#fff', bd=0, bg='#3D8CBF', command=lambda: indicate(sign_indicate, sign_page))
	sign_btn.place(x=40, y=80)
	sign_indicate = tk.Label(options_frame, text='', bg='#fff')
	sign_indicate.place(x=3, y=80, width=5, height=45)
	
	sign_page()

	verify_btn = tk.Button(options_frame, text="Verify", font=('Microsoft YaHei UI Light', 16, 'bold'), fg='#fff', bd=0, bg='#3D8CBF', command=lambda: indicate(verify_indicate, verify_page))
	verify_btn.place(x=40, y=140)
	verify_indicate = tk.Label(options_frame, text='', bg='#3D8CBF')
	verify_indicate.place(x=3, y=140, width=5, height=45)

	about_btn = tk.Button(options_frame, text="About", font=('Microsoft YaHei UI Light', 16, 'bold'), fg='#fff', bd=0, bg='#3D8CBF', command=lambda: indicate(about_indicate, about_page))
	about_btn.place(x=40, y=200)
	about_indicate = tk.Label(options_frame, text='', bg='#3D8CBF')
	about_indicate.place(x=3, y=200, width=5, height=45)

	logout_btn = tk.Button(options_frame, text="Logout", font=('Microsoft YaHei UI Light', 12, 'bold'), fg='#fff', bd=0, bg='#3D8CBF', command=lambda: indicate(logout_indicate, logout_page))
	logout_btn.place(x=40, y=620)
	logout_indicate = tk.Label(options_frame, text='', bg='#3D8CBF')
	tk.Frame(options_frame, width=200, height=2, bg='white').place(x=0, y=610)


	root.mainloop()