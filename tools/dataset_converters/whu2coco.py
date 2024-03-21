import json
import os
import shutil
import xml.etree.ElementTree as ET
from PIL import Image
from sklearn.model_selection import train_test_split

categories_dict = {'car': 1, 'crosswalk': 4, 'light': 3, 'traffic_sign': 5, 'warning_line': 2}

data_root = '/home/lixiang/PycharmProjects/mmdetection/data/Omnidirectional Street-view Dataset/equirectangular/'
img_dir = '%sJPEGImages' % data_root
anno_dir = '%sAnnotations' % data_root

img_file_names = [img for img in sorted(os.listdir(img_dir)) if img.endswith('.jpg')]
anno_file_names = [anno for anno in sorted(os.listdir(anno_dir)) if anno.endswith('.xml')]
train_imgs, val_imgs, train_annos, val_annos = train_test_split(img_file_names, anno_file_names, test_size=0.25,
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


def convert_to_coco(xml='/home/lixiang/下载/Omnidirectional Street-view Dataset/DriscollHealy/Annotations/000001.xml'):
    # 解析XML文件并返回ElementTree对象
    tree = ET.parse(xml)
    root = tree.getroot()
    annotations = []
    for obj in root.iter('object'):
        bbox = obj.find('bndbox')
        width = float(bbox.find('xmax').text) - float(bbox.find('xmin').text)
        height = float(bbox.find('ymax').text) - float(bbox.find('ymin').text)
        anno = {
            'iscrowd': 0,
            'category_id': categories_dict[obj.find('name').text],
            'bbox': [float(bbox.find('xmin').text),
                     float(bbox.find('ymin').text),
                     width,
                     height],
            'area': width * height,
            'segmentation': [[]],
            'image_id': int(xml.split('/')[-1].split('.')[0])
        }
        annotations.append(anno)
    return annotations


def get_categories(xml):
    tree = ET.parse(xml)
    root = tree.getroot()
    ctgry_names = set()
    for obj in root.iter('object'):
        ctgry_name = obj.find('name').text
        ctgry_names.add(ctgry_name)
    return ctgry_names


def convert_anno_file(image_files_dir, anno_files_dir, output):
    images = []
    image_names = sorted(os.listdir(image_files_dir))
    for img_name in image_names:
        img_path = os.path.join(image_files_dir, img_name)
        img = Image.open(img_path)
        image = {
            'height': img.height,
            'width': img.width,
            'file_name': img_name,
            'id': int(img_name.replace('.jpg', ''))
        }
        images.append(image)
    categories = []
    for name, ctgry_id in categories_dict.items():
        categories.append({'id': ctgry_id, 'name': name})
    anno_names = sorted(os.listdir(anno_files_dir))
    annotations = []
    for anno_xml in anno_names:
        xml_path = os.path.join(anno_files_dir, anno_xml)
        annotations += convert_to_coco(xml_path)
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
