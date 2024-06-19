model = dict(
    type='MaskRCNN',
    backbone=dict(
        type='ResNet',
        depth=50,
        num_stages=4,
        out_indices=(0, 1, 2, 3),
        frozen_stages=1,
        norm_cfg=dict(type='BN', requires_grad=True),
        norm_eval=True,
        style='pytorch',
        init_cfg=dict(type='Pretrained', checkpoint='torchvision://resnet50')
    ),
    neck=dict(
        type='FPN',
        in_channels=[256, 512, 1024, 2048],
        out_channels=256,
        num_outs=5),
    rpn_head=dict(
        type='RPNHead',
        in_channels=256,
        feat_channels=256,
        anchor_generator=dict(
            type='AnchorGenerator',
            scales=[8],
            ratios=[0.5, 1.0, 2.0],
            strides=[4, 8, 16, 32, 64]),
        bbox_coder=dict(
            type='DeltaXYWHBBoxCoder',
            target_means=[0.0, 0.0, 0.0, 0.0],
            target_stds=[1.0, 1.0, 1.0, 1.0]),
        loss_cls=dict(
            type='CrossEntropyLoss', use_sigmoid=True, loss_weight=1),
        loss_bbox=dict(type='BalancedL1Loss', loss_weight=1)),
    roi_head=dict(
        type='StandardRoIHead',
        bbox_roi_extractor=dict(
            type='SingleRoIExtractor',
            roi_layer=dict(type='RoIAlign', output_size=7, sampling_ratio=0),
            out_channels=256,
            featmap_strides=[4, 8, 16, 32]),
        bbox_head=dict(
            type='Shared2FCBBoxHead',
            in_channels=256,
            fc_out_channels=1024,
            roi_feat_size=7,
            num_classes=24,
            bbox_coder=dict(
                type='DeltaXYWHBBoxCoder',
                target_means=[0.0, 0.0, 0.0, 0.0],
                target_stds=[0.1, 0.1, 0.2, 0.2]),
            reg_class_agnostic=False,
            loss_cls=dict(
                type='CrossEntropyLoss', use_sigmoid=False, loss_weight=1),
            loss_bbox=dict(type='BalancedL1Loss', loss_weight=1)),
        mask_roi_extractor=dict(
            type='SingleRoIExtractor',
            roi_layer=dict(type='RoIAlign', output_size=14, sampling_ratio=0),
            out_channels=256,
            featmap_strides=[4, 8, 16, 32]),
        mask_head=dict(
            type='FCNMaskHead',
            num_convs=4,
            in_channels=256,
            conv_out_channels=256,
            num_classes=24,
            loss_mask=dict(
                type='CrossEntropyLoss', use_mask=True, loss_weight=1.0))),
    train_cfg=dict(
        rpn=dict(
            assigner=dict(
                type='MaxIoUAssigner',
                pos_iou_thr=0.7,
                neg_iou_thr=0.3,
                min_pos_iou=0.3,
                match_low_quality=True,
                ignore_iof_thr=-1),
            sampler=dict(
                type='RandomSampler',
                num=256,
                pos_fraction=0.5,
                neg_pos_ub=-1,
                add_gt_as_proposals=False),
            allowed_border=-1,
            pos_weight=-1,
            debug=False),
        rpn_proposal=dict(
            nms_pre=2000,
            max_per_img=1000,
            nms=dict(type='nms', iou_threshold=0.7),
            min_bbox_size=0),
        rcnn=dict(
            assigner=dict(
                type='MaxIoUAssigner',
                pos_iou_thr=0.5,
                neg_iou_thr=0.5,
                min_pos_iou=0.5,
                match_low_quality=True,
                ignore_iof_thr=-1),
            sampler=dict(
                type='RandomSampler',
                num=512,
                pos_fraction=0.25,
                neg_pos_ub=-1,
                add_gt_as_proposals=True),
            mask_size=28,
            pos_weight=-1,
            debug=False)),
    test_cfg=dict(
        rpn=dict(
            nms_pre=1000,
            max_per_img=1000,
            nms=dict(type='nms', iou_threshold=0.7),
            min_bbox_size=0),
        rcnn=dict(
            score_thr=0.05,
            nms=dict(type='nms', iou_threshold=0.5),
            max_per_img=100,
            mask_thr_binary=0.5)))
