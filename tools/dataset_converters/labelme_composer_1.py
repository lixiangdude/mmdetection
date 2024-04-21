import json
import os
import shutil

root = '/home/lixiang/下载/ossutil-v1.7.19-linux-amd64/人行道路面破损'
image_dir = root
anno_dir = '/home/lixiang/下载/西城指标/人行道路面破损-labelme'
result_dir = '/home/lixiang/下载/西城指标/人行道路面破损-labelme'

if not os.path.exists(result_dir):
    os.makedirs(result_dir, exist_ok=True)

for anno in os.listdir(anno_dir):
    if anno.endswith('.json'):
        anno_file = os.path.join(anno_dir, anno)
        with open(anno_file, 'r') as f:
            anno_json = json.load(f)
            if '\\' in anno_json['imagePath']:
                anno_json['imagePath'] = anno_json['imagePath'].split('\\')[-1]
            with open(os.path.join(result_dir, anno), 'w+') as anno_result:
                json.dump(anno_json, anno_result)
        shutil.copyfile(os.path.join(image_dir, anno.split('.')[0] + '.jpg'), os.path.join(result_dir, anno.split('.')[0] + '.jpg'))
