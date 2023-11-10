import cv2

import os
import sys
import utils
root = os.getcwd()
pwd = os.path.dirname(os.path.realpath("face"))
sys.path.insert(0, root)

from face.detect import Face_Detect
import faiss_
import utils

from s3_minio.minio_ import Minio_Client
from s3_minio import utils_minio

from sensor import api_mocua

THRESHOLD_FACE_DETECT = 0.5
THRESHOLD_FACE_EMB = 0.3

# Khởi tạo detector khuôn mặt
detector_face = Face_Detect()

# Khởi tạo Minio Clinet
minio = Minio_Client()


def main():
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
        time = {
            "timeVisit": utils.datenow2timestamp(),
            "timestamp": utils.date_to_timestamp(),
            "time" : utils.timestamp_to_date(utils.datenow2timestamp())
        }
        
        if frame_count != int(fps * 5): # Nếu đã đọc đủ số frame tương ứng với 5 giây
            frame = cv2.putText(frame, text=time["time"], org=(100,100), fontFace= cv2.FONT_HERSHEY_SIMPLEX,fontScale= 3,
                        color=(0,0,255), thickness=3, lineType= cv2.LINE_AA)
            continue
        # Reset biến đếm frame
        frame_count = 0

        bbox, dsts, confidences = detector_face.detect(cv_image= frame)
        
        # neeus cos nguoi thi xu li, khong co thi next
        if dsts is None : 
            continue
        
        box, dst, confidence = bbox[0], dsts[0], confidences[0]

        
        if confidence < THRESHOLD_FACE_DETECT: 
            continue

        face_align = detector_face.align_face(frame, dst)
        
        
        emb, score = detector_face.get_emb(frame, dst)
        if score < THRESHOLD_FACE_EMB :
            continue

        
        id_person = faiss_.faiss_search(emb)
        data_id_person = utils_minio.find_metadata(id_person)

        #  đẩy dữ liệu + ảnh lên s3, gửi thông báo vào telegram
        utils_minio.push_data(data_id_person, face_align, time)

        print(data_id_person)
        
        # mo cua khi thay nguoi quen
        if id_person != -1 :
            api_mocua.mocua()

        frame = utils.draw_data2frame(frame, box, data_id_person)

        frame = cv2.putText(frame, text=time["time"], org=(100,100), fontFace= cv2.FONT_HERSHEY_SIMPLEX,fontScale= 3,
                        color=(0,0,255), thickness=3, lineType= cv2.LINE_AA)
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


if __name__ == "__main__":  
    main()