import os
from PIL import Image
import setting


# 画像を任意の数に分割
def split_all_images(
    directory,
    output_dir,
    target_resolution=(setting.img_width, setting.img_height),
    grid_size=(setting.grid_size_width, setting.grid_size_height),
):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for file_name in os.listdir(directory):
        if file_name.lower().endswith((".png", ".jpg", ".jpeg")):
            image_path = os.path.join(directory, file_name)
            with Image.open(image_path) as img:
                # 画像の解像度をチェック
                if img.size == target_resolution:
                    img_width, img_height = img.size
                    tile_width = img_width // grid_size[0]
                    tile_height = img_height // grid_size[1]

                    for i in range(grid_size[0]):  # 横の分割数
                        for j in range(grid_size[1]):  # 縦の分割数
                            left = i * tile_width
                            upper = j * tile_height
                            right = left + tile_width
                            lower = upper + tile_height
                            cropped_img = img.crop((left, upper, right, lower))

                            base_name = os.path.basename(image_path)
                            file_name, file_ext = os.path.splitext(base_name)
                            cropped_img.save(
                                os.path.join(
                                    output_dir,
                                    f"{file_name}_{i * grid_size[1] + j + 1}{file_ext}",
                                )
                            )
