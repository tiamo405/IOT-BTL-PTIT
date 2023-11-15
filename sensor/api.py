import time
import cv2
def mocua():
    print("Da mo cua")

def dongcua():
    print("Da dong cua")


if __name__ == "__main__":  
    # Đọc video từ tệp tin hoặc camera (thay đổi đối số thành 0 nếu bạn muốn sử dụng camera)
    video_path = '/mnt/nvme0n1/phuongnam/IOT/output.mp4'
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

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret :
            break
        frame_count +=1

        if frame_count % 10 == 0 :
            frame = cv2.putText(frame, text= 'frame: '+str(frame), org=(100,100), fontFace= cv2.FONT_HERSHEY_SIMPLEX,fontScale= 3,
                        color=(255,0,0), thickness=3, lineType= cv2.LINE_AA)
            mocua()
        else :
            frame = cv2.putText(frame, text= 'frame: '+str(frame), org=(100,100), fontFace= cv2.FONT_HERSHEY_SIMPLEX,fontScale= 3,
                        color=(255,0,0), thickness=3, lineType= cv2.LINE_AA)
        video_writer.write(frame)

    # Giải phóng các tài nguyên và đóng cửa sổ video
    video_writer.release()
    cap.release()
    cv2.destroyAllWindows()