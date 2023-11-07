import json
import numpy as np
import os
import sys
root = os.getcwd()
pwd = os.path.dirname(os.path.realpath("."))
sys.path.insert(0, root)
from utils import datenow2timestamp, date_to_timestamp

from s3_minio.minio_ import Minio_Client
# Khởi tạo Minio Clinet
minio = Minio_Client()

def find_metadata(id_person):
    customer = minio.get_file_json(name_file= "customer.json")
    data = customer[str(id_person)]
    metadata = {
        "customerID":str(id_person),
        "name": data["name"],
        "timeVisit": datenow2timestamp(),
        "timestamp":date_to_timestamp()
    }
    print(metadata)
    return metadata

def push_data(data_id_person):
    data = minio.get_file_json(name_file= "data.json")
    timeVisit = data_id_person["timeVisit"]
    data[str(timeVisit)] = data_id_person

    # Serializing json
    json_object = json.dumps(data, indent=4)
    # Writing to sample.json
    with open("tmp/data.json", "w") as outfile:
        outfile.write(json_object)

    minio.upload_file(file = 'data.json')
