import os
import json
import shutil

train_img = os.listdir('./train')
val_img = os.listdir('./val')
test_img = os.listdir('./test')
# tempo_img = os.listdir('./tempo')

train_img.remove('DEP')
train_img.remove('annotation_lcms_train.json')
train_img.remove('compteur.csv')

val_img.remove('DEP')
val_img.remove('annotation_lcms_val.json')

test_img.remove('DEP')
test_img.remove('annotation_lcms_test.json')

f = open('./train/annotation_lcms_train.json')
train_ann = json.load(f)
f = open('./val/annotation_lcms_val.json')
val_ann = json.load(f)
f = open('./test/annotation_lcms_test.json')
test_ann = json.load(f)

train_annotee = [img['file_name'] for img in train_ann['images']]
val_annotee = [img['file_name'] for img in val_ann['images']]
test_annotee = [img['file_name'] for img in test_ann['images']]

# n=0
# k=0
# for img in test_annotee:
#     if  img in test_img:
#         #print(img)
#         shutil.move('./val/'+img, './tempo/'+img)
#         shutil.move('./val/DEP/'+img, './tempo/DEP/'+img)
#         n+=1
#     k+=1
# print(n, k)

good_ann = []
for img_ann in test_ann['images']:
    if img_ann['file_name'] in test_img:
        good_ann += [img_ann]

new_ann = dict()
new_ann['annotations'] = []
new_ann['categories'] = test_ann['categories']
new_ann['info'] = test_ann['info']
new_ann['licenses'] = test_ann['licenses']
new_ann['images'] = []

idx = 0
for img_info in good_ann:
    prev_id = img_info['id']
    for ann in test_ann['annotations']:
        if prev_id == ann['image_id']:
            ann['image_id'] = idx
            new_ann['annotations'] += [ann]
    img_info['id'] = idx
    new_ann['images'] += [img_info]
    idx += 1

#print(new_ann.keys())
#print(len(new_ann['annotations']), len(new_ann['images']))

with open("fichier_annoté.json", "w") as fp:
    json.dump(new_ann , fp)