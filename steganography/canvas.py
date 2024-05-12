import tkinter as tk
from tkinter import *
from tkinter import filedialog, ttk, messagebox
from PIL import ImageTk, Image, ImageDraw
from tkcalendar import *
import os
import ast

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
    'apiKey': "AIzaSyBfKm-l21pCn85T-kRiX5Y30ElO4ONpVmQ",
    'authDomain': "digitalsigner-e32f1.firebaseapp.com",
    'databaseURL': "https://digitalsigner-e32f1-default-rtdb.asia-southeast1.firebasedatabase.app",
    'projectId': "digitalsigner-e32f1",
    'storageBucket': "digitalsigner-e32f1.appspot.com",
    'messagingSenderId': "858934402648",
    'appId': "1:858934402648:web:b32d0449b689563044342d",
    'serviceAccount': 'serviceAccount.json'
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
	canvas = tk.Canvas(sign_frame, bg="white", width=512, height=600)
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

	def sign_w_email():
		if date.get().strip() == 'Enter date of validity' or author.get().strip() == 'Author' or purpose.get().strip() == 'Purpose' or receiver.get().strip() == 'Receiver':
			messagebox.showerror("Error", "Entry cannot be blank")
		else: 
			save_as_png()
			str_author = author.get()
			str_receiver = receiver.get()
			str_purpose = purpose.get()
			str_date = date.get()	

			message = str(str_author) + ',' + str(str_date)
				
			# loc = str('D:/OLD-sawcon/New-Documents/Github/lsb-test-ntru/digital_sig.png')
			# print("input_image:", loc)
			# path, file = os.path.split(loc)
			# # split the filename and the image extension
			# filename, ext = file.split(".")
			# output_image = os.path.join(path, f"{filename}_ENHLSB.{ext}")
			# # encode the data into the image
			# encoded_image = encode(image_name=loc, secret_data=message)
			# cv2.imwrite(output_image, encoded_image)
			# nplmageSuperSave = cv2.imread(output_image)

			# cv2.imwrite(output_image, encoded_image)
			# print("[+] Saved encoded image.")

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

	tk.Button(frame, width=39, pady=7, text='Sign and send via e-mail', bg='#FCCF64', fg='black', border=0, command=sign_w_email).place(x=35, y=360)
	tk.Button(frame, width=39, pady=7, text='Sign only', bg='#57a1f8', fg='white', border=0, command=sign_w_email).place(x=35, y=400)

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

			# decoded_data = decode(loc)
			# print(f"decoded: {decoded_data}")

			# NTRUdecrypt.readPub()
			# NTRUdecrypt.readPriv()

			# NTRUdecrypt.decryptString(decoded_data)
			# data = NTRUdecrypt.M
			
			# split_data = data.split(',')
			# author, receiver, purpose, date = split_data

			# print("[+] Decoded data:", split_data)
			# v_author.config(text = author)
			# v_receiver.config(text = receiver)
			# v_purpose.config(text = purpose)
			# v_date.config(text = date)
			# if date is later than today then show error
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
		v_author.config(text = '')
		v_receiver.config(text = '')
		v_purpose.config(text = '')
		v_date.config(text = '')
		

	clear = Button(frame2, width=6, text='Clear', border=0, bg='white', cursor='hand2', fg='#57a1f8', command=clear_img)
	clear.place(x=150, y=360)

	stego_img = tk.Label(verify_frame, bg='#fff')
	stego_img.place(x=450, y=50)


def about_page():
	about_frame = tk.Frame(main_frame, bg='#fff')
	about_frame.pack()
	about_frame.pack_propagate(False)
	about_frame.configure(width=1080, height=720)

	frame2 = Frame(about_frame, width=950, height=500, bg ="white")
	frame2.place(x=70, y=50)

	question_png = Image.open("questionmark.png")
	question_img = ImageTk.PhotoImage(question_png)
	question_label = tk.Label(frame2, image=question_img)
	question_label.place(x=0, y=120)

	about_png = Image.open("about.png")
	about_img = ImageTk.PhotoImage(about_png)
	about_label = tk.Label(frame2, image=about_img)
	about_label.place(x=0, y=0)



def logout_page():
	options_frame.pack_forget()
	ribbon_frame.pack_forget()
	main_frame.pack_forget()
	login_frame.pack()

welcome_lbl = tk.Label(options_frame, text="Welcome, Nicoh", font=('Monda', 16), fg='#fff', bd=0, bg='#3D8CBF')
welcome_lbl.place(x=20, y=20)

sign_btn = tk.Button(options_frame, text="Sign", font=('Microsoft YaHei UI Light', 16, 'bold'), fg='#fff', bd=0, bg='#3D8CBF', command=lambda: indicate(sign_indicate, sign_page))
sign_btn.place(x=40, y=80)
sign_indicate = tk.Label(options_frame, text='', bg='#3D8CBF')
sign_indicate.place(x=3, y=80, width=5, height=45)

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