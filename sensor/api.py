import os
import sys
root = os.getcwd()
pwd = os.path.dirname(os.path.realpath("."))
sys.path.insert(0, root)
import time
from firebase import firebase
import config

FB = firebase.FirebaseApplication(config.FIREBASE_URL, None)


def confirm_open():
    max_wait_time = 2
    # Thời điểm bắt đầu
    start_time = time.time()
    # khoi tao action
    action = None

    while time.time() - start_time < max_wait_time:
        action = get_data()
        if action == "damocua" :
            break
    if action == "damocua":
        return action
    else : return "error"

def confirm_close():
    max_wait_time = 2
    # Thời điểm bắt đầu
    start_time = time.time()
    # khoi tao action
    action = None

    while time.time() - start_time < max_wait_time:
        action = get_data()
        if action == "dadongcua" :
            break
    if action == "dadongcua":
        return action
    else : return "error"

def mocua():

    if confirm_close() == "dadongcua":
        push_data(data="mocua")
    
    return confirm_open()

def dongcua():

    if confirm_open() == "damocua":
        push_data(data="dongcua")

    return confirm_close()

def push_data(data):

    url = '/'
    name = '/action'
    result = FB.put(url,name, data)
    return result
def get_data():
    url = '/'
    name = '/action'
    result = FB.get(url, name)
    return result
if __name__ == "__main__":  
    # push_data(data = "mocua")
    # print(get_data())
    
    print(mocua())