import cv2
from mtcnn import MTCNN
import numpy as np
import os
import sys
root = os.getcwd()
pwd = os.path.dirname(os.path.realpath("face"))
sys.path.insert(0, root)
from face import utils_face
from face.face_infer import FaceEmbedding
import config

TRITON_HOST = config.TRITON_HOST
TRITON_POST = config.TRITON_PORT

class Face_Detect():
    def __init__(self, threshold_face = 0.5):
        self.model = MTCNN()
        self.threshold_face = threshold_face
        self.face_embedding = FaceEmbedding(TRITON_HOST= TRITON_HOST, 
                                            TRITON_PORT= TRITON_POST)

    def detect(self, cv_image):
        results = self.model.detect_faces(cv_image)
        bbox = []
        dsts = []
        confidences = []
        for result in results:
            confidence = result['confidence'] # score
            if confidence < self.threshold_face: 
                continue
            x, y, w, h = result['box']  # Tọa độ và kích thước của khuôn mặt
            keypoints = result['keypoints']  # Các điểm trên khuôn mặt
            dst = self._dst(keypoints= keypoints)

            bbox.append((x, y, w, h))
            dsts.append(dst)
            confidences.append(confidence)
        return bbox, dsts, confidences
    
    def _dst(self, keypoints ):
        left_eye = keypoints['left_eye']
        right_eye = keypoints['right_eye']
        nose = keypoints['nose']
        left_mouth = keypoints['mouth_left']
        right_mouth = keypoints['mouth_right']
        dst =[]
        dst.append(left_eye)
        dst.append(right_eye)
        dst.append(nose)
        dst.append(left_mouth)
        dst.append(right_mouth)
        return dst
    
    def align_face(self, cv_image, dst):
        face_align = utils_face.align_face(cv_image, dst)
        cv2.imwrite('face_align.jpg', face_align)
        return face_align

    def get_emb(self, cv_image, dst) :
        face_align = self.align_face(cv_image, dst)
        emb, score = self.face_embedding.get_emb(face_align)
        return emb,score


if __name__ == "__main__":  
    Face_Detect_ = Face_Detect()
    img = cv2.imread('debug.jpg')
    bbox, dsts, confidences = Face_Detect_.detect(img)
    dst = dsts[0]
    Face_Detect_.align_face(img, dst)
    
    