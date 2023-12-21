import pyproj
from math import atan2, degrees, sqrt, radians, tan
import setting
import os


def detected_object_location(directory):
    for file_name in os.listdir(directory):
        if file_name.endswith(".txt") and not file_name.endswith("_combine.txt"):
            base_name = file_name.split(".")[0]

            # 緯度経度ファイルの読み込み
            with open(os.path.join(directory, file_name), "r") as file:
                center_latitude, center_longitude = map(float, file.readline().split())

            # 対応する物体位置ファイルの存在確認
            combine_file_name = f"{base_name}_combine.txt"
            if combine_file_name in os.listdir(directory):
                with open(os.path.join(directory, combine_file_name), "r") as file:
                    # 新しい緯度経度をファイルに保存
                    location_file_name = os.path.join(
                        directory, f"{base_name}_location.txt"
                    )
                    with open(location_file_name, "w") as location_file:
                        for line in file:
                            object_x_px, object_y_px = map(int, line.split())
                            new_latitude, new_longitude = calculate_location(
                                center_latitude,
                                center_longitude,
                                object_x_px,
                                object_y_px,
                            )
                            location_file.write(f"{new_latitude} {new_longitude}\n")


def calculate_location(center_latitude, center_longitude, object_x_px, object_y_px):
    # ここでの計算は設定値に依存するため、設定を適切に読み込む必要があります。
    fov_radians = radians(setting.fov_degrees)
    shooting_area_width = 2 * setting.drone_altitude * tan(fov_radians / 2)
    shooting_area_height = shooting_area_width * (
        setting.sensor_height_mm / setting.sensor_width_mm
    )
    meter_per_pixel_x = shooting_area_width / setting.img_width
    meter_per_pixel_y = shooting_area_height / setting.img_height

    # 物体の中心からのオフセットを計算（メートル単位）
    offset_x_m = (object_x_px - setting.img_width / 2) * meter_per_pixel_x
    offset_y_m = (setting.img_height / 2 - object_y_px) * meter_per_pixel_y

    # 方位角を計算（度単位）
    bearing = degrees(atan2(offset_y_m, offset_x_m))

    # 距離を計算（メートル単位）
    distance = sqrt(offset_x_m**2 + offset_y_m**2)

    # Geodオブジェクトを作成（WGS84楕円体を使用）
    geod = pyproj.Geod(ellps="WGS84")

    # 新しい緯度経度を計算
    new_longitude, new_latitude, _ = geod.fwd(
        center_longitude, center_latitude, bearing, distance
    )

    return new_latitude, new_longitude
