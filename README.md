# Đề tài : Sử dụng khuôn mặt để đóng mở cửa tự động. Có thể theo dõi qua telegram và Web app

# Face
- Feature :
    + Nhận dạng người quen
        + Done
    + Đóng mở cửa
        + Done
- Run
```sh
pythom main.py
```
Mới chạy video, chưa thử camera
# Telegram 
+ Run
```sh
cd bot_tele
python bot_noti.py
```
- Chạy nếu cần sử dụng lệnh trên tele để điều khiển cửa
# Web-app
- Feature :
    + add_family 
        + Done
    + View history 
        + Done
+ Run 
```sh
python web-app/app.py
```
# Phần cứng IOT
- Sử dụng esp8266 và 1 động cơ sevor ( motor qua 180 độ) để quay vòng
- gửi dữ liệu từ backend lên firebase để esp8266 nhận dữ liệu rồi truyền 0-1 cho servo
- nạp code vào esp8266: 
- Chưa có phần cứng, đợi vậy