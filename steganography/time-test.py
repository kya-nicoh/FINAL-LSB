import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

email_from = 'workthynicoh@gmail.com'
email_to = 'gabbnicoh@gmail.com'

pswd = "avqbabcgtunegszc"

def send_emails(email_to, subject):
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


send_emails(email_to, 'test')



# import webbrowser
# import os

# def compose_email(recipient_email, subject, message_body, image_path):
#     # Prepare mailto URL
#     mailto_url = f"mailto:{recipient_email}?subject={subject}&body={message_body}"

#     # If image path provided, add it as an attachment
#     if image_path and os.path.exists(image_path):
#         print('image found')
#         mailto_url += f"&attachment=file://{os.path.abspath(image_path)}"

#     # Open the default email client
#     webbrowser.open(mailto_url)

# # Example usage
# recipient_email = 'gabbnicoh@gmail.com'
# subject = 'Test Email with Image Attachment'
# message_body = 'This email contains an image attachment.'
# image_path = 'D:/OLD-sawcon/New-Documents/Github/lsb-test-ntru/digital_sig_ENHLSB.png'

# compose_email(recipient_email, subject, message_body, image_path)
