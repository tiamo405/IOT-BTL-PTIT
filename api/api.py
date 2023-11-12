import numpy as np
import cv2
import json
import os
import sys
root = os.getcwd()
pwd = os.path.dirname(os.path.realpath("s3_minio"))
sys.path.insert(0, root)

from s3_minio.minio_ import Minio_Client

minio = Minio_Client()

import faiss_

# Khởi tạo detector khuôn mặt
pwd = os.path.dirname(os.path.realpath("face"))
sys.path.insert(0, root)

from face.detect import Face_Detect
detector_face = Face_Detect()

def add_family(image, name, dob="01/01/2000", gender="", role="family") :
    
    image = cv2.imread(image)
    bbox, dsts, confidences = detector_face.detect(cv_image= image)
    # neeus cos nguoi thi xu li, khong co thi next
    if dsts is None : 
        return
    
    box, dst, confidence = bbox[0], dsts[0], confidences[0]

    if confidence < 0.5: 
        return
    face_align = detector_face.align_face(image, dst)

    
    emb, score = detector_face.get_emb(image, dst)

    # kiểm tra người này đã được thêm vào database chưa
    id_person = faiss_.faiss_search(emb)
    if id_person == "-1": # đã có trong database thì không thêm nữa
        return 0
    
    # kiểm tra score có đủ để thêm ảnh vào database
    if score < 0.3 :
        return
    
    # bắt đầu thêm emb vào data emb
    embs = minio.get_embs()
    embs = np.vstack((embs, emb)) 
    # lưu lại để push lên s3
    np.save('tmp/family/embs.npy', embs)
    
    # lưu ảnh lại để push lên s3
    cv2.imwrite(os.path.join('tmp','family' ,str(num_persons-1)+'.jpg'), face_align)
    # dowload file family về đề thêm các trường dữ liệu người mới
    family_data = minio.get_file_json(name_file= "family/family.json", bucket='iot')
    num_persons = len(family_data)

    # thêm dữ liệu người mới
    family_data[str(num_persons-1)] = {
        "name": name,
        "Dob": dob,
        "gender": gender,
        "role": role
    }

    # viet lai file json family
    json_object = json.dumps(family_data, indent=4)
    with open("tmp/family/family.json", "w") as outfile:
        outfile.write(json_object)
    
    # bắt đầu đẩy 3 file là json, img, embs lên
    minio.upload_file(file= 'family/'+ str(num_persons-1)+'.jpg', bucket='iot')    
    minio.upload_file(file= 'family/embs.npy', bucket= 'iot')
    minio.upload_file(file = 'family/family.json', bucket= 'iot')
    return 1
if __name__ == "__main__":  

    add_family(image="tmp/data/1699434204.jpg", name="test")