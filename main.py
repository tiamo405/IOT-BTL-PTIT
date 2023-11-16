import cv2
import os
import sys
import utils, utils_time
import config


root = os.getcwd()
pwd = os.path.dirname(os.path.realpath("face"))
sys.path.insert(0, root)

# Face
from face.detect import Face_Detect
THRESHOLD_FACE_DETECT = config.THRESHOLD_FACE_DETECT
THRESHOLD_FACE_EMB = config.THRESHOLD_FACE_EMB
# Khởi tạo detector khuôn mặt
detector_face = Face_Detect()


# faiss
import faiss_


# minio
from s3_minio.minio_ import Minio_Client
from s3_minio import utils_minio
# Khởi tạo Minio Clinet
minio = Minio_Client()

# hàm liên quan đến sensor kit
from sensor import api

# telegrame
from bot_tele.bot_noti import MyBot
BOT_TOKEN = config.BOT_TOKEN
mybot = MyBot(token= BOT_TOKEN)


def main():
    # Đọc video từ tệp tin hoặc camera (thay đổi đối số thành 0 nếu bạn muốn sử dụng camera)
    video_path = 'test.mp4'
    cap = cv2.VideoCapture(video_path)

    # Đọc tần suất khung hình của luồng video (frames per second - FPS)
    fps = cap.get(cv2.CAP_PROP_FPS)
    #
    frame_width, frame_height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter("output.mp4", fourcc, fps, (frame_width, frame_height))
    # Tạo biến để đếm số frame đã xử lý
    frame_count = 0
    tmp_emb = None

    thoi_gian_mo_cua = int(fps * 10)
    time_start_open = float('inf')

    while cap.isOpened():
        # Đọc frame từ video
        ret, frame = cap.read()
        if not ret:
            break
        frame_count +=1

        time = {
            "timeVisit": utils_time.datenow2timestamp(),
            "timestamp": utils_time.date_to_timestamp(),
            "time" : utils_time.timestamp_to_date(utils_time.datenow2timestamp())
        }

        # Nếu đã đọc đủ số frame tương ứng với 5 giây
        if frame_count % int(fps * 5) == 0: 
            frame = cv2.putText(frame, text=time["time"], org=(100,100), fontFace= cv2.FONT_HERSHEY_SIMPLEX,fontScale= 3,
                        color=(0,0,255), thickness=3, lineType= cv2.LINE_AA)
            video_writer.write(frame)
            continue

        bbox, dsts, confidences = detector_face.detect(cv_image= frame)

        # neeus cos nguoi thi xu li, khong co thi dong cua
        if len(dsts) == 0 :
            if (frame_count - time_start_open) > thoi_gian_mo_cua:
                time_start_open = float('inf')
                api.dongcua()
            continue
        
        box, dst, confidence = bbox[0], dsts[0], confidences[0]

        if confidence < THRESHOLD_FACE_DETECT:
            utils.draw_error(frame, error="khuon mat khong ro")
            continue

        face_align = detector_face.align_face(frame, dst)
        cv2.imwrite(os.path.join(config.DIR_ROOT, "face_align.jpg"), face_align)
        
        emb, score = detector_face.get_emb(frame, dst)
        if score < THRESHOLD_FACE_EMB :
            utils.draw_error(frame, error="khuon mat khong ro")
            continue
        
        # so sánh người này đã đc thông báo chưa. Nếu khonagr cách gần thì là cùng 1 người, vậy không xử lí, nếu là ng lạ thì mới xử lý tiếp
        if tmp_emb is None:
            tmp_emb = emb
        else :
            distance = utils.calculate_cosine_similarity(tmp_emb, emb)
            print(distance)
            if distance < 0.5 : # nếu cùng 1 ng 
                continue
            else : # nếu là người khác thì gán lại tmp_emb
                tmp_emb = emb

        # tìm id người đến, nếu = -1 là người lạ
        id_person = faiss_.faiss_search(emb)
        # tìm thông tin ng đến
        data_id_person = utils_minio.find_metadata(id_person, time)

        #  đẩy dữ liệu + ảnh lên s3, gửi thông báo vào telegram
        utils_minio.push_data(data_id_person, face_align)
 
        print(data_id_person)
        
        # mo cua khi thay nguoi quen
        if id_person != -1 :
            time_start_open = frame_count
            api.mocua()

        frame = utils.draw_data2frame(frame, box, data_id_person)
        cv2.imwrite('debug.jpg', frame)

        mybot.send_notification(text = data_id_person["name"]+ " "+ time["time"],
            path_image= os.path.join(config.DIR_ROOT, "face_align.jpg"))

        video_writer.write(frame)
        # break
        # # Hiển thị frame với kết quả detect
        # cv2.imshow('Face Detection', frame)

        # # Nhấn 'q' để thoát
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Giải phóng các tài nguyên và đóng cửa sổ video
    video_writer.release()
    cap.release()
    cv2.destroyAllWindows()
    
    mybot.start_polling() 

if __name__ == "__main__":  
    main()