import os
import shutil

data_root = '/home/lixiang/下载/ossutil-v1.7.19-linux-amd64/堆物堆料/堆物堆料'
assigment_root = '/home/lixiang/下载/ossutil-v1.7.19-linux-amd64/assigment'
mod = 4

imgs = os.listdir(data_root)

for i in range(4):
    dir = os.path.join(assigment_root, f'堆物堆料_{i + 1}')
    if not os.path.exists(dir):
        os.makedirs(dir, exist_ok=True)

for idx, img in enumerate(imgs):
    img_path = os.path.join(data_root, img)
    assign_path = os.path.join(assigment_root, f'堆物堆料_{idx % mod + 1}', img)
    shutil.copyfile(img_path, assign_path)
    print(assign_path)
