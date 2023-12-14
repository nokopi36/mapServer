import math
import os
import sys
from turtle import st
from PIL import Image
import numpy as np

open_imgDir = "valid/images/img0.jpg"

# open_droneLocDir = 'valid/images/droneLocation.txt'
# open_personLocDir = 'concat/result.txt'
open_droneLocDir = sys.argv[2]
open_personLocDir = sys.argv[4]
txt_count = 1


# 以下実際の緯度経度を求める()
# 楕円体
ELLIPSOID_GRS80 = 1  # GRS80
ELLIPSOID_WGS84 = 2  # WGS84

# 楕円体別の長軸半径と扁平率
GEODETIC_DATUM = {
    ELLIPSOID_GRS80: [
        6378137.0,  # [GRS80]長軸半径
        1 / 298.257222101,  # [GRS80]扁平率
    ],
    ELLIPSOID_WGS84: [
        6378137.0,  # [WGS84]長軸半径
        1 / 298.257223563,  # [WGS84]扁平率
    ],
}

# 反復計算の上限回数
ITERATION_LIMIT = 1000

"""
Vincenty法(順解法)
始点の座標(緯度経度)と方位角と距離から、終点の座標と方位角を求める
:param lat: 緯度
:param lon: 経度
:param azimuth: 方位角
:param distance: 距離
:param ellipsoid: 楕円体
:return: 終点の座標、方位角
"""


def vincenty_direct(lat, lon, azimuth, distance, ellipsoid=None):
    # 計算時に必要な長軸半径(a)と扁平率(ƒ)を定数から取得し、短軸半径(b)を算出する
    # 楕円体が未指定の場合はGRS80の値を用いる
    a, ƒ = GEODETIC_DATUM.get(ellipsoid, GEODETIC_DATUM.get(ELLIPSOID_GRS80))
    b = (1 - ƒ) * a

    # ラジアンに変換する(距離以外)
    φ1 = math.radians(lat)
    λ1 = math.radians(lon)
    alpha1 = math.radians(azimuth)
    s = distance

    sinAlpha1 = math.sin(alpha1)
    cosAlpha1 = math.cos(alpha1)

    # 更成緯度(補助球上の緯度)
    U1 = math.atan((1 - ƒ) * math.tan(φ1))

    sinU1 = math.sin(U1)
    cosU1 = math.cos(U1)
    tanU1 = math.tan(U1)

    sigma1 = math.atan2(tanU1, cosAlpha1)
    sinAlpha = cosU1 * sinAlpha1
    cos2Alpha = 1 - sinAlpha**2
    u2 = cos2Alpha * (a**2 - b**2) / (b**2)
    A = 1 + u2 / 16384 * (4096 + u2 * (-768 + u2 * (320 - 175 * u2)))
    B = u2 / 1024 * (256 + u2 * (-128 + u2 * (74 - 47 * u2)))

    # σをs/(b*A)で初期化
    sigma = s / (b * A)

    # 以下の計算をσが収束するまで反復する
    # 地点によっては収束しないことがあり得るため、反復回数に上限を設ける
    for i in range(ITERATION_LIMIT):
        cos2Sigmam = math.cos(2 * sigma1 + sigma)
        sinSigma = math.sin(sigma)
        cosSigma = math.cos(sigma)
        ΔSigma = (
            B
            * sinSigma
            * (
                cos2Sigmam
                + B
                / 4
                * (
                    cosSigma * (-1 + 2 * cos2Sigmam**2)
                    - B
                    / 6
                    * cos2Sigmam
                    * (-3 + 4 * sinSigma**2)
                    * (-3 + 4 * cos2Sigmam**2)
                )
            )
        )
        sigmaDash = sigma
        sigma = s / (b * A) + ΔSigma

        # 偏差が.000000000001以下ならbreak
        if abs(sigma - sigmaDash) <= 1e-12:
            break
    else:
        # 計算が収束しなかった場合はNoneを返す
        return None

    # σが所望の精度まで収束したら以下の計算を行う
    x = sinU1 * sinSigma - cosU1 * cosSigma * cosAlpha1
    φ2 = math.atan2(
        sinU1 * cosSigma + cosU1 * sinSigma * cosAlpha1,
        (1 - ƒ) * math.sqrt(sinAlpha**2 + x**2),
    )
    λ = math.atan2(
        sinSigma * sinAlpha1, cosU1 * cosSigma - sinU1 * sinSigma * cosAlpha1
    )
    C = ƒ / 16 * cos2Alpha * (4 + ƒ * (4 - 3 * cos2Alpha))
    L = λ - (1 - C) * ƒ * sinAlpha * (
        sigma + C * sinSigma * (cos2Sigmam + C * cosSigma * (-1 + 2 * cos2Sigmam**2))
    )
    λ2 = L + λ1

    alpha2 = math.atan2(sinAlpha, -x) + math.pi

    return {
        "lat": math.degrees(φ2),  # 緯度
        "lon": math.degrees(λ2),  # 経度
        "azimuth": math.degrees(alpha2),  # 方位角
    }


