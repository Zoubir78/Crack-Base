_base_ = 'mask_rcnn_r50_fpn_1x_coco_grap.py'
#_base_ = r'mask_rcnn/mask_rcnn_x101_32x8d_fpn_mstrain-poly_3x_coco.py'
img_norm_cfg = dict(
    mean=[123.675, 116.28, 103.53], std=[58.395, 57.12, 57.375], to_rgb=True)

model = dict(

rpn_head=dict(
        type='RPNHead',
        in_channels=256,
        feat_channels=256,
        anchor_generator=dict(
            type='AnchorGenerator',
            scales=[8],
            ratios=[0.05, 0.1, 0.2, 0.5, 1.0, 2.0],
            strides=[4, 8, 16, 32, 64]),
        bbox_coder=dict(
            type='DeltaXYWHBBoxCoder',
            target_means=[0.0, 0.0, 0.0, 0.0],
            target_stds=[1.0, 1.0, 1.0, 1.0]),
        loss_cls=dict(
            type='CrossEntropyLoss', use_sigmoid=True, loss_weight=1.0),
        loss_bbox=dict(type='BalancedL1Loss', loss_weight=1.0)),
        
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
                type='CrossEntropyLoss', use_sigmoid=False, loss_weight=1.0),
            loss_bbox=dict(type='BalancedL1Loss', loss_weight=1.0)),
            
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
            mask_thr_binary=0.5)) 
)

albu_train_transforms = [
    # dict(
    #     type='GaussNoise',
    #     var_limit=(2e1, 6e1),
    #     mean=0,
    #     per_channel=False,
    #     p=0.9
    # ),
    # dict(
    #     type='RandomBrightnessContrast',
    #     brightness_limit=[-0.20, 0.20],
    #     contrast_limit=[-0.25, 0.25],
    #     p=1.0),
    #dict(type='ChannelShuffle', p=0.1),
    # dict(
    #     type='OneOf',
    #     transforms=[
    #         dict(type='Blur', blur_limit=(3, 5), p=1.0),
    #         dict(type='MedianBlur', blur_limit=(3, 5), p=1.0)
    #     ],
    #     p=0.3),
    # dict(
    #     type='ShiftScaleRotate',
    #     shift_limit=0.1,
    #     scale_limit=(-0.3, 0.8),
    #     rotate_limit=10,
    #     interpolation=1,
    #     border_mode=0,
    #     value=0,
    #     p=1),
    # dict(type='ImageCompression', quality_lower=30, quality_upper=50, p=0.95),
]

train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='LoadAnnotations', with_bbox=True, with_mask=True),
    # dict(type='RandomFlip', flip_ratio=0.5),
    # dict(
    #     type='Albu',
    #     transforms=albu_train_transforms,
    #     bbox_params=dict(
    #         type='BboxParams',
    #         format='pascal_voc',
    #         label_fields=['gt_labels'],
    #         min_visibility=0.04,
    #         filter_lost_elements=True),
    #     keymap={
    #         'img': 'image',
    #         'gt_masks': 'masks',
    #         'gt_bboxes': 'bboxes'
    #     },
    #     update_pad_shape=False,
    #     skip_img_without_anno=True),
    dict(type='Resize', img_scale=(864, 992), keep_ratio=False),
    dict(type='Normalize', **img_norm_cfg),
    dict(type='Pad', size_divisor=32),
    dict(type='DefaultFormatBundle'),
    dict(type='Collect', keys=['img', 'jet', 'gt_bboxes', 'gt_labels', 'gt_masks']),
]
test_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(
        type='MultiScaleFlipAug',
        img_scale=(864, 992),
        flip=False,
        transforms=[
            dict(type='Resize', keep_ratio=False),
            #dict(type='RandomFlip'),
            dict(type='Normalize', **img_norm_cfg),
            dict(type='Pad', size_divisor=32),
            dict(type='DefaultFormatBundle'), # Image to tensor, keys=['img','jet']),
            dict(type='Collect', keys=['img','jet', 'gt_bboxes', 'gt_labels', 'gt_masks']),
        ])
]

dataset_type = 'CocoDataset' 
classes = ('non_classee', 'cable',
           'passe_cable', 'lumiere',
           'joint', 'camera',
           'prisme_sos_telephone', 'bouche_incendie',
           'reflecteur', 'prisme_issue_en_face',
           'indication_issue_de_secours', 'plaque_numerotee',
           'issue_de_secours', 'plaque_anneau',
           'indication_id_sos', 'issue_sos_telephone',
           'panneau_signalisation', 'coffrage',
           'boitier_elec', 'non_definie_1',
           'non_definie_2', 'non_definie_3',
           'non_definie_4', 'non_definie_5')  


