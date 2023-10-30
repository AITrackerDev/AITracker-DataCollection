import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

subject = "AI Data"
body = "Test Email"
sender = "eyetrackerdata@gmail.com"
recipients = "eyetrackercollection@gmail.com"
password = "kjio oydv zphc tkdi"

# instance of MIMEMultipart
msg = MIMEMultipart()

# storing the senders email address
msg['From'] = sender

# storing the receivers email address
msg['To'] = recipients

# storing the subject
msg['Subject'] = "Test Mail"

# string to store the body of the mail
body = "Test Email"

# attach the body with the msg instance
msg.attach(MIMEText(body, 'plain'))

# open the file to be sent
filename = "opencv_frame_0.png"
attachment = open("opencv_frame_0.png", "rb")

# instance of MIMEBase and named as p
p = MIMEBase('image', 'plain')

# To change the payload into encoded form
p.set_payload(attachment.read())

# encode into base64
encoders.encode_base64(p)

p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

# attach the instance 'p' to instance 'msg'
msg.attach(p)

# creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)

# start TLS for security
s.starttls()

# Authentication
s.login(sender, password)

# Converts the Multipart msg into a string
text = msg.as_string()

# sending the mail
s.sendmail(sender, recipients, text)

# terminating the session
s.quit()