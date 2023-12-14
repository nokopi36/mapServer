import sys
from PIL import Image
import glob
import re

def numericalSort(value):
    numbers = re.compile(r'(\d+)')
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

open_dir = sys.argv[2]
save_dir = sys.argv[4]
W_DIV = int(sys.argv[6]) # 横分割数
H_DIV = int(sys.argv[8]) # 縦分割数
path_all = sorted(glob.glob(open_dir + '*.jpg'), key=numericalSort)

# print(open_dir + '\n' + save_dir + '\n' + sys.argv[6],sys.argv[8])


new_jpg_count = 1 # 新しくjpgファイルを作るときのファイル名用のカウンタ

for f in range(len(path_all)):		# 元の*.jpgごとのループ
    # 元画像の読み出し
    img = Image.open(path_all[f])
    width, height = img.size
    
    # 分割画像の書き出し
    for i in range(H_DIV):
        for j in range(W_DIV):
            #print(len(new_data[i][j]))
            new_jpg_name = save_dir + "{0:04d}.jpg".format(new_jpg_count)
            # print(new_jpg_name)
            left = int((width / W_DIV ) * j)
            right =  int((width / W_DIV ) * (j + 1))
            upper = int((height / W_DIV ) * i)
            lower = int((height / W_DIV ) * (i + 1))
            #print("left={0}, upper={1}, right={2}, lower={3}".format(left,upper,right,lower))
            img_crop = img.crop((left, upper, right, lower))
            img_crop.save(new_jpg_name, quality=95)
            new_jpg_count += 1    