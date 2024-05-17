import json
import os
import shutil

root_dir = '/home/lixiang/下载/数据标注-兼职/美丽海淀'
img_dir = os.path.join('/home/lixiang/下载/数据标注-兼职/模型训练/标注')
result_dir = os.path.join('/home/lixiang/下载/数据标注-兼职/模型训练/数据验证')

if not os.path.exists(result_dir):
    os.makedirs(result_dir, exist_ok=True)

for root, dirs, anno_files in os.walk(root_dir):
    for file in anno_files:
        if file.endswith('.json'):
            anno_file = os.path.join(root, file)
            with open(anno_file, 'r') as f:
                anno_json = json.load(f)
                if '\\' in anno_json['imagePath']:
                    anno_json['imagePath'] = anno_json['imagePath'].split('\\')[-1]
                print(os.path.join(result_dir, file))
                with open(os.path.join(result_dir, file), 'w+') as anno_result:
                    json.dump(anno_json, anno_result)
                shutil.copy(os.path.join(img_dir, anno_json['imagePath']), os.path.join(result_dir, anno_json['imagePath']))
                #     print(anno_json)
