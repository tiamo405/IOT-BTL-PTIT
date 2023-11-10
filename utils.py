import pytz
from datetime import datetime
import cv2
import requests
import numpy as np
import os
import json
import shutil

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_time():
    current_time = datetime.now()
    hour = str(current_time.hour).zfill(2)
    minute = str(current_time.minute).zfill(2)
    second = str(current_time.second).zfill(2)
    day = str(current_time.day).zfill(2)
    month = str(current_time.month).zfill(2)
    year = str(current_time.year).zfill(2)
    str_time = f"{second}_{minute}_{hour}_{day}_{month}_{year}"

    return str_time

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



def date_to_timestamp(day=0, month=0, year=0, hour=0, minute=0, second=0):
    # Get the local timezone
    local_tz = pytz.timezone('Asia/Ho_Chi_Minh')

    if(year == 0 ):
        now = datetime.now()
        day = now.day
        month = now.month
        year = now.year

    # Create a naive datetime object with the given date and time set to 0 hour 0 minute 0 second
    naive_date = datetime(year, month, day, hour, minute, second)
    
    
    # Localize the naive datetime to the local timezone
    local_date = local_tz.localize(naive_date, is_dst=None)
    
    # Convert the localized datetime object to UTC
    utc_date = local_date.astimezone(pytz.UTC)
    
    # Convert the UTC datetime object to a UNIX timestamp
    timestamp = int(utc_date.timestamp())
    
    return timestamp

def timestamp_to_date(timestamp):
    tz = pytz.timezone('Asia/Ho_Chi_Minh')  # Chọn múi giờ Asia/Ho_Chi_Minh
    utc_time = datetime.utcfromtimestamp(timestamp).replace(tzinfo=pytz.utc)  # Chuyển timestamp thành UTC
    local_time = utc_time.astimezone(tz)  # Chuyển đổi sang múi giờ Asia/Ho_Chi_Minh
    formatted_time = local_time.strftime('%H:%M:%S')  # Định dạng ngày tháng năm giờ phút
    return formatted_time

def check_timeVisit(day, month, year, timeVisit, timeStart, timeEnd ) :
    # Chuyển đổi ngày, tháng, năm thành timestamp cho timeStart và timeEnd
    timeStart_parse = [int(timeStart[:2]), int(timeStart[3:])] 
    timeEnd_parse = [int(timeEnd[:2]), int(timeEnd[3:])] 
    assert timeStart_parse[0] <= 23 
    assert timeStart_parse[1] <= 59 
    assert timeEnd_parse[0] <= 23 
    assert timeEnd_parse[1] <= 59 
    timestamp_start = date_to_timestamp(day, month, year, hour = timeStart_parse[0], minute= timeStart_parse[1])
    timestamp_end = date_to_timestamp(day, month, year, hour = timeEnd_parse[0], minute= timeEnd_parse[1])
    
    # Kiểm tra xem thời gian thăm có nằm trong khoảng thời gian cho phép hay không
    return timestamp_start <= timeVisit <= timestamp_end 

# def checkbbox(box):

def datenow2timestamp():
    now = datetime.now()
    # Get the local timezone
    local_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    
    # Localize the naive datetime to the local timezone
    local_date = local_tz.localize(now, is_dst=None)
    
    # Convert the localized datetime object to UTC
    utc_date = local_date.astimezone(pytz.UTC)
    
    # Convert the UTC datetime object to a UNIX timestamp
    timestamp = int(utc_date.timestamp())
    
    return timestamp


def draw_data2frame(frame, box, data) :
    x_top, y_top, x_bottom, y_bottom = box
    # date = timestamp_to_date(data["timeVisit"])
    name_customer = data["name"]
    customerID = data["customerID"]

    color_ = (0,255,0) if customerID != "-1" else (255,0,0)
    frame = cv2.rectangle(frame, (x_top, y_top), (x_bottom, y_bottom),
                            color_, 2)
    
    # frame = cv2.putText(frame, text=date, org=(100,100), fontFace= cv2.FONT_HERSHEY_SIMPLEX,fontScale= 3,
    #                     color=(0,0,255), thickness=3, lineType= cv2.LINE_AA)
    frame = cv2.putText(frame, text=name_customer, org=(x_top, y_top+100), fontFace= cv2.FONT_HERSHEY_SIMPLEX,fontScale= 3,
                        color=color_, thickness=3, lineType= cv2.LINE_AA)
    return frame


if __name__ =="__main__":
    # img = read_img()
    timestamp = 1699288262  # Thay thế giá trị này bằng timestamp bạn muốn chuyển đổi
    formatted_date = timestamp_to_date(timestamp)
    print(formatted_date)
    print(datenow2timestamp())
    
