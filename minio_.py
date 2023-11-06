from minio import Minio
import os
import pymongo
from utils import date_to_timestamp, check_timeVisit



MONGOCLIENT = os.environ.get('MONGOCLIENT')
ENDPOINT = os.environ.get('ENDPOINT')
ACCESS_KEY = os.environ.get('ACCESS_KEY')
SECRET_KEY = os.environ.get('SECRET_KEY')

# MONGOCLIENT = "mongodb://192.168.100.23:27017"
# ENDPOINT = "s3.hcm01.cxview.ai"
# ACCESS_KEY = "cVn2tXPeh06hf8X4"
# SECRET_KEY = "otrT8mTON2oLGr4n3v9Fd8D5xaAC0UpK"


def _query(groupID, boxID, day, month, year):
    myclient = pymongo.MongoClient(MONGOCLIENT)
    mydb = myclient["cxview"]
    mycol = mydb["customerrecord"]
    timestamp = date_to_timestamp(day, month, year)
    # myquery = { "groupID": groupID, "timestamp": timestamp}
    myquery = { "groupID": groupID,"boxID": boxID, "timestamp": timestamp}
    results = mycol.find(myquery)
    return results

def get_url(minio_client, bucket, name_file):

    url = minio_client.presigned_get_object(
            bucket, name_file 
        )
    return url

def get_urls(bucket, groupID, boxID, day, month, year, timeStart, timeEnd):
    
    minio_client = Minio(
        endpoint= ENDPOINT,
        access_key=ACCESS_KEY,
        secret_key=SECRET_KEY,
        secure=True,# True nếu sử dụng kết nối an toàn (HTTPS)
    )

    results = _query(groupID, boxID, day, month, year)

    metadatas = []
    for x in results:
        name_file = x['id']+'.jpg'
        url = get_url(minio_client, bucket, name_file)
        if (str(x['isMaskedFace']) == 'True' or str(x['isMaskedFace']) == 'None') \
            and check_timeVisit(day, month, year, x['timeVisit'], timeStart, timeEnd) == True:
            x['url'] = url
            metadatas.append(x)
    return metadatas

def upload_file(minio_client: Minio, bucket, file):
    minio_client.fput_object(
        bucket_name= bucket, object_name = file, file_path= file 
    )

if __name__ == "__main__":  

    # minio_client = Minio(
    #     endpoint= ENDPOINT,
    #     access_key=ACCESS_KEY,
    #     secret_key=SECRET_KEY,
    #     secure=True  # True nếu sử dụng kết nối an toàn (HTTPS)
    # )
    # url = get_url(minio_client= minio_client, bucket= "product-customer-image", 
    #               name_file="1ac358dc-7cca-4a9a-9fb7-bd8efbd27814.jpg")
    # print(url)
    # url = minio_client.presigned_get_object(
    #         bucket_name= "product-customer-image", 
    #         object_name = "7bb85ce7-ebbe-4a0d-a3aa-2435d3c9bec1.jpg"
    #     )
    # print(url)
    # minio_client = Minio(
    #     endpoint= "192.168.100.254:9000",
    #     access_key="hoangnt",
    #     secret_key= "cxview2023",
    #     secure=False
    # )
    # # upload_file(minio_client, bucket= "84soft", file="app.log")
    # url = get_url(minio_client= minio_client, bucket="84soft", name_file= "log.log")
    # print(url)
    myclient = pymongo.MongoClient(MONGOCLIENT)
    mydb = myclient["cxview"]
    mycol = mydb["customerrecord"]
    timestamp = date_to_timestamp(10, 10, 2023)
    myquery = {"groupID":"dc1ef397-60e0-4040-8326-8375b7270716", "timestamp": timestamp}

    results = mycol.find(myquery)

    # ids = []

    # for x in results:
    #     # with open('file.txt', 'a') as f:
    #     #     timestamp = x['timestamp']
    #     #     f.write(x["id"]+' '+ x['groupID']+"\n")
    #     #     # ids.append(x["id"]+"\n")
    #     # f.close()
    #     print(x)

        # print(x['id'], ' ', x['groupID'])