dataset_type = 'CocoDataset'
data_root = 'data/coco/'
img_norm_cfg = dict(
    mean=[123.675, 116.28, 103.53], std=[58.395, 57.12, 57.375], to_rgb=True)
albu_train_transforms = [
    dict(
        type='GaussNoise',
        var_limit=(20.0, 60.0),
        mean=0,
        per_channel=False,
        p=0.9),
    dict(
        type='RandomBrightnessContrast',
        brightness_limit=[-0.2, 0.2],
        contrast_limit=[-0.25, 0.25],
        p=1.0),
    dict(
        type='OneOf',
        transforms=[
            dict(type='Blur', blur_limit=(3, 5), p=1.0),
            dict(type='MedianBlur', blur_limit=(3, 5), p=1.0)
        ],
        p=0.3),
    dict(
        type='ShiftScaleRotate',
        shift_limit=0.1,
        scale_limit=(-0.3, 0.8),
        rotate_limit=10,
        interpolation=1,
        border_mode=0,
        value=0,
        p=1),
    dict(type='ImageCompression', quality_lower=30, quality_upper=50, p=0.95)
]
train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='LoadAnnotations', with_bbox=True, with_mask=True),
    dict(type='Resize', img_scale=(864, 992), keep_ratio=False),
    dict(
        type='Normalize',
        mean=[123.675, 116.28, 103.53],
        std=[58.395, 57.12, 57.375],
        to_rgb=True),
    dict(type='Pad', size_divisor=32),
    dict(type='DefaultFormatBundle'),
    dict(
        type='Collect',
        keys=['img', 'jet', 'gt_bboxes', 'gt_labels', 'gt_masks'])
]
test_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(
        type='MultiScaleFlipAug',
        img_scale=(864, 992),
        flip=False,
        transforms=[
            dict(type='Resize', keep_ratio=False),
            dict(
                type='Normalize',
                mean=[123.675, 116.28, 103.53],
                std=[58.395, 57.12, 57.375],
                to_rgb=True),
            dict(type='Pad', size_divisor=32),
            dict(type='DefaultFormatBundle'),
            dict(type='Collect', keys=['img', 'jet'])
        ])
]
data = dict(
    samples_per_gpu=1,
    workers_per_gpu=1,
    train=dict(
        type='RepeatDataset',
        times=3,
        dataset=dict(
            type='CocoDataset',
            ann_file=
            'C:/Users/nathan.sikora/Desktop/Stagenathan/mmdetection_deep/configs/my_custom/grap/train/DEP/annotation_lcms_train.json',
            img_prefix=
            'C:/Users/nathan.sikora/Desktop/Stagenathan/mmdetection_deep/configs/my_custom/grap/train',
            pipeline=[
                dict(type='LoadImageFromFile'),
                dict(type='LoadAnnotations', with_bbox=True, with_mask=True),
                dict(type='RandomFlip', flip_ratio=0.5),
                dict(
                    type='Albu',
                    transforms=[
                        dict(
                            type='GaussNoise',
                            var_limit=(20.0, 60.0),
                            mean=0,
                            per_channel=False,
                            p=0.9),
                        dict(
                            type='RandomBrightnessContrast',
                            brightness_limit=[-0.2, 0.2],
                            contrast_limit=[-0.25, 0.25],
                            p=1.0),
                        dict(
                            type='OneOf',
                            transforms=[
                                dict(type='Blur', blur_limit=(3, 5), p=1.0),
                                dict(
                                    type='MedianBlur',
                                    blur_limit=(3, 5),
                                    p=1.0)
                            ],
                            p=0.3),
                        dict(
                            type='ShiftScaleRotate',
                            shift_limit=0.1,
                            scale_limit=(-0.3, 0.8),
                            rotate_limit=10,
                            interpolation=1,
                            border_mode=0,
                            value=0,
                            p=1),
                        dict(
                            type='ImageCompression',
                            quality_lower=30,
                            quality_upper=50,
                            p=0.95)
                    ],
                    bbox_params=dict(
                        type='BboxParams',
                        format='pascal_voc',
                        label_fields=['gt_labels'],
                        min_visibility=0.04,
                        filter_lost_elements=True),
                    keymap=dict(
                        img='image', gt_masks='masks', gt_bboxes='bboxes'),
                    update_pad_shape=False,
                    skip_img_without_anno=True),
                dict(type='Resize', img_scale=(850, 1000), keep_ratio=True),
                dict(
                    type='Normalize',
                    mean=[123.675, 116.28, 103.53],
                    std=[58.395, 57.12, 57.375],
                    to_rgb=True),
                dict(type='Pad', size_divisor=32),
                dict(type='DefaultFormatBundle'),
                dict(
                    type='Collect',
                    keys=['img', 'jet', 'gt_bboxes', 'gt_labels', 'gt_masks'])
            ],
            jet_prefix=
            'C:/Users/nathan.sikora/Desktop/Stagenathan/mmdetection_deep/configs/my_custom/grap/train/DEP',
            classes=('non_classee', 'cable', 'passe_cable', 'lumiere', 'joint',
                     'camera', 'prisme_sos_telephone', 'bouche_incendie',
                     'reflecteur', 'prisme_issue_en_face',
                     'indication_issue_de_secours', 'plaque_numerotee',
                     'issue_de_secours', 'plaque_anneau', 'indication_id_sos',
                     'issue_sos_telephone', 'panneau_signalisation',
                     'coffrage', 'boitier_elec', 'non_definie_1',
                     'non_definie_2', 'non_definie_3', 'non_definie_4',
                     'non_definie_5')),
        pipeline=[
            dict(type='LoadImageFromFile'),
            dict(type='LoadAnnotations', with_bbox=True, with_mask=True),
            dict(type='Resize', img_scale=(864, 992), keep_ratio=False),
            dict(
                type='Normalize',
                mean=[123.675, 116.28, 103.53],
                std=[58.395, 57.12, 57.375],
                to_rgb=True),
            dict(type='Pad', size_divisor=32),
            dict(type='DefaultFormatBundle'),
            dict(
                type='Collect',
                keys=['img', 'jet', 'gt_bboxes', 'gt_labels', 'gt_masks'])
        ]),
    val=dict(
        type='CocoDataset',
        ann_file=
        'C:/Users/nathan.sikora/Desktop/Stagenathan/mmdetection_deep/configs/my_custom/grap/val/annotation_lcms_val.json',
        img_prefix=
        'C:/Users/nathan.sikora/Desktop/Stagenathan/mmdetection_deep/configs/my_custom/grap/val/',
        pipeline=[
            dict(type='LoadImageFromFile'),
            dict(
                type='MultiScaleFlipAug',
                img_scale=(864, 992),
                flip=False,
                transforms=[
                    dict(type='Resize', keep_ratio=False),
                    dict(
                        type='Normalize',
                        mean=[123.675, 116.28, 103.53],
                        std=[58.395, 57.12, 57.375],
                        to_rgb=True),
                    dict(type='Pad', size_divisor=32),
                    dict(type='DefaultFormatBundle'),
                    dict(type='Collect', keys=['img', 'jet'])
                ])
        ],
        jet_prefix=
        'C:/Users/nathan.sikora/Desktop/Stagenathan/mmdetection_deep/configs/my_custom/grap/val/DEP',
        classes=('non_classee', 'cable', 'passe_cable', 'lumiere', 'joint',
                 'camera', 'prisme_sos_telephone', 'bouche_incendie',
                 'reflecteur', 'prisme_issue_en_face',
                 'indication_issue_de_secours', 'plaque_numerotee',
                 'issue_de_secours', 'plaque_anneau', 'indication_id_sos',
                 'issue_sos_telephone', 'panneau_signalisation', 'coffrage',
                 'boitier_elec', 'non_definie_1', 'non_definie_2',
                 'non_definie_3', 'non_definie_4', 'non_definie_5')),
    test=dict(
        type='CocoDataset',
        ann_file=
        'C:/Users/nathan.sikora/Desktop/Stagenathan/mmdetection_deep/configs/my_custom/grap/test/annotation_lcms_test.json',
        img_prefix=
        'C:/Users/nathan.sikora/Desktop/Stagenathan/mmdetection_deep/configs/my_custom/grap/test/',
        pipeline=[
            dict(type='LoadImageFromFile'),
            dict(
                type='MultiScaleFlipAug',
                img_scale=(864, 992),
                flip=False,
                transforms=[
                    dict(type='Resize', keep_ratio=False),
                    dict(
                        type='Normalize',
                        mean=[123.675, 116.28, 103.53],
                        std=[58.395, 57.12, 57.375],
                        to_rgb=True),
                    dict(type='Pad', size_divisor=32),
                    dict(type='DefaultFormatBundle'),
                    dict(type='Collect', keys=['img', 'jet'])
                ])
        ],
        jet_prefix=
        'C:/Users/nathan.sikora/Desktop/Stagenathan/mmdetection_deep/configs/my_custom/grap/test/DEP',
        classes=('non_classee', 'cable', 'passe_cable', 'lumiere', 'joint',
                 'camera', 'prisme_sos_telephone', 'bouche_incendie',
                 'reflecteur', 'prisme_issue_en_face',
                 'indication_issue_de_secours', 'plaque_numerotee',
                 'issue_de_secours', 'plaque_anneau', 'indication_id_sos',
                 'issue_sos_telephone', 'panneau_signalisation', 'coffrage',
                 'boitier_elec', 'non_definie_1', 'non_definie_2',
                 'non_definie_3', 'non_definie_4', 'non_definie_5')))
