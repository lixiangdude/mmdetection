import json
import os
import shutil
import xml.etree.ElementTree as ET
from PIL import Image
from sklearn.model_selection import train_test_split
import cv2

# categories_dict = {'破损': 1, '凹陷': 1, '衣物': 2, '鞋': 2, '垃圾满冒': 3, '乱扔垃圾': 4, '垃圾正常盛放': 5}
# real_ctgry_dict = {1: 'pavement damage', 2: 'drying along the street', 3: 'trash overflow', 4: 'litter', 5: 'normal trash holding'}
categories_dict = {'打包垃圾': 1, '沿街晾晒': 2, '垃圾桶': 3, '晾晒': 2, '井盖': 4}
real_ctgry_dict = {1: 'trash', 2: 'drying along the street', 3: 'trash can', 4: 'manhole cover'}
# real_ctgry_dict = {1: 'broken located on the sidewalk', 2: 'clothes drying on the street', 3: 'trash overflowing out of the garbage cans', 4: 'the garbage that gets thrown around', 5: 'garbage normally placed in garbage cans'}

data_root = '/home/lixiang/下载/模型训练/标注'
result_root = '/home/lixiang/下载/模型训练/data/'
img_dir = data_root
anno_dir = data_root

anno_file_names = [anno for anno in sorted(os.listdir(anno_dir)) if anno.endswith('.json')]
file_prefixs = [anno.split('.')[0] for anno in anno_file_names]
img_file_names = [img for img in sorted(os.listdir(img_dir)) if (img.endswith('.jpg') or img.endswith('jpeg') or img.endswith('png')) and img.split('.')[0] in file_prefixs]
train_imgs, val_imgs, train_annos, val_annos = train_test_split(img_file_names, anno_file_names, test_size=0.2,
                                                                random_state=8)

image_file_dict = {}
for img_file_name in img_file_names:
    image_file_dict[img_file_name.split('.')[0]] = img_file_name

img_train_dir = os.path.join('%simages' % result_root, 'train')
img_val_dir = os.path.join('%simages' % result_root, 'val')
anno_result_dir = '%sannotations' % result_root
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
    imread = cv2.imread(os.path.join(img_dir, train_img))
    cv2.imwrite(os.path.join(img_train_dir, f'{train_img.split(".")[0]}.jpg'), imread)
for val_img in val_imgs:
    imread = cv2.imread(os.path.join(img_dir, val_img))
    cv2.imwrite(os.path.join(img_val_dir, f'{val_img.split(".")[0]}.jpg'), imread)
for train_anno in train_annos:
    shutil.copyfile(os.path.join(anno_dir, train_anno), os.path.join(anno_train_dir, train_anno))
for val_anno in val_annos:
    shutil.copyfile(os.path.join(anno_dir, val_anno), os.path.join(anno_val_dir, val_anno))


def convert_to_coco(img_id, label_file, img):
    with open(label_file, 'r') as f:
        label_json = json.load(f)
    annotations = []
    for shape in label_json['shapes']:
        width = abs(round(shape['points'][1][0], 0) - round(shape['points'][0][0], 0))
        height = abs(round(shape['points'][1][1], 0) - round(shape['points'][0][1], 0))
        if shape['label'] not in categories_dict:
            continue
        # 获取左上角
        x = round(max(0, min(shape['points'][0][0], shape['points'][1][0])), 0)
        y = round(max(0, min(shape['points'][0][1], shape['points'][1][1])), 0)
        anno = {
            'iscrowd': 0,
            'category_id': categories_dict[shape['label']],
            'bbox': [x,
                     y,
                     # 标注框宽度最大不能超过图像宽度
                     min(width, img.width - x),
                     # 标注框高度最大不能超过图像高度
                     min(height, img.height - y)],
            'area': width * height,
            'segmentation': [[]],
            'image_id': img_id
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
    anno_names = sorted(os.listdir(anno_files_dir))
    annotations = []
    for anno_xml, img_name in zip(anno_names, image_names):
        xml_path = os.path.join(anno_files_dir, anno_xml)
        img_path = os.path.join(image_files_dir, img_name)
        img = Image.open(img_path)
        coco_anno = convert_to_coco(image_id, xml_path, img)

        if len(coco_anno) == 0:
            os.remove(os.path.join(anno_files_dir, anno_xml))
            os.remove(os.path.join(image_files_dir, f'{anno_xml.split(".")[0]}.jpg'))
            continue
        annotations += coco_anno

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
    for ctgry_id, name in real_ctgry_dict.items():
        categories.append({'id': ctgry_id, 'name': name})

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
