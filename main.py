import cv2

import os
import sys
root = os.getcwd()
pwd = os.path.dirname(os.path.realpath("face"))
sys.path.insert(0, root)

from face.detect import Face_Detect
import faiss_

THRESHOLD_FACE_DETECT = 0.5
THRESHOLD_FACE_EMB = 0.3

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
    if dsts is None : 
        continue

    box, dst, confidence = bbox[0], dsts[0], confidences[0]
    if confidence < THRESHOLD_FACE_DETECT: 
        continue
    face_align = detector_face.align_face(frame, dst)
    emb, score = detector_face.get_emb(frame, dst)
    if score < THRESHOLD_FACE_EMB :
        continue
    index = faiss_.faiss_search(emb)
    print(index)
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
