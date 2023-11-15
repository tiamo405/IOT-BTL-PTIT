import pytz
from datetime import datetime

def get_time():
    current_time = datetime.now()
    hour = str(current_time.hour).zfill(2)
    minute = str(current_time.minute).zfill(2)
    second = str(current_time.second).zfill(2)
    day = str(current_time.day).zfill(2)
    month = str(current_time.month).zfill(2)
    year = str(current_time.year).zfill(2)
    str_time = f"{hour} : {minute} : {second} {day}-{month}-{year}"

    return str_time


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
    formatted_time = local_time.strftime('%Y-%m-%d %H:%M:%S')  # Định dạng ngày tháng năm giờ phút
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