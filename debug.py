import numpy as np
import json
from utils import datenow2timestamp

data = []
for i in range(4):
    json_data = {
        "customerID": i,
        "timeVisit" : datenow2timestamp()
    }
    data.append(json_data)

with open('tmp/data.json', 'w') as json_file:
    json.dump(data, json_file)

# Đọc dữ liệu từ tệp tin JSON
with open('tmp/data.json', 'r') as json_file:
    loaded_data = json.load(json_file)

# Kiểm tra xem dữ liệu đã được đọc đúng chưa
print(loaded_data)