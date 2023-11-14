import json
import numpy as np
import cv2
import os
import sys
root = os.getcwd()
pwd = os.path.dirname(os.path.realpath("."))
sys.path.insert(0, root)
import config

from s3_minio.minio_ import Minio_Client
# Khởi tạo Minio Clinet
minio = Minio_Client()

def find_metadata(id_person):
    if os.path.exists(os.path.join(config.DIR_ROOT, "tmp/family/embs.npy")):
        f = open(os.path.join(config.DIR_ROOT, "tmp/family/embs.npy"))
        family_data = json.load(f)
    else:
        family_data = minio.get_file_json(name_file= "family/family.json", bucket='iot')
    data = family_data[str(id_person)]
    metadata = {
        "customerID":str(id_person),
        "name": data["name"],
    }
    return metadata

def push_data(data_id_person, image, time):

    if os.path.exists(os.path.join(config.DIR_ROOT, "tmp/data/data.json")) :
        f = open(os.path.join(config.DIR_ROOT, "tmp/data/data.json"))
        data = json.load(f)
    else:
        data = minio.get_file_json(name_file= "data/data.json", bucket='iot')
    
    timeVisit = time["timeVisit"]
    timestamp = time["timestamp"]

    data_id_person["timeVisit"] = timeVisit
    data_id_person["timestamp"] = timestamp

    data[str(timeVisit)] = data_id_person

    # Serializing json
    json_object = json.dumps(data, indent=4)
    # Writing to sample.json
    with open("tmp/data/data.json", "w") as outfile:
        outfile.write(json_object)

    cv2.imwrite(os.path.join('tmp','data' , str(timeVisit)+'.jpg'), image)
    
    minio.upload_file(file = 'data/data.json', bucket='iot')
    minio.upload_file(file= 'data/'+str(timeVisit)+'.jpg', bucket='iot')
    os.remove(os.path.join('tmp', 'data',str(timeVisit)+'.jpg'))

    # bot_tele.send(data_id_person)

