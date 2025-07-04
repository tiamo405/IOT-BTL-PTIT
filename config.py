import os
from environs import Env
env = Env()
env.read_env()

DIR_ROOT = os.path.dirname(os.path.abspath(__file__))


# TRITON
TRITON_HOST = os.getenv("TRITON_HOST")
TRITON_PORT = os.getenv("TRITON_PORT")

# S3
# ENDPOINT = "192.168.100.254:9000"
# ACCESS_KEY = "hoangnt"
# SECRET_KEY = "cxview2023"
ENDPOINT = "127.0.0.1:9000"
ACCESS_KEY = "minioadmin"
SECRET_KEY = "minioadmin"
SECURE = False
BUCKET = "iot"

#Tele
BOT_TOKEN = os.getenv("BOT_TOKEN")
USER_CHAT_ID = os.getenv("USER_CHAT_ID")

#  threshold face
THRESHOLD_FACE_DETECT = 0.5
THRESHOLD_FACE_EMB = 0.3

# Firebase

FIREBASE_CERT = os.getenv("FIREBASE_CERT")
FIREBASE_DB_URL = os.getenv("FIREBASE_DB_URL")
