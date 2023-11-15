import cv2
import requests
import numpy as np
import os
import utils_time
from sklearn.metrics.pairwise import cosine_similarity

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def crop(image):
    height, width, _ = image.shape
    
    # Tính toán tọa độ bắt đầu và kết thúc để cắt ảnh giữa
    if height > 112 and width >112:
        start_x = (width - 112) // 2
        end_x = start_x + 112
        start_y = (height - 112) // 2
        end_y = start_y + 112

        # Cắt ảnh theo tọa độ đã tính
        cropped_image = image[start_y:end_y, start_x:end_x]
        return cropped_image
    else : 
        return image

def read_img(path):
    image = None
    if path.startswith('http://') or path.startswith('https://'):
        try:
            response = requests.get(path)
            if response.status_code == 200:
                # Đọc dữ liệu hình ảnh từ nội dung của response
                image_data = np.frombuffer(response.content, dtype=np.uint8)

                # Đọc hình ảnh bằng OpenCV
                image_ori = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
                image_crop = crop(image_ori)
            else :
                return None
        
        except Exception as e:
            return e
    elif os.path.isfile(path):
        image_ori = cv2.imread(path)
        image_crop = crop(image_ori)

    return image_crop, image_ori 


def draw_data2frame(frame, box, data) :
    x_top, y_top, x_bottom, y_bottom = box

    name_customer = data["name"]
    customerID = data["customerID"]
    time = utils_time.timestamp_to_date(data["timeVisit"])

    color_ = (0,255,0) if customerID != "-1" else (255,0,0)

    frame = cv2.rectangle(frame, (x_top, y_top), (x_bottom, y_bottom),
                            color_, 2)
    

    frame = cv2.putText(frame, text=name_customer, org=(x_top, y_top+100), fontFace= cv2.FONT_HERSHEY_SIMPLEX,fontScale= 3,
                        color=color_, thickness=3, lineType= cv2.LINE_AA)
    
    frame = cv2.putText(frame, text= time, org=(100,100), fontFace= cv2.FONT_HERSHEY_SIMPLEX,fontScale= 3,
                        color=(0,0,255), thickness=3, lineType= cv2.LINE_AA)
    return frame

def draw_error(frame, error):
    frame_height, frame_width, _ = frame.shape
    # Tính kích thước của đoạn thông báo
    (text_width, text_height), baseline = cv2.getTextSize(text = error, fontFace = cv2.FONT_HERSHEY_SIMPLEX, fontScale= 3 , thickness=3)
    # Tính toán tọa độ để đặt văn bản vào giữa frame
    x = (frame_width - text_width) // 2
    y = (frame_height + text_height) // 2
    frame = cv2.putText(frame, text= error, org=(x,y), fontFace= cv2.FONT_HERSHEY_SIMPLEX,fontScale= 3,
                        color=(255,0,0), thickness=3, lineType= cv2.LINE_AA)
    return frame


def calculate_cosine_similarity(embedding1, embedding2):
    # Chuẩn hóa vectơ embedding
    embedding1_normalized = embedding1 / np.linalg.norm(embedding1)
    embedding2_normalized = embedding2 / np.linalg.norm(embedding2)

    # Reshape để có cùng kích thước
    embedding1_reshaped = embedding1_normalized.reshape(1, -1)
    embedding2_reshaped = embedding2_normalized.reshape(1, -1)

    # Tính cosine similarity
    distance = 1 -cosine_similarity(embedding1_reshaped, embedding2_reshaped)[0, 0]

    return distance


if __name__ =="__main__":
    # img = read_img()
    timestamp = 1699288262  # Thay thế giá trị này bằng timestamp bạn muốn chuyển đổi
    formatted_date = utils_time.timestamp_to_date(timestamp)
    print(formatted_date)
    print(utils_time.datenow2timestamp())
    
