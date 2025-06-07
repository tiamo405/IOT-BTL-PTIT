import os
import sys
root = os.getcwd()
pwd = os.path.dirname(os.path.realpath("."))
sys.path.insert(0, root)
import time
import firebase_admin
from firebase_admin import credentials, db
import config

# Khởi tạo Firebase app
if not firebase_admin._apps:
    cred = credentials.Certificate(config.FIREBASE_CERT)
    firebase_admin.initialize_app(cred, {
        'databaseURL': config.FIREBASE_DB_URL
    })

def push_data(data):
    ref = db.reference("/action")
    ref.set(data)

def get_data():
    ref = db.reference("/action")
    return ref.get()

def confirm_open():
    max_wait_time = 2
    start_time = time.time()
    action = None

    while time.time() - start_time < max_wait_time:
        action = get_data()
        if action == "damocua":
            break
    return action if action == "damocua" else "error"

def confirm_close():
    max_wait_time = 2
    start_time = time.time()
    action = None

    while time.time() - start_time < max_wait_time:
        action = get_data()
        if action == "dadongcua":
            break
    return action if action == "dadongcua" else "error"

def mocua():
    if confirm_close() == "dadongcua":
        push_data("mocua")
    return confirm_open()

def dongcua():
    if confirm_open() == "damocua":
        push_data("dongcua")
    return confirm_close()

if __name__ == "__main__":
    print(mocua())
    # print(dongcua())
