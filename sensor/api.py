import time
import cv2
from firebase import firebase
def mocua():

    print("Da mo cua")

def dongcua():
    print("Da dong cua")

def push_data(data):
    fb = firebase.FirebaseApplication('https://iot-ptit-61e0e-default-rtdb.firebaseio.com/', None)
    new_uesr = '/test'
    action = '/action'
    result = fb.put(new_uesr,action, data)
    print(result)
if __name__ == "__main__":  
    push_data("0")