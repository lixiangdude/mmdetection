import argparse
import json
import os
import random
import shutil

parser = argparse.ArgumentParser(
    description='Label data verification tool')
parser.add_argument('label_path', help='path of label file')
parser.add_argument('image_path', help='path of image file')
parser.add_argument('result_path', help='path of merged images and labels')
args = parser.parse_args()

if not os.path.exists(args.result_path):
    os.makedirs(args.result_path, exist_ok=True)

person_names = ['申神乐', '吴佳慧', '尹力超', '张敏']

for person_name in person_names:
    if not os.path.exists(os.path.join(args.result_path, person_name)):
        os.makedirs(os.path.join(args.result_path, person_name))
    dir_names = [dir_name for dir_name in os.listdir(args.label_path) if person_name in dir_name]
    file_names = []
    for dir_name in dir_names:
        for root, dirs, anno_files in os.walk(os.path.join(args.label_path, dir_name)):
            for file in anno_files:
                if file.endswith('.json'):
                    file_names.append(os.path.join(root, file.split('.')[0]))
    if len(file_names) == 0:
        continue
    file_names = random.sample(file_names, 200)
    anno_file_names = list(map(lambda x: x.split('/')[-1].split('.')[0], file_names))
    for file in os.listdir(args.image_path):
        filename = file.split('.')[0]
        if filename in anno_file_names and 'json' not in filename:
            anno_file = f'{file_names[anno_file_names.index(filename)]}.json'
            with open(anno_file, 'r') as f:
                anno_json = json.load(f)
                if '\\' in anno_json['imagePath']:
                    anno_json['imagePath'] = anno_json['imagePath'].split('\\')[-1]
                print(os.path.join(args.result_path, person_name, f'{filename}.json'))
                with open(os.path.join(args.result_path, person_name, f'{filename}.json'), 'w+') as anno_result:
                    json.dump(anno_json, anno_result)
            img_file = os.path.join(args.image_path, file)
            shutil.copyfile(img_file, os.path.join(args.result_path, person_name, file))
