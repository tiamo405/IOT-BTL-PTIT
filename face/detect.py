import cv2
from mtcnn import MTCNN
import numpy as np


class Face_Detect():
    def __init__(self, threshold_face = 0.5):
        self.model = MTCNN()
        self.threshold_face = threshold_face
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
    
    