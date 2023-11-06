import cv2
from mtcnn import MTCNN

import os
import sys
root = os.getcwd()
pwd = os.path.dirname(os.path.realpath("face"))
sys.path.insert(0, root)

from face.utils_face import align_face
from face.detect import Face_Detect

# Khởi tạo detector khuôn mặt
detector_face = Face_Detect()

# Đọc video từ tệp tin hoặc camera (thay đổi đối số thành 0 nếu bạn muốn sử dụng camera)
video_path = 'test.mp4'
cap = cv2.VideoCapture(video_path)

while cap.isOpened():
    # Đọc frame từ video
    ret, frame = cap.read()
    if not ret:
        break

    bbox, dsts, confidences = detector_face.detect(cv_image= frame)
    box, dst, confidence = bbox[0], dsts[0], confidences[0]
    
    cv2.imwrite('debug.jpg', frame)
    break
    # # Hiển thị frame với kết quả detect
    # cv2.imshow('Face Detection', frame)

    # # Nhấn 'q' để thoát
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

# Giải phóng các tài nguyên và đóng cửa sổ video
cap.release()
cv2.destroyAllWindows()