optimizer = dict(type='SGD', lr=0.004, momentum=0.9, weight_decay=0.0001)
optimizer_config = dict(grad_clip=None)
lr_config = dict(
    policy='step',
    warmup='linear',
    warmup_iters=500,
    warmup_ratio=0.0001,
    step=[5, 10, 15, 20, 40, 60, 100],
    gamma=0.8)
runner = dict(type='EpochBasedRunner', max_epochs=1000)
checkpoint_config = dict(interval=1)
log_config = dict(interval=120, hooks=[dict(type='TextLoggerHook')])
custom_hooks = [dict(type='NumClassCheckHook')]
dist_params = dict(backend='nccl')
log_level = 'INFO'
load_from = 'C:/Users/nathan.sikora/Desktop/Stagenathan/mmdetection_deep/checkpoints/resnet152-394f9c45.pth'
resume_from = None
workflow = [('train', 1)]
opencv_num_threads = 0
mp_start_method = 'fork'
auto_scale_lr = dict(enable=False, base_batch_size=16)
classes = ('non_classee', 'cable', 'passe_cable', 'lumiere', 'joint', 'camera',
           'prisme_sos_telephone', 'bouche_incendie', 'reflecteur',
           'prisme_issue_en_face', 'indication_issue_de_secours',
           'plaque_numerotee', 'issue_de_secours', 'plaque_anneau',
           'indication_id_sos', 'issue_sos_telephone', 'panneau_signalisation',
           'coffrage', 'boitier_elec', 'non_definie_1', 'non_definie_2',
           'non_definie_3', 'non_definie_4', 'non_definie_5')
evaluation = dict(metric=['bbox', 'segm'])
work_dir = './work_dirs\my_custom_config_1'
auto_resume = True
gpu_ids = [0]
