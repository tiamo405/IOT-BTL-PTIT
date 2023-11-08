import os
from environs import Env
env = Env()
env.read_env()


TRITON_HOST = os.getenv("TRITON_HOST")
TRITON_PORT = os.getenv("TRITON_PORT")

# ENDPOINT = os.environ.get('ENDPOINT')
# ACCESS_KEY = os.environ.get('ACCESS_KEY')
# SECRET_KEY = os.environ.get('SECRET_KEY')

ENDPOINT = "192.168.100.254:9000"
ACCESS_KEY = "hoangnt"
SECRET_KEY = "cxview2023"
SECURE = False
BUCKET = "84soft"