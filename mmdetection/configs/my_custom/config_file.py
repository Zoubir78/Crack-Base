_base_ = [
    '../_base_/models/mask_rcnn_r50_fpn.py',
    '../_base_/datasets/coco_instance.py',
    '../_base_/schedules/schedule_1x.py', 
    '../_base_/default_runtime.py'
]

# Modification des hyperparamètres
model = dict(
    roi_head=dict(
        bbox_head=dict(num_classes=24),
        mask_head=dict(num_classes=24)
    )
)

dataset_type = 'CocoDataset'
data_root = ''

data = dict(
    train=dict(
        type=dataset_type,
        ann_file='path/to/your/output_coco.json',
        img_prefix='path/to/your/images'),
    val=dict(
        type=dataset_type,
        ann_file='path/to/your/output_coco.json',
        img_prefix='path/to/your/images'),
    test=dict(
        type=dataset_type,
        ann_file='path/to/your/output_coco.json',
        img_prefix='path/to/your/images'))

optimizer = dict(type='SGD', lr=0.02, momentum=0.9, weight_decay=0.0001)
lr_config = dict(
    policy='step',
    warmup=None,
    step=[8, 11])

total_epochs = 12
