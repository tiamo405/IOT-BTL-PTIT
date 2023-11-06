import cv2
import numpy as np
from skimage import transform

def align_face(cv_img, dst):
    """align face theo widerface
    
    Arguments:
        cv_img {arr} -- Ảnh face gốc
        dst {arr}} -- landmark 5 điểm theo mtcnn
    
    Returns:
        arr -- Ảnh face đã align
    """
    face_img = np.zeros((112, 112), dtype=np.uint8)
    # Matrix standard lanmark same wider dataset
    src = np.array([
        [38.2946, 51.6963],
        [73.5318, 51.5014],
        [56.0252, 71.7366],
        [41.5493, 92.3655],
        [70.7299, 92.2041] ], dtype=np.float32)
    
    tform = transform.SimilarityTransform()
    tform.estimate(dst, src)
    M = tform.params[0:2,:]
    face_img = cv2.warpAffine(cv_img, M, (112,112), borderValue=0.0)
    return face_img

def xywh2xyxy(box) :
    x,y,w,h = box
    x_top = x - w//2
    y_top = y - h//2
    x_bot = x + w//2
    y_bot = y + h//2
    return (x_top, y_top, x_bot, y_bot)
    