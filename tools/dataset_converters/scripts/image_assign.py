import os
import shutil

data_root = '/home/lixiang/下载/全景图片切分'
assigment_root = '/home/lixiang/下载/全景图片切分任务分配'
mod = 5

imgs = os.listdir(data_root)

for i in range(mod):
    dir = os.path.join(assigment_root, f'全景图片_{i + 1}')
    if not os.path.exists(dir):
        os.makedirs(dir, exist_ok=True)

size = int(len(imgs) / mod)

for idx, img in enumerate(imgs):
    img_path = os.path.join(data_root, img)
    assign_path = os.path.join(assigment_root, f'全景图片_{min(mod, int(idx / size) + 1)}', img)
    shutil.copyfile(img_path, assign_path)
    print(assign_path)
