import pyrebase

firebaseConfig = {
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
storage = firebase.storage()

email = 'workthynicoh@gmail.com'
password = '123456'

file_img = 'D:/OLD-sawcon/New-Documents/Github/lsb-test-ntru/digital_sig_ENHLSB.png'
file_txt = 'D:/OLD-sawcon/New-Documents/Github/lsb-test-ntru/digital_sig_ENHLSB_dec.txt'

def upload_firebase():
    storage.child("digital_sig_ENHLSB.png").put("digital_sig_ENHLSB.png")
    storage.child("digital_sig_ENHLSB_dec.txt").put("digital_sig_ENHLSB_dec.txt")
    print("Uploaded successfully")

def download_firebase():
    storage.child("digital_sig_ENHLSB.png").download("digital_sig_ENHLSB.png",     "digital_sig_ENHLSB.png")
    storage.child("digital_sig_ENHLSB_dec.txt").download("digital_sig_ENHLSB_dec.txt", "digital_sig_ENHLSB_dec.txt")
    print("Downloaded successfully")

def sign_up():
    user = auth.create_user_with_email_and_password(email, password)

def login():
    try: 
        user = auth.sign_in_with_email_and_password(email, password)
        print('Login Success!')
        # go to next frame
    except Exception as e:
        print(e)

def logout():
    try:
        auth.current_user = None
        print("Logged out successfully")
    except Exception as e:
        print("Error:", e)

# sign_up()
login()
# upload_firebase()
# download_firebase()

# auth.send_email_verification(user['idToken'])

auth.send_password_reset_email(email)