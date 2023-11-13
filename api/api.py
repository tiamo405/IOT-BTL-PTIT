import numpy as np
import cv2
import json
import os
import sys
root = os.getcwd()
pwd = os.path.dirname(os.path.realpath("s3_minio"))
sys.path.insert(0, root)

from s3_minio.minio_ import Minio_Client
from s3_minio import utils_minio
cwd = os.getcwd()
sys.path.append(os.path.abspath(os.path.dirname(cwd)))
import utils, config

minio = Minio_Client()

import faiss_

# Khởi tạo detector khuôn mặt
pwd = os.path.dirname(os.path.realpath("face"))
sys.path.insert(0, root)

from face.detect import Face_Detect
detector_face = Face_Detect()


def api_add_family(image, name="test", dob="01/01/2000", gender="", role="family", push = True) :
    # khoi tao error
    ERROR = "File uploaded successfully"
    try:
        image = cv2.imread(image)
        print(image.shape)
    except:
        ERROR = "Image not valid."
        return ERROR
    bbox, dsts, confidences = detector_face.detect(cv_image= image)
    print(bbox)
    # neeus cos nguoi thi xu li, khong co thi next
    if len(bbox) == 0:
        ERROR = "khong nhan dien duoc face"
        print(ERROR)
        return ERROR
    
    box, dst, confidence = bbox[0], dsts[0], confidences[0]

    if confidence < 0.5: 
        ERROR = "khuon mat bi mo"
        print(ERROR)
        return ERROR
    face_align = detector_face.align_face(image, dst)

    
    emb, score = detector_face.get_emb(image, dst)
    # kiểm tra score có đủ để thêm ảnh vào database
    if score < 0.3 :
        ERROR = " khuon mat bi mo"
        print(ERROR)
        return ERROR

    if push:
        # kiểm tra người này đã được thêm vào database chưa
        
        id_person = faiss_.faiss_search(emb)
        if int(id_person) != -1: # đã có trong database thì không thêm nữa
            data_id_person = utils_minio.find_metadata(id_person)
            ERROR = "khuon mat da co trong data" + str(data_id_person)
            print(ERROR)
            return ERROR
    if push:
    # bắt đầu thêm emb vào data emb
        embs = minio.get_embs()
        embs = np.vstack((embs, emb)) 
    else:
        if os.path.exists(os.path.join(config.DIR_ROOT, 'tmp/family/embs.npy')):
            embs = np.load(os.path.join(config.DIR_ROOT, 'tmp/family/embs.npy'))
            embs = np.vstack((embs, emb))
        else:
            embs = emb

    # lưu lại để push lên s3
    np.save(os.path.join(config.DIR_ROOT, 'tmp/family/embs.npy'), embs)
    
    if push:
        # dowload file family về đề thêm các trường dữ liệu người mới
        family_data = minio.get_file_json(name_file= "family/family.json", bucket='iot')
    else:
        f = open(os.path.join(config.DIR_ROOT, 'tmp/family/family.json'))
        family_data = json.load(f)
    num_persons = len(family_data)

    # lưu ảnh lại để push lên s3
    cv2.imwrite(os.path.join(config.DIR_ROOT,'tmp','family' ,str(num_persons-1)+'.jpg'), face_align)
    # thêm dữ liệu người mới
    family_data[str(num_persons-1)] = {
        "name": name,
        "Dob": dob,
        "gender": gender,
        "role": role,
        "time_upload": utils.timestamp_to_date(utils.datenow2timestamp())
    }
    # in
    print(family_data)
    # viet lai file json family
    json_object = json.dumps(family_data, indent=4)
    with open(os.path.join(config.DIR_ROOT, "tmp/family/family.json"), "w") as outfile:
        outfile.write(json_object)
    
    if push:
        # bắt đầu đẩy 3 file là json, img, embs lên
        minio.upload_file(file= 'family/'+ str(num_persons-1)+'.jpg', bucket='iot')    
        minio.upload_file(file= 'family/embs.npy', bucket= 'iot')
        minio.upload_file(file = 'family/family.json', bucket= 'iot')

    return ERROR
if __name__ == "__main__":  

    error = api_add_family(image="0.jpg", name="Tran Phuong Nam", dob = "05/05/2002", gender="male", role="admin", push= False)
    print(error)