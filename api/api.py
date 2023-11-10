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
    if score < 0.3 :
        return
    embs = minio.get_embs()
    embs = np.vstack((embs, emb)) 
    np.save('tmp/family/embs.npy', embs)
    
    family_data = minio.get_file_json(name_file= "family/family.json", bucket='iot')
    num_persons = len(family_data)
    cv2.imwrite(os.path.join('tmp','family' ,str(num_persons-1)+'.jpg'), face_align)
    family_data[str(num_persons-1)] = {
        "name": name,
        "Dob": dob,
        "gender": gender,
        "role": role
    }
    # Serializing json
    json_object = json.dumps(family_data, indent=4)
    # viet lai file json family
    with open("tmp/family/family.json", "w") as outfile:
        outfile.write(json_object)
    
    minio.upload_file(file= 'family/'+ str(num_persons-1)+'.jpg', bucket='iot')    
    minio.upload_file(file= 'family/embs.npy', bucket= 'iot')
    minio.upload_file(file = 'family/family.json', bucket= 'iot')

if __name__ == "__main__":  

    add_family(image="tmp/data/1699434204.jpg", name="test")