with open(open_droneLocDir, "r") as fDrone:
    d_line = fDrone.readline()
    droneLocate = d_line.split()
    droneLatitude = float(droneLocate[0])
    droneLongtitude = float(droneLocate[1])
    droneAltitude = float(droneLocate[2])
    droneHeading = float(droneLocate[3])
    print(droneLatitude, droneLongtitude, droneAltitude, droneHeading)

# print(math.tan(math.radians(47.5)))
img_width = 2 * droneAltitude / math.tan(math.radians(47.5))
img_height = 3 * img_width / 4
# print(img_width, img_height)

img = Image.open(open_imgDir)
imgCenter_x = int(img.width / 2)  # center and zero
imgCenter_y = int(img.height / 2)  # center and zero
# print(imgCenter_x, imgCenter_y)
xDot_m = img.width / img_width  # width dot/m
yDot_m = img.height / img_height  # height dot/m
# print(xDot_m,yDot_m)

with open(open_personLocDir, "r") as fPerson:
    while True:
        s_line = fPerson.readline()
        if not s_line:
            break
        personLocate = s_line.split()
        personLocatNumber = personLocate[0]
        personLocate_x = int(personLocate[1])
        personLocate_y = int(personLocate[2])
        # print(personLocate_x,personLocate_y)

        if imgCenter_x >= personLocate_x:
            distance_x = imgCenter_x - personLocate_x
        else:
            distance_x = personLocate_x - imgCenter_x

        if imgCenter_y >= personLocate_y:
            distance_y = imgCenter_y - personLocate_y
        else:
            distance_y = personLocate_y - imgCenter_y
        # print(distance_x, distance_y)

        realDistance_x = distance_x / xDot_m
        realDistance_y = distance_y / yDot_m

        realDistance_xy = math.sqrt(realDistance_x**2 + realDistance_y**2)
        # print(realDistance_x,realDistance_y,realDistance_xy)

        x0, y0 = 0, 0
        x1, y1 = 0, imgCenter_y
        # print(x1,y1)
        x2, y2 = personLocate_x - imgCenter_x, imgCenter_y - personLocate_y
        # print(x2,y2)
        vec1 = [x1 - x0, y1 - y0]
        vec2 = [x2 - x0, y2 - y0]
        absvec1 = np.linalg.norm(vec1)
        absvec2 = np.linalg.norm(vec2)
        inner = np.inner(vec1, vec2)
        # print(inner)
        cos_theta = inner / (absvec1 * absvec2)
        theta = math.degrees(math.acos(cos_theta))
        kakudo = round(theta, 2)
        if x2 < 0:
            kakudo = 360 - kakudo
            print("angle =" + str(kakudo) + "deg")
        else:
            print("angle =" + str(kakudo) + "deg")

        hoseiKakudo = kakudo - droneHeading
        print("hoseikakudo =" + str(hoseiKakudo))
        if hoseiKakudo < 0:
            kakudo = 360 + hoseiKakudo
            print("-true kakudo =" + str(kakudo) + "deg")
        elif hoseiKakudo > 360:
            kakudo = hoseiKakudo - 360
            print("+true kakudo =" + str(kakudo) + "deg")
        else:
            kakudo = hoseiKakudo
            print("true kakudo =" + str(kakudo) + "deg")

        finalLocation = vincenty_direct(
            droneLatitude, droneLongtitude, kakudo, realDistance_xy
        )
        print("Number", personLocatNumber)
        print("緯度：%s" % finalLocation["lat"])
        print("経度：%s" % finalLocation["lon"])
        print("方位角：%s" % finalLocation["azimuth"])
