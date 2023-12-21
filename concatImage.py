import os
from PIL import Image
import setting
import re


def combine_images_and_txt(
    input_dir,
    output_dir,
    original_size=(setting.img_width, setting.img_height),
    grid_size=(setting.grid_size_width, setting.grid_size_height),
):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 正規表現パターンを定義（'数字_数字.jpg'の形式）
    pattern = re.compile(r"\d+_\d+\.jpg")

    for file in os.listdir(input_dir):
        if pattern.match(file):
            base_name = file.split("_")[0]

            # 新しい画像を作成
            new_image = Image.new("RGB", original_size)
            tile_width = original_size[0] // grid_size[0]
            tile_height = original_size[1] // grid_size[1]

            # 合成した物体の位置を記録するためのリスト
            combined_objects = []

            # 画像とテキストファイルの組み合わせを処理
            for i in range(grid_size[0] * grid_size[1]):
                img_path = os.path.join(input_dir, f"{base_name}_{i + 1}.jpg")
                txt_path = os.path.join(input_dir, f"{base_name}_{i + 1}.txt")

                if os.path.exists(img_path):
                    with Image.open(img_path) as tile:
                        x = (i // grid_size[1]) * tile_width  # 列のインデックスに基づくX座標
                        y = (i % grid_size[1]) * tile_height  # 行のインデックスに基づくY座標
                        new_image.paste(tile, (x, y))
                        # テキストファイルがあれば、物体の位置を読み取る
                        if os.path.exists(txt_path):
                            with open(txt_path, "r") as f:
                                for line in f:
                                    obj_x, obj_y = map(int, line.split())
                                    combined_objects.append((obj_x + x, obj_y + y))

            # 画像を保存
            new_image.save(os.path.join(output_dir, f"{base_name}_combine.jpg"))

            # 物体の位置を含むテキストファイルを保存
            if combined_objects:
                with open(
                    os.path.join(output_dir, f"{base_name}_combine.txt"), "w"
                ) as f:
                    for obj_x, obj_y in combined_objects:
                        f.write(f"{obj_x} {obj_y}\n")
