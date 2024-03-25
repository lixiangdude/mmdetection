import json
import os
import shutil
import xml.etree.ElementTree as ET
from PIL import Image
from sklearn.model_selection import train_test_split

categories_dict = {'汽车': 1, '交通标志': 4, '路灯': 3, '广告牌': 2}

data_root = '/home/lixiang/PycharmProjects/mmdetection/data/tsingyan/'
img_dir = data_root
anno_dir = data_root

img_file_names = [img for img in sorted(os.listdir(img_dir)) if img.endswith('.png')]
anno_file_names = [anno for anno in sorted(os.listdir(anno_dir)) if anno.endswith('.json')]
train_imgs, val_imgs, train_annos, val_annos = train_test_split(img_file_names, anno_file_names, test_size=0.5,
                                                                random_state=8)

img_train_dir = os.path.join('%simages' % data_root, 'train')
img_val_dir = os.path.join('%simages' % data_root, 'val')
anno_result_dir = '%sannotations' % data_root
anno_train_dir = os.path.join(anno_result_dir, 'train')
anno_val_dir = os.path.join(anno_result_dir, 'val')

if not os.path.exists(img_train_dir):
    os.makedirs(img_train_dir)
if not os.path.exists(img_val_dir):
    os.makedirs(img_val_dir)
if not os.path.exists(anno_train_dir):
    os.makedirs(anno_train_dir)
if not os.path.exists(anno_val_dir):
    os.makedirs(anno_val_dir)

for train_img in train_imgs:
    shutil.copyfile(os.path.join(img_dir, train_img), os.path.join(img_train_dir, train_img))
for val_img in val_imgs:
    shutil.copyfile(os.path.join(img_dir, val_img), os.path.join(img_val_dir, val_img))
for train_anno in train_annos:
    shutil.copyfile(os.path.join(anno_dir, train_anno), os.path.join(anno_train_dir, train_anno))
for val_anno in val_annos:
    shutil.copyfile(os.path.join(anno_dir, val_anno), os.path.join(anno_val_dir, val_anno))


def convert_to_coco(img_id_dict, label_file):
    with open(label_file, 'r') as f:
        label_json = json.load(f)
    annotations = []
    for shape in label_json['shapes']:
        width = abs(round(shape['points'][1][0], 0) - round(shape['points'][0][0], 0))
        height = abs(round(shape['points'][1][1], 0) - round(shape['points'][0][1], 0))
        anno = {
            'iscrowd': 0,
            'category_id': categories_dict[shape['label']],
            'bbox': [round(shape['points'][0][0], 0),
                     round(shape['points'][0][1], 0),
                     width,
                     height],
            'area': width * height,
            'segmentation': [[]],
            'image_id': img_id_dict[label_file.split('/')[-1].split('.')[0]]
        }
        annotations.append(anno)
    return annotations


def get_categories(label_file):
    with open(label_file, 'r') as f:
        label_json = json.load(f)
    ctgry_names = set()
    for shape in label_json['shapes']:
        ctgry_name = shape['label']
        ctgry_names.add(ctgry_name)
    return ctgry_names


def convert_anno_file(image_files_dir, anno_files_dir, output):
    images = []
    image_names = sorted(os.listdir(image_files_dir))
    image_id = 0
    img_id_dict = {}
    for img_name in image_names:
        img_path = os.path.join(image_files_dir, img_name)
        img = Image.open(img_path)
        image = {
            'height': img.height,
            'width': img.width,
            'file_name': img_name,
            'id': image_id
        }
        images.append(image)
        img_id_dict[img_name.split('.')[0]] = image_id
        image_id += 1
    categories = []
    for name, ctgry_id in categories_dict.items():
        categories.append({'id': ctgry_id, 'name': name})
    anno_names = sorted(os.listdir(anno_files_dir))
    annotations = []
    for anno_xml in anno_names:
        xml_path = os.path.join(anno_files_dir, anno_xml)
        annotations += convert_to_coco(img_id_dict, xml_path)
    for idx, annotation in enumerate(annotations):
        annotation['id'] = idx
    result = {
        'images': images,
        'categories': categories,
        'annotations': annotations
    }
    print(json.dumps(result))
    with open(output, 'w') as f:
        f.write(json.dumps(result))


convert_anno_file(img_train_dir, anno_train_dir, os.path.join(anno_result_dir, 'annotations_train.json'))
convert_anno_file(img_val_dir, anno_val_dir, os.path.join(anno_result_dir, 'annotations_val.json'))
