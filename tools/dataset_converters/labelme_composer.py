import json
import os
import shutil

root = '/home/lixiang/下载/路灯'
image_dir = os.path.join(root, '路灯损坏', '路灯损坏')
anno_dir = os.path.join(root, '已打标')
result_dir = os.path.join(root, 'data')

if not os.path.exists(result_dir):
    os.makedirs(result_dir, exist_ok=True)

for anno in os.listdir(anno_dir):
    anno_file = os.path.join(anno_dir, anno)
    with open(anno_file, 'r') as f:
        anno_json = json.load(f)
        if '\\' in anno_json['imagePath']:
            anno_json['imagePath'] = anno_json['imagePath'].split('\\')[-1]
        with open(os.path.join(result_dir, anno), 'w+') as anno_result:
            json.dump(anno_json, anno_result)
    shutil.copyfile(os.path.join(image_dir, anno.split('.')[0] + '.jpg'), os.path.join(result_dir, anno.split('.')[0] + '.jpg'))
