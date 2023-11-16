import numpy as np
import cv2
from minio import Minio
import json

import os
import sys
root = os.getcwd()
pwd = os.path.dirname(os.path.realpath("."))
sys.path.insert(0, root)
import config 
import utils

class Minio_Client():
    def __init__(self, endpoint = config.ENDPOINT, access_key = config.ACCESS_KEY, secret_key = config.SECRET_KEY, secure = config.SECURE):
        self.endpoint = endpoint
        self.access_key = access_key
        self.secret_key = secret_key
        self.secure = secure
        self.minio_client = Minio(
            endpoint= self.endpoint,
            access_key= self.access_key,
            secret_key= self.secret_key,
            secure= self.secure,# True nếu sử dụng kết nối an toàn (HTTPS)
        )
        
    def get_embs(self, bucket=config.BUCKET, name_file = 'family/embs.npy'):
        try:
            self.minio_client.fget_object(bucket_name=bucket, 
                                        object_name =name_file , file_path= os.path.join(config.DIR_ROOT, 'tmp', name_file))
            
            embs = np.load(os.path.join(config.DIR_ROOT, 'tmp', name_file))
            embs = np.array(embs).astype('float32')
            return embs
        except :
            return None

    def upload_file(self, bucket=config.BUCKET, file=None):
        # timestape = utils.datenow2timestamp()
        # if file is None :
        #     if file_type =='image' :
        #         file = str(timestape)+'.jpg'
        #     elif file_type == 'json' :
        #         file = str(timestape)+ '.json'

        self.minio_client.fput_object(
            bucket_name= bucket, object_name = file, file_path= os.path.join(config.DIR_ROOT,'tmp', file) 
        )

    def get_url(self, bucket, name_file):

        url = self.minio_client.presigned_get_object(
                bucket, name_file 
            )
        return url
    
    def get_file_json(self, bucket=config.BUCKET, name_file = 'data.json'):
        try:
            self.minio_client.fget_object(bucket_name=bucket, 
                                        object_name =name_file , file_path= os.path.join(config.DIR_ROOT,'tmp', name_file))
            f = open(os.path.join(config.DIR_ROOT, 'tmp', name_file))
            data = json.load(f)
            return data
        except :
            return None
    
if __name__ == "__main__":  
    minio_clinet = Minio_Client()
    # embs = minio_clinet.get_embs(bucket= '84soft', name_file='emb.npy')
    # print(embs)
    # minio_clinet.upload_file(file= 'debug.jpg')
    url = minio_clinet.get_url(bucket= 'iot', name_file='data/1699593296.jpg')
    print(url)
