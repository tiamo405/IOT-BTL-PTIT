import numpy as np
import cv2
from minio import Minio

import os
import sys
root = os.getcwd()
pwd = os.path.dirname(os.path.realpath("."))
sys.path.insert(0, root)
import config 

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
        
    def get_embs(self, bucket='84soft', name_file = 'embs.npy'):
        try:
            self.minio_client.fget_object(bucket_name=bucket, 
                                        object_name =name_file , file_path= os.path.join('tmp', name_file))
            
            embs = np.load(os.path.join('tmp', name_file))
            embs = np.array(embs).astype('float32')
            return embs
        except :
            return None

    def upload_file(minio_client: Minio, bucket, file):
        minio_client.fput_object(
            bucket_name= bucket, object_name = file, file_path= file 
        )

    def get_url(self, bucket, name_file):

        url = self.minio_client.presigned_get_object(
                bucket, name_file 
            )
        return url
    
if __name__ == "__main__":  
    minio_clinet = Minio_Client()
    embs = minio_clinet.get_embs(bucket= '84soft', name_file='emb.npy')
    print(embs)