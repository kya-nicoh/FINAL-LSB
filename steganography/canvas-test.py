import tkinter as tk
from tkinter import *
from tkinter import filedialog, ttk, messagebox
from PIL import ImageTk, Image, ImageDraw
from tkcalendar import *
import os

root = tk.Tk()
root.geometry('1280x720')
root.title('canvas test')
root.configure(bg="#fff")
root.resizable(False,False)

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
			# encoded_image = encode(image_name=loc, secret_data=message)
			# cv2.imwrite(output_image, encoded_image)
			# nplmageSuperSave = cv2.imread(output_image)

			# cv2.imwrite(output_image, encoded_image)
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
		# if date.get().strip() == 'Enter date of validity' or author.get().strip() == 'Author' or purpose.get().strip() == 'Purpose' or receiver.get().strip() == 'Receiver':
		# 	messagebox.showerror("Error", "Entry cannot be blank")
		# else: 
		sign_only()

		# open email then attach the image
		loc = str('D:/OLD-sawcon/New-Documents/Github/lsb-test-ntru/digital_sig.png')
		
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
		
		emailto = email_to.get()
		subjectto = subject_to.get()

		tk.Button(screen, width=39, pady=7, text='Send', bg='#57a1f8', fg='white', border=0, command=lambda: send_email(emailto, subjectto)).place(x=35, y=230)


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
    pass

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