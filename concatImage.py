import sys
from PIL import Image, ImageDraw, ImageFont
import os

font = ImageFont.truetype("NotoSerifCJK-Bold.ttc", 96)

open_dir = sys.argv[2]
save_dir = sys.argv[4]
saveImageName = sys.argv[6]
W_DIV = int(sys.argv[8]) # 横分割数
H_DIV = int(sys.argv[10]) # 縦分割数
save_result_txt = sys.argv[12]

detectNumber = 1
txt_count = 1
new_jpg_count = 1
im1 = Image.open(open_dir + "{0:04d}.jpg".format(new_jpg_count))

if os.path.isfile(save_result_txt + "result.txt"):
    os.remove(save_result_txt + "result.txt")

def concat_h(im1, im2):
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst

def concat_w(im1, im2):
    dst = Image.new('RGB', (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst

for h in range(1, W_DIV, 1):
    new_jpg_count += 1
    im2 = Image.open(open_dir + "{0:04d}.jpg".format(new_jpg_count))
    im1 = concat_h(im1, im2)

for i in range(1, W_DIV, 1):
    new_jpg_count += 1
    im3 = Image.open(open_dir + "{0:04d}.jpg".format(new_jpg_count))
    for f in range(1, H_DIV, 1):
        new_jpg_count += 1
        im2 = Image.open(open_dir + "{0:04d}.jpg".format(new_jpg_count))
        im3 = concat_h(im3, im2)
    im1 = concat_w(im1, im3)

for i in range(W_DIV * H_DIV):
    if os.path.isfile(open_dir + "{0:04d}.txt".format(txt_count)):
        sum_y = 0
        sum_x = 0
        with open(open_dir + "{0:04d}.txt".format(txt_count), "r") as f:
            syou, amari= divmod(txt_count, W_DIV)
            # print(txt_count, syou, amari, i)
            for j in range(syou):   # concat height
                jpg_count = txt_count - W_DIV * (j + 1)
                if jpg_count == 0:
                    break
                im1_txt = Image.open(open_dir + "{0:04d}.jpg".format(jpg_count))
                sum_y = sum_y + im1_txt.height
            if amari == 0:    # concat width
                for k in range(H_DIV - 1):
                    jpg_count = txt_count - (k + 1)
                    im2_txt = Image.open(open_dir + "{0:04d}.jpg".format(jpg_count))
                    sum_x = sum_x + im2_txt.width 
            else :
                for k in range(amari - 1):
                    jpg_count = txt_count - (k + 1)
                    im2_txt = Image.open(open_dir + "{0:04d}.jpg".format(jpg_count))
                    sum_x = sum_x + im2_txt.width
            
            while True:
                s_line = f.readline()
                # print(s_line)
                if not s_line:
                    break
                locate = s_line.split()
                x = sum_x + int(locate[0])
                y = sum_y + int(locate[1])
                # print(x)
                # print(y)
                with open(save_result_txt + "result.txt", "a") as resultFile:
                    resultFile.write(str(detectNumber) + " " + str(x) + " " + str(y) + '\n')
                    draw = ImageDraw.Draw(im1)
                    draw.text((x,y), str(detectNumber), (0,0,255), font=font)
                detectNumber += 1
    txt_count += 1


im1.save(save_dir + saveImageName + ".jpg")
print("Concat Image saved to", '\33[1m' + save_dir + saveImageName + ".jpg" + '\033[0m')