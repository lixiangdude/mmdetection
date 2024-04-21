import argparse
import json
import os
import shutil

parser = argparse.ArgumentParser(
    description='Label data verification tool')
parser.add_argument('label_path', help='path of label file')
parser.add_argument('image_path', help='path of image file')
parser.add_argument('result_path', help='path of merged images and labels')
args = parser.parse_args()

if not os.path.exists(args.result_path):
    os.makedirs(args.result_path, exist_ok=True)

file_names = []
for file in os.listdir(args.label_path):
    if file.endswith('.json'):
        anno_file = os.path.join(args.label_path, file)
        with open(anno_file, 'r') as f:
            anno_json = json.load(f)
            if '\\' in anno_json['imagePath']:
                anno_json['imagePath'] = anno_json['imagePath'].split('\\')[-1]
            print(os.path.join(args.result_path, file))
            with open(os.path.join(args.result_path, file), 'w+') as anno_result:
                json.dump(anno_json, anno_result)
        file_names.append(file.split('.')[0])
for file in os.listdir(args.image_path):
    if file.split('.')[0] in file_names:
        img_file = os.path.join(args.image_path, file)
        shutil.copyfile(os.path.join(args.image_path, file), os.path.join(args.result_path, file))