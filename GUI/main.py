import tkinter as tk
from tkinter import *
from tkinter import filedialog, ttk
from PIL import ImageTk, Image

root = Tk()
root.title('Modified Least Significant Bit Algorithm')
root.geometry("450x650")
root.resizable(0, 0)
root.configure(background="#2F4155")

# Create a notebook
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# Create frames for each page
frame1 = tk.Frame(notebook, bg="#2F4155")
frame2 = tk.Frame(notebook, bg="#2F4155")

notebook.add(frame1, text='Signing')
notebook.add(frame2, text='Verifying')

# SIGNING
mdf_LSB = tk.Label(frame1, text='Modified LSB Image Signing', padx=30, pady=20, font=('Roboto',20), bg="#2F4155", fg = "white")
mdf_LSB.grid(row=0, column=0, padx=15, pady=10, columnspan="2")

SECRET_MESSAGE_STR = tk.StringVar()
IMAGE_LOC_STR = tk.StringVar()

lbl_secret_msg      = tk.Label(frame1, text='Enter Secret Message:', padx=20, pady=20, font=('Roboto',12), bg="#2F4155", fg = "white")
lbl_signing_status  = tk.Label(frame1, text='Signing Status:', padx=20, pady=20,  font=('Roboto',12), bg="#2F4155", fg = "white")
lbl_empty_status    = tk.Label(frame1, padx=20, pady=20, font=('Roboto',12), bg="#2F4155", fg = "white")
show_pic            = tk.Label(frame1, bg='#2F4155')
enter_secret_msg    = tk.Entry(frame1, font=('Roboto', 12), textvariable=SECRET_MESSAGE_STR)
enter_secret_msg.place(width=150,height=150) 


def selectPic():
    global tk_img
    global filename
    filename = filedialog.askopenfilename(initialdir="/images", title="Select Image",
                           filetypes=(("png images","*.png"),("jpg images","*.jpg"), ("bmp images","*.bmp")))
    tk_img = Image.open(filename)
    tk_img = tk_img.resize((200,200))
    tk_img = ImageTk.PhotoImage(tk_img)
    show_pic['image'] = tk_img
    # save filename
    
btn_browse = tk.Button(frame1, text='Select Image', bg='grey', fg='#ffffff', font=('Roboto',12), command=selectPic)

def print_message():
    message = SECRET_MESSAGE_STR.get()
    message = str(message)
    global filename
    loc = str(filename)
    print("Location", loc)
    print("Secret Message", message)

btn_embed = tk.Button(frame1, text='Sign the image', bg='green', fg='#ffffff', font=('Roboto',12), command=print_message)

lbl_secret_msg.grid(row=1, column=0, sticky=W)
enter_secret_msg.grid(row=1, column=1, padx=(0,20), columnspan="2", sticky=W)

btn_browse.grid(row=2, column=0, padx=10, pady=10, columnspan="2")

show_pic.grid(row=3, column=0, columnspan="2", rowspan="2", padx=10, pady=10)
btn_embed.grid(row=5, column=0, columnspan="2", padx=10, pady=10)

lbl_signing_status.grid(row=6, column = 0)
lbl_empty_status.grid(row=7, column = 0, columnspan="2")




# --------------------------------------------------------------------------------------------------------------------------




# VERIFYING
mdf_LSB = tk.Label(frame2, text='Modified LSB Image Verification', padx=20, pady=20, font=('Roboto',20), bg="#2F4155", fg = "white")
mdf_LSB.grid(row=0, column=0, padx=15, pady=10, columnspan="2")

VER_IMAGE_LOC_STR = tk.StringVar()

lbl_ver_status = tk.Label(frame2, text='Verification Status:', padx=20, pady=20,  font=('Roboto',12), bg="#2F4155", fg = "white")
lbl_ver_output = tk.Label(frame2, padx=20, pady=20, font=('Roboto',12), bg="#2F4155", fg = "white", wraplength=300)
show_stego_img = tk.Label(frame2, bg='#2F4155')
enter_stego_img = tk.Entry(frame2, font=('Roboto', 12), textvariable=VER_IMAGE_LOC_STR)

def verify_secret():
    global tk_stego_img
    filename = filedialog.askopenfilename(initialdir="/images", title="Select Image",
                           filetypes=(("png images","*.png"),("jpg images","*.jpg"), ("bmp images","*.bmp")))
    tk_stego_img = Image.open(filename)
    tk_stego_img = tk_stego_img.resize((200,200))
    tk_stego_img = ImageTk.PhotoImage(tk_stego_img)
    show_stego_img['image'] = tk_stego_img
    enter_stego_img.insert(0, filename)

btn_stego_browse = tk.Button(frame2, text='Select Stego Image', bg='grey', fg='#ffffff', font=('Roboto',12), command=verify_secret)

def ver_output():
    worked = "IT WORKED Bas;fo asji;sa kjfs;lksjad f;asofikjspf osiaj fspaf oiafjs;fokjfepoi awjfl;wokj fwa;lfk j;lITCH"
    lbl_ver_output.config(text = worked)

btn_ver_stego = tk.Button(frame2, text='Verifiy Stego Image', bg='green', fg='#ffffff', font=('Roboto',12), command=ver_output)

btn_stego_browse.grid(row=1, column=0, padx=10, pady=10, columnspan="2")
# enter_stego_img.grid(row=1, column=1, padx=(0,20), sticky=W)
show_stego_img.grid(row=2, column=0, columnspan="2", rowspan="2", padx=10, pady=10)

btn_ver_stego.grid(row=4, column=0, padx=10, pady=10, columnspan="2")

lbl_ver_status.grid(row=5, column=0, columnspan="2")
lbl_ver_output.grid(row=6, column=0, columnspan="2")


root.mainloop()