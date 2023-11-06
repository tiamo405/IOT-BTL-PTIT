import cv2

import os
import sys
root = os.getcwd()
pwd = os.path.dirname(os.path.realpath("face"))
sys.path.insert(0, root)

from face.detect import Face_Detect
import faiss_
import utils

from s3_minio.minio_ import Minio_Client
THRESHOLD_FACE_DETECT = 0.5
THRESHOLD_FACE_EMB = 0.3

# Khởi tạo detector khuôn mặt
detector_face = Face_Detect()
minio = Minio_Client

# Đọc video từ tệp tin hoặc camera (thay đổi đối số thành 0 nếu bạn muốn sử dụng camera)
video_path = 'test.mp4'
cap = cv2.VideoCapture(video_path)
# Đọc tần suất khung hình của luồng video (frames per second - FPS)
fps = cap.get(cv2.CAP_PROP_FPS)
# Tạo biến để đếm số frame đã xử lý
frame_count = 0
while cap.isOpened():
    # Đọc frame từ video
    ret, frame = cap.read()
    if not ret:
        break
    frame_count +=1
    if frame_count != int(fps * 5): # Nếu đã đọc đủ số frame tương ứng với 5 giây
        continue
    # Reset biến đếm frame
    frame_count = 0

    bbox, dsts, confidences = detector_face.detect(cv_image= frame)
    if dsts is None : 
        continue
    
    box, dst, confidence = bbox[0], dsts[0], confidences[0]

    x_top, y_top, x_bottom, y_bottom = box
    frame = cv2.rectangle(frame, (x_top, y_top), (x_bottom, y_bottom),
                          (0,255,0), 2)
    if confidence < THRESHOLD_FACE_DETECT: 
        continue

    face_align = detector_face.align_face(frame, dst)

    emb, score = detector_face.get_emb(frame, dst)
    if score < THRESHOLD_FACE_EMB :
        continue
    timestamp = utils.datenow2timestamp()
    cv2.imwrite(os.path.join('tmp', str(timestamp)+'.jpg'))
    

    id_person = faiss_.faiss_search(emb)
    print(id_person)

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
