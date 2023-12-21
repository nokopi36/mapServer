# 捜索範囲を指定するためのmapの設定
map_start_latitude = 34.439946888534195
map_start_longtitude = 132.4169722549677
photo_height = 10
photo_width = 20
rows = 2
cols = 2
original_map_path = "original_map.html"
new_map_path = "map.html"

# システムを動かすための設定
detect_model = "runs/detect/trainResult/LDGen/s/1280_33Y20_0.3/weights/best.pt"
detect_img_path = "datasets/1280_33/images/test"
split_img_path = ""
server_ip = ""
sercer_port = 12345
send_file_name = "shotPoint.txt"  # Androidに送信するファイル名
drone_altitude = 50
grid_size_width = 3
grid_size_height = 3

# DJI Mavic2 Enterprise DUALのカメラスペック
sensor_width_mm = 6.287  # センサーサイズの幅（ミリメートル）
sensor_height_mm = 4.712  # センサーサイズの高さ（ミリメートル）
focal_length_mm = 4.3  # 焦点距離（ミリメートル）
fov_degrees = 85  # 視野角（度）
img_width = 4056
img_height = 3040