data = dict(
    samples_per_gpu=1,  
    workers_per_gpu=1,  


    train=dict(
        type='RepeatDataset',
        times=3,
        dataset=dict(
            img_prefix='C:/Users/nathan.sikora/Desktop/Stageflorian/LCMS_mmdetect/newdataset_Florian_test6/train',  
            jet_prefix = 'C:/Users/nathan.sikora/Desktop/Stageflorian/LCMS_mmdetect/newdataset_Florian_test6/train',
            classes=classes,
            ann_file='C:/Users/nathan.sikora/Desktop/Stageflorian/LCMS_mmdetect/newdataset_Florian_test6/train/annotation_lcms_train.json'),
            pipeline = train_pipeline),  

    # train=dict(
    #     type='RepeatDataset',
    #     times=3,
    #     dataset=dict(
    #         img_prefix='C:/Users/nathan.sikora/Desktop/Stagenathan/mmdetection_deep/configs/my_custom/grap/train',  
    #         jet_prefix = 'C:/Users/nathan.sikora/Desktop/Stagenathan/mmdetection_deep/configs/my_custom/grap/train/DEP',
    #         classes=classes,
    #         ann_file='C:/Users/nathan.sikora/Desktop/Stagenathan/mmdetection_deep/configs/my_custom/grap/train/DEP/annotation_lcms_train.json'),
    #         pipeline = train_pipeline), 

    val=dict(
        img_prefix='C:/Users/nathan.sikora/Desktop/Stageflorian/LCMS_mmdetect/newdataset_Florian_test6/val/',  
        jet_prefix = 'C:/Users/nathan.sikora/Desktop/Stageflorian/LCMS_mmdetect/newdataset_Florian_test6/val/',
        classes=classes,
        ann_file='C:/Users/nathan.sikora/Desktop/Stageflorian/LCMS_mmdetect/newdataset_Florian_test6/val/annotation_lcms_val.json',
        pipeline=test_pipeline),  

    # val=dict(
    #     img_prefix='C:/Users/nathan.sikora/Desktop/Stagenathan/mmdetection_deep/configs/my_custom/grap/val/',  
    #     jet_prefix = 'C:/Users/nathan.sikora/Desktop/Stagenathan/mmdetection_deep/configs/my_custom/grap/val/DEP',
    #     classes=classes,
    #     ann_file='C:/Users/nathan.sikora/Desktop/Stagenathan/mmdetection_deep/configs/my_custom/grap/val/annotation_lcms_val.json',
    #     pipeline=test_pipeline), 
    
    test=dict(
        img_prefix='C:/Users/nathan.sikora/Desktop/Stageflorian/LCMS_mmdetect/newdataset_Florian_test6/test/',  
        jet_prefix = 'C:/Users/nathan.sikora/Desktop/Stageflorian/LCMS_mmdetect/newdataset_Florian_test6/test/',
        classes=classes,
        ann_file='C:/Users/nathan.sikora/Desktop/Stageflorian/LCMS_mmdetect/newdataset_Florian_test6/test/annotation_lcms_test.json',
        pipeline=test_pipeline))  

        # test=dict(
        # img_prefix='C:/Users/nathan.sikora/Desktop/Stagenathan/mmdetection_deep/configs/my_custom/grap/val/',  
        # jet_prefix = 'C:/Users/nathan.sikora/Desktop/Stagenathan/mmdetection_deep/configs/my_custom/grap/val/DEP',
        # classes=classes,
        # ann_file='C:/Users/nathan.sikora/Desktop/Stagenathan/mmdetection_deep/configs/my_custom/grap/val/annotation_lcms_val.json',
        # pipeline=test_pipeline))


 



optimizer = dict(type='SGD', lr=4e-3, momentum=0.9, weight_decay=1e-4)
optimizer_config = dict(grad_clip=None)
runner = dict(type='EpochBasedRunner', max_epochs=350)
log_config = dict(
    interval=120,
    hooks=[
        dict(type='TextLoggerHook'),
        #dict(type='TensorboardLoggerHook'),
    ])

lr_config = dict(
    policy='step',
    warmup='linear',
    warmup_iters=100,
    warmup_ratio=1e-4,
    gamma=0.8,
    step=[5, 10, 15, 20, 40, 60, 100])
evaluation = dict(metric=['bbox', 'segm'])
workflow = [('train', 1)]#, ('val', 1)]
load_from = 'C:/Users/nathan.sikora/Desktop/Stageflorian/LCMS_mmdetect/configs/checkpoints/mask_rcnn_x101_32x8d_fpn_mstrain-poly_3x_coco_20210607_161042-8bd2c639.pth'