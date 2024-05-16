import os
import shutil

data_root = '/home/lixiang/下载/ossutil-v1.7.19-linux-amd64/美丽海淀图片'
assigment_root = '/home/lixiang/下载/ossutil-v1.7.19-linux-amd64/assigment'
mod = 50

imgs = os.listdir(data_root)

for i in range(mod):
    dir = os.path.join(assigment_root, f'美丽海淀图片_{i + 1}')
    if not os.path.exists(dir):
        os.makedirs(dir, exist_ok=True)

size = int(len(imgs) / mod)

for idx, img in enumerate(imgs):
    img_path = os.path.join(data_root, img)
    assign_path = os.path.join(assigment_root, f'美丽海淀图片_{min(mod, int(idx / size) + 1)}', img)
    shutil.copyfile(img_path, assign_path)
    print(assign_path)
