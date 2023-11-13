import os
from environs import Env
env = Env()
env.read_env()

DIR_ROOT = os.path.dirname(os.path.abspath(__file__))

TRITON_HOST = os.getenv("TRITON_HOST")
TRITON_PORT = os.getenv("TRITON_PORT")

ENDPOINT = "192.168.100.254:9000"
ACCESS_KEY = "hoangnt"
SECRET_KEY = "cxview2023"
SECURE = False
BUCKET = "iot"
