import sys
import functools
import cv2
import glob
import os
import os.path as osp
import imgviz
import html
import json
import math
import argparse
import numpy as np
import tempfile
import torch
import base64
import subprocess
from segment_anything import SamPredictor, sam_model_registry
from segment_anything.utils.transforms import ResizeLongestSide

from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QApplication, QPushButton, QLabel, QFileDialog, QProgressBar, QComboBox, QScrollArea, QDockWidget, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon, QImage
from PyQt5.Qt import QSize
from qtpy.QtCore import Qt
from qtpy import QtCore
from qtpy import QtGui, QtWidgets
from canvas import Canvas
import utils
from utils.download_model import download_model

from labelme.widgets import ToolBar, UniqueLabelQListWidget, LabelDialog, LabelListWidget, LabelListWidgetItem, ZoomWidget
from labelme import PY2
from labelme.label_file import LabelFile
from labelme.label_file import LabelFileError


from shape import Shape

from PIL import Image

from collections import namedtuple
Click = namedtuple('Click', ['is_positive', 'coords'])

from segment_anything import sam_model_registry, SamPredictor





LABEL_COLORMAP = imgviz.label_colormap()

class MainWindow(QMainWindow):

    FIT_WINDOW, FIT_WIDTH, MANUAL_ZOOM = 0, 1, 2

    def __init__(self, parent=None, global_w=1000, global_h=1800, model_type='vit_b', keep_input_size=True, max_size=1080):
        super(MainWindow, self).__init__(parent)
        self.resize(global_w, global_h)
        self.model_type = model_type
        self.keep_input_size = keep_input_size
        self.max_size = float(max_size)

        self.image_id = 1
        self.annotation_id = 1
        self.all_annotations = {"images": [], "annotations": [], "categories": self.get_categories()}
        self.category_list = [cat["name"] for cat in self.all_annotations["categories"]]
        self.current_output_dir = None
        self.current_output_filename = None
        self.current_img_index = 0
        self.img_len = 0
        self.img_list = []
        self.raw_h = 0
        self.raw_w = 0
        self.current_img = None
        self.dirty = False
        self.class_on_flag = False

        self.setWindowTitle('SAM')
        self.canvas = Canvas(self,
            epsilon=10.0,
            double_click='close',
            num_backups=10,
            app=self,
        )

        
        self._noSelectionSlot = False
        self.current_output_dir = 'output'
        os.makedirs(self.current_output_dir, exist_ok=True)
        self.current_output_filename = ''
        self.canvas.zoomRequest.connect(self.zoomRequest)

        self.memory_shapes = []
        self.sam_mask = []
        self.sam_mask_proposal = []
        self.image_encoded_flag = False
        self.min_point_dis = 4

        self.predictor = None

        self.scroll_values = {
            Qt.Horizontal: {},
            Qt.Vertical: {},
        }
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidget(self.canvas)
        self.scrollArea.setWidgetResizable(True)
        self.scrollBars = {
            Qt.Vertical: self.scrollArea.verticalScrollBar(),
            Qt.Horizontal: self.scrollArea.horizontalScrollBar(),
        }
        self.canvas.scrollRequest.connect(self.scrollRequest)
        self.canvas.newShape.connect(self.newShape)
        self.canvas.shapeMoved.connect(self.setDirty)
        self.canvas.selectionChanged.connect(self.shapeSelectionChanged)
        self.canvas.drawingPolygon.connect(self.toggleDrawingSensitive)

        self.uniqLabelList = UniqueLabelQListWidget()
        self.uniqLabelList.setToolTip(
            self.tr(
                "Select label to start annotating for it. "
                "Press 'Esc' to deselect."
            )
        )
        self.labelDialog = LabelDialog(
            parent=self,
            labels=[],
            sort_labels=False,
            show_text_field=True,
            completion='contains',
            fit_to_content={'column': True, 'row': False},
        )

        self.labelList = LabelListWidget()
        self.labelList.itemSelectionChanged.connect(self.labelSelectionChanged)
        self.labelList.itemDoubleClicked.connect(self.editLabel)
        self.labelList.itemChanged.connect(self.labelItemChanged)
        self.labelList.itemDropped.connect(self.labelOrderChanged)

        self.shape_dock = QDockWidget(
            self.tr("Polygon Labels"), self
        )
        self.shape_dock.setObjectName("Labels")
        self.shape_dock.setWidget(self.labelList)

        self.category_list = [i.strip() for i in open(r'C:\Users\z.marouf-araibi\Desktop\Crack-Base\classes.csv', 'r', encoding='utf-8').readlines()]
        self.labelDialog = LabelDialog(
            parent=self,
            labels=self.category_list,
            sort_labels=False,
            show_text_field=True,
            completion='contains',
            fit_to_content={'column': True, 'row': False},
        )
        self.zoom_values = {}
        self.video_directory = ''
        self.video_list = []
        self.video_len = len(self.video_list)

        self.img_list = []
        self.img_len = len(self.img_list)
        self.current_img_index = 0
        self.current_img = ''
        self.current_img_data = ''

        self.button_next = QPushButton('Image suivante', self)
        self.button_next.clicked.connect(self.clickButtonNext)
        self.button_last = QPushButton('Image précédente', self)
        self.button_last.clicked.connect(self.clickButtonLast)

        self.img_progress_bar = QProgressBar(self)
        self.img_progress_bar.setMinimum(0)
        self.img_progress_bar.setMaximum(1)
        self.img_progress_bar.setValue(0)
        self.button_proposal1 = QPushButton('Proposition 1', self)
        self.button_proposal1.clicked.connect(self.choose_proposal1)
        self.button_proposal1.setShortcut('1')
        self.button_proposal2 = QPushButton('Proposition 2', self)
        self.button_proposal2.clicked.connect(self.choose_proposal2)
        self.button_proposal2.setShortcut('2')
        self.button_proposal3 = QPushButton('Proposition 3', self)
        self.button_proposal3.clicked.connect(self.choose_proposal3)
        self.button_proposal3.setShortcut('3')
        self.button_proposal4 = QPushButton('Proposition 4', self)
        self.button_proposal4.clicked.connect(self.choose_proposal4)
        self.button_proposal4.setShortcut('4')
        self.button_proposal_list = [self.button_proposal1, self.button_proposal2, self.button_proposal3, self.button_proposal4]
        
        self.class_on_flag = True
        self.class_on_text = QLabel("Classe : On", self)
        

        #naive layout
        self.scrollArea.move(int(0.02 * global_w), int(0.08 * global_h))
        self.scrollArea.resize(int(0.75 * global_w), int(0.7 * global_h))
        self.shape_dock.move(int(0.79 * global_w), int(0.08 * global_h))
        self.shape_dock.resize(int(0.2 * global_w), int(0.7 * global_h))
        self.button_next.move(int(0.18 * global_w), int(0.85 * global_h))
        self.button_next.resize(int(0.1 * global_w),int(0.04 * global_h))
        self.button_last.move(int(0.01 * global_w), int(0.85 * global_h))
        self.button_last.resize(int(0.1 * global_w),int(0.04 * global_h))
        self.class_on_text.move(int(0.01 * global_w), int(0.9 * global_h))
        self.img_progress_bar.move(int(0.01 * global_w), int(0.8 * global_h))
        self.img_progress_bar.resize(int(0.3 * global_w),int(0.04 * global_h))
        
        self.button_proposal1.resize(int(0.17 * global_w),int(0.14 * global_h))
        self.button_proposal1.move(int(0.33 * global_w), int(0.8 * global_h))
        self.button_proposal2.resize(int(0.17 * global_w),int(0.14 * global_h))
        self.button_proposal2.move(int(0.50 * global_w), int(0.8 * global_h))
        self.button_proposal3.resize(int(0.17 * global_w),int(0.14 * global_h))
        self.button_proposal3.move(int(0.67 * global_w), int(0.8 * global_h))
        self.button_proposal4.resize(int(0.17 * global_w),int(0.14 * global_h))
        self.button_proposal4.move(int(0.84 * global_w), int(0.8 * global_h))
        
        
        
        self.zoomWidget = ZoomWidget()

        action = functools.partial(utils.newAction, self)
        

        categoryFile = action(
            self.tr("Catégories"),
            lambda: self.clickCategoryChoose(),
            'None',
            "objects",
            self.tr("Catégories"),
            enabled=True,
        )
        imageDirectory = action(
            self.tr("Dossier d'images"),
            lambda: self.clickFileChoose(),
            'None',
            "objects",
            self.tr("Répertoire d'images"),
            enabled=True,
        )
        LoadSAM = action(
            self.tr("Charger SAM"),
            lambda: self.clickLoadSAM(),
            'None',
            "objects",
            self.tr("Charger SAM"),
            enabled=True,
        )
        AutoSeg = action(
            self.tr("AutoSeg"),
            lambda: self.clickAutoSeg(),
            'None',
            "objects",
            self.tr("AutoSeg"),
            enabled=True,
        )
        promptSeg = action(
            self.tr("Accepter"),
            lambda: self.addSamMask(),
            'a',
            "objects",
            self.tr("Accepter"),
            enabled=False,
        )

        saveDirectory = action(
            self.tr("Enregistrer"),
            lambda: self.clickSaveChoose(),
            'None',
            "objects",
            self.tr("Enregistrer"),
            enabled=True,
        )

        createMode = action(
            self.tr("Polygones"),
            lambda: self.toggleDrawMode(False, createMode="polygon"),
            'Ctrl+W',
            "objects",
            self.tr("Start drawing polygons"),
            enabled=True,
        )
        createPointMode = action(
            self.tr("Points"),
            lambda: self.toggleDrawMode(False, createMode="point"),
            'None',
            "objects",
            self.tr("Invite de points"),
            enabled=True,
        )
        createRectangleMode = action(
            self.tr("Boîte"),
            lambda: self.toggleDrawMode(False, createMode="rectangle"),
            'None',
            "objects",
            self.tr("Invite de boîte"),
            enabled=True,
        )
        cleanPrompt = action(
            self.tr("Rejeter"),
            lambda: self.cleanPrompt(),
            'r',
            "objects",
            self.tr("Rejeter"),
            enabled=True,
        )
        
        self.switchClass = action(
            self.tr("Classe On/Off"),
            lambda: self.clickSwitchClass(),
            'none',
            "objects",
            self.tr("Classe On/Off"),
            enabled=True,
        )

        editMode = action(
            self.tr("Modifier le polygone"),
            self.setEditMode,
            'None',
            "edit",
            self.tr("Déplacer et modifier les polygones sélectionnés"),
            enabled=False,
        )
        saveAs = action(
            self.tr("&Save As"),
            self.saveFileAs,
            'ALT+s',
            "save-as",
            self.tr("Enregistrer les étiquettes dans un autre fichier"),
            enabled=True,
        )

        undoLastPoint = action(
            self.tr("Annuler le dernier point"),
            self.canvas.undoLastPoint,
            'U',
            "undo",
            self.tr("Annuler le dernier point dessiné"),
            enabled=False,
        )

        hideAll = action(
            self.tr("&Hide\nPolygons"),
            functools.partial(self.togglePolygons, False),
            icon="eye",
            tip=self.tr("Masquer tous les polygones"),
            enabled=False,
        )
        showAll = action(
            self.tr("&Show\nPolygons"),
            functools.partial(self.togglePolygons, True),
            icon="eye",
            tip=self.tr("Afficher tous les polygones"),
            enabled=False,
        )

        undo = action(
            self.tr("Annuler"),
            self.undoShapeEdit,
            'Ctrl+U',
            "undo",
            self.tr("Annuler le dernier ajout et modification de la forme"),
            enabled=False,
        )

        save = action(
            self.tr("&Sauvegarder"),
            self.saveFile,
            'S',
            "save",
            self.tr("Enregistrer les étiquettes dans un fichier"),
            enabled=False,
        )

        delete = action(
            self.tr("Supprimer des polygones"),
            self.deleteSelectedShape,
            'd',
            "cancel",
            self.tr("Supprimer les polygones sélectionnés"),
            enabled=False,
        )
        duplicate = action(
            self.tr("Dupliquer le Polygone"),
            self.duplicateSelectedShape,
            'None',
            "copy",
            self.tr("Créer un double des polygones sélectionnés"),
            enabled=False,
        )
        reduce_point = action(
            self.tr("Réduire les points"),
            self.reducePoint,
            'None',
            "copy",
            self.tr("Réduire les points"),
            enabled=True,
        )            
        edit = action(
            self.tr("&Modifier l'étiquette"),
            self.editLabel,
            'None',
            "edit",
            self.tr("Modifier le label du polygone sélectionné"),
            enabled=False,
        )
        

        self.actions = utils.struct(
            categoryFile=categoryFile,
            imageDirectory=imageDirectory,
            saveDirectory=saveDirectory,
            switchClass=self.switchClass,
            loadSAM=LoadSAM,
            autoSeg=AutoSeg,
            promptSeg=promptSeg,
            cleanPrompt=cleanPrompt,
            createMode=createMode,
            createPointMode=createPointMode,
            createRectangleMode=createRectangleMode,
            editMode=editMode,
            undoLastPoint=undoLastPoint,
            undo=undo,
            delete=delete,
            edit=edit,
            duplicate=duplicate,
            reduce_point=reduce_point,
            save=save,
            onShapesPresent=(saveAs, hideAll, showAll),
            menu=(
                createMode,
                editMode,
                undoLastPoint,
                undo,
                save,
            )
            )

        # Custom context menu for the canvas widget:
        utils.addActions(self.canvas.menus[0], self.actions.menu)
        utils.addActions(
            self.canvas.menus[1],
            (
                action("&Copy here", self.copyShape),
                action("&Move here", self.moveShape),
            ),
        )

        self.toolbar = self.addToolBar('Tool')
        self.toolbar.addAction(categoryFile)
        self.toolbar.addAction(imageDirectory)
        self.toolbar.addAction(saveDirectory)
        self.toolbar.addAction(self.switchClass)
        self.toolbar.addAction(LoadSAM)
        self.toolbar.addAction(AutoSeg)
        self.toolbar.addAction(promptSeg)
        self.toolbar.addAction(cleanPrompt)
        self.toolbar.addAction(createMode)
        self.toolbar.addAction(createPointMode)
        self.toolbar.addAction(createRectangleMode)
        self.toolbar.addAction(editMode)
        self.toolbar.addAction(undoLastPoint)
        self.toolbar.addAction(undo)
        self.toolbar.addAction(delete)
        self.toolbar.addAction(edit)
        self.toolbar.addAction(duplicate)
        self.toolbar.addAction(reduce_point)
        self.toolbar.addAction(save)
        self.toolbar.setToolButtonStyle(Qt.ToolButtonTextOnly)

        zoom = QtWidgets.QWidgetAction(self)
        zoom.setDefaultWidget(self.zoomWidget)
        self.zoomWidget.setWhatsThis(
            str(
                self.tr(
                    "Zoom in or out of the image. Also accessible with "
                    "{} from the canvas."
                )
            ).format(
                #utils.fmtShortcut(
                #    "{},{}".format(shortcuts["zoom_in"], shortcuts["zoom_out"])
                #),
                utils.fmtShortcut(self.tr("Ctrl+Wheel")),
            )
        )
        self.zoomWidget.setEnabled(True)

        self.zoomWidget.valueChanged.connect(self.paintCanvas)
        self.canvas.actions = self.actions

    def get_categories(self):
        return [
            {"id": 1, "name": "non_classee", "supercategory": "equipement"},
            {"id": 2, "name": "cable", "supercategory": "equipement"},
            {"id": 3, "name": "passe_cable", "supercategory": "equipement"},
            {"id": 4, "name": "lumiere", "supercategory": "equipement"},
            {"id": 5, "name": "joint", "supercategory": "equipement"},
            {"id": 6, "name": "camera", "supercategory": "equipement"},
            {"id": 7, "name": "prisme_sos_telephone", "supercategory": "equipement"},
            {"id": 8, "name": "bouche_incendie", "supercategory": "equipement"},
            {"id": 9, "name": "reflecteur", "supercategory": "equipement"},
            {"id": 10, "name": "prisme_issue_en_face", "supercategory": "equipement"},
            {"id": 11, "name": "indication_issue_de_secours", "supercategory": "equipement"},
            {"id": 12, "name": "plaque_numerotee", "supercategory": "equipement"},
            {"id": 13, "name": "issue_de_secours", "supercategory": "equipement"},
            {"id": 14, "name": "plaque_anneau", "supercategory": "equipement"},
            {"id": 15, "name": "indication_id_sos", "supercategory": "equipement"},
            {"id": 16, "name": "issue_sos_telephone", "supercategory": "equipement"},
            {"id": 17, "name": "panneau_signalisation", "supercategory": "equipement"},
            {"id": 18, "name": "coffrage", "supercategory": "equipement"},
            {"id": 19, "name": "boitier_elec", "supercategory": "equipement"},
            {"id": 20, "name": "non_definie_1", "supercategory": "equipement"},
            {"id": 21, "name": "non_definie_2", "supercategory": "equipement"},
            {"id": 22, "name": "non_definie_3", "supercategory": "equipement"},
            {"id": 23, "name": "non_definie_4", "supercategory": "equipement"},
            {"id": 24, "name": "non_definie_5", "supercategory": "equipement"},
        ]

    def saveFileAs(self, _value=False):
        assert not self.image.isNull(), "cannot save empty image"
        self._saveFile(self.saveFileDialog())

    def saveFile(self, _value=False):
        self._saveFile(self.current_output_filename)

    def _saveFile(self, filename):
        if filename and self.saveLabels(filename):
            self.setClean()

    def saveLabels(self, filename):
        def format_shape(s):
            points = [[p.x(), p.y()] for p in s.points]
            min_x = min(point[0] for point in points)
            min_y = min(point[1] for point in points)
            max_x = max(point[0] for point in points)
            max_y = max(point[1] for point in points)
            bbox = [min_x, min_y, max_x - min_x, max_y - min_y]
            area = (max_x - min_x) * (max_y - min_y)
            segmentation = [points]

            return {
                "area": area,
                "bbox": bbox,
                "category_id": self.getCategoryId(s.label),
                "id": self.annotation_id,
                "image_id": self.image_id,
                "iscrowd": 0,
                "segmentation": segmentation
            }

        shapes = [format_shape(item.shape()) for item in self.labelList]
        self.annotation_id += len(shapes)

        image_entry = {
            "id": self.image_id,
            "file_name": self.current_img,
            "height": self.raw_h,
            "width": self.raw_w
        }
        self.all_annotations["images"].append(image_entry)
        self.all_annotations["annotations"].extend(shapes)

        self.image_id += 1
        return True
    
    def getCategoryId(self, label):
        try:
            return self.category_list.index(label) + 1  # Add 1 to match category IDs in get_categories
        except ValueError:
            return -1  # Return an invalid category ID if not found

    def setClean(self):
        self.dirty = False
        self.actions.save.setEnabled(False)
        self.actions.createMode.setEnabled(True)

    def saveFileDialog(self):
        caption = self.tr("Choose File")
        filters = self.tr("Label files")
        dlg = QFileDialog(self, caption, self.output_dir if self.output_dir else self.currentPath(), filters)
        dlg.setDefaultSuffix(LabelFile.suffix[1:])
        dlg.setAcceptMode(QFileDialog.AcceptSave)
        dlg.setOption(QFileDialog.DontConfirmOverwrite, False)
        dlg.setOption(QFileDialog.DontUseNativeDialog, False)
        basename = os.path.basename(self.current_img)[:-4]
        default_labelfile_name = osp.join(self.output_dir if self.output_dir else self.currentPath(), basename + LabelFile.suffix)
        filename = dlg.getSaveFileName(self, self.tr("Choose File"), default_labelfile_name, self.tr("Label files (*%s)") % LabelFile.suffix)
        if isinstance(filename, tuple):
            filename, _ = filename
        return filename

    def currentPath(self):
        return "."

    def saveAllAnnotations(self, output_filename):
        with open(output_filename, 'w') as f:
            json.dump(self.all_annotations, f, indent=4)

    def loadAnno(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)

        annotations = data.get("annotations", [])  # Récupérer les annotations du fichier JSON
        for annotation in annotations:
            points = annotation["segmentation"][0]  # Récupérer les points de la segmentation
            label = self.category_list[annotation["category_id"] - 1]  # Récupérer le label en fonction de l'ID de catégorie
            shape = Shape(
                label=label,
                shape_type="polygon",
                group_id=annotation["id"],  # Utiliser l'ID de l'annotation comme ID de groupe
            )
            for i in range(0, len(points), 2):
                x = points[i]
                y = points[i + 1]
                shape.addPoint(QtCore.QPointF(x, y))
            shape.close()
            self.addLabel(shape)

        self.canvas.loadShapes([item.shape() for item in self.labelList])

    def clickButtonNext(self):
        if self.actions.save.isEnabled():
            self.saveFile()
        if self.current_img_index < self.img_len - 1:
            self.current_img_index += 1
            self.current_img = self.img_list[self.current_img_index]
            self.loadImg()

    def clickButtonLast(self):
        if self.actions.save.isEnabled():
            self.saveFile()
        if self.current_img_index > 0:
            self.current_img_index -= 1
            self.current_img = self.img_list[self.current_img_index]
            self.loadImg()

    def choose_proposal1(self):
        if len(self.sam_mask_proposal) > 0:
            self.sam_mask = self.sam_mask_proposal[0]
            self.canvas.setHiding()
            self.canvas.update()

    def choose_proposal2(self):
        if len(self.sam_mask_proposal) > 1:
            self.sam_mask = self.sam_mask_proposal[1]
            self.canvas.setHiding()
            self.canvas.update()
            
    def choose_proposal3(self):
        if len(self.sam_mask_proposal) > 2:
            self.sam_mask = self.sam_mask_proposal[2]
            self.canvas.setHiding()
            self.canvas.update()
            
    def choose_proposal4(self):
        if len(self.sam_mask_proposal) > 3:
            self.sam_mask = self.sam_mask_proposal[3]
            self.canvas.setHiding()
            self.canvas.update()
            
    def loadImg(self):
        self.raw_h, self.raw_w = cv2.imread(self.current_img).shape[:2]
        pixmap = QPixmap(self.current_img)
        self.canvas.loadPixmap(pixmap)
        self.img_progress_bar.setValue(self.current_img_index)

        img_name = os.path.basename(self.current_img)[:-4]
        self.current_output_filename = osp.join(self.current_output_dir, img_name + '.json')
        self.labelList.clear()
        if os.path.isfile(self.current_output_filename):
            self.loadAnno(self.current_output_filename)
        self.image_encoded_flag = False
        self.current_img_data = LabelFile.load_image_file(self.current_img)

        # Sauvegarder toutes les annotations dans le fichier annotations.json
        self.saveAllAnnotationsToFile()

    def saveAllAnnotationsToFile(self):
        output_filename = os.path.join(self.current_output_dir, 'annotations.json')
        self.saveAllAnnotations(output_filename)

    def clickFileChoose(self):
        directory = QFileDialog.getExistingDirectory(self, 'choose target fold','.')
        if directory == '':
            return
        self.img_list = glob.glob(directory + '/*.jpg') + glob.glob(directory + '/*.png')
        self.img_list.sort()
        self.img_len = len(self.img_list)
        if self.img_len == 0:
            return
        self.current_img_index = 0
        self.current_img = self.img_list[self.current_img_index]
        self.img_progress_bar.setMinimum(0)
        self.img_progress_bar.setMaximum(self.img_len-1)
        self.loadImg()

    def clickSaveChoose(self):
        directory = QFileDialog.getExistingDirectory(self, 'choose target fold','.')
        if directory == '':
            return
        else:
            self.current_output_dir = directory
            os.makedirs(self.current_output_dir, exist_ok=True)
            self.loadImg()
            return directory

    def clickSwitchClass(self):
        if self.class_on_flag:
            self.class_on_flag = False
            self.class_on_text.setText('Class Off')
        else:
            self.class_on_flag = True
            self.class_on_text.setText('Class On')

    def clickCategoryChoose(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'choose target file','.')
        try:
            with open(filename, 'r') as f:
                data = f.readlines()
                self.category_list = [i.strip() for i in data]
                self.category_list.sort()
                self.labelDialog = LabelDialog(
                    parent=self,
                    labels=self.category_list,
                    sort_labels=False,
                    show_text_field=True,
                    completion='contains',
                    fit_to_content={'column': True, 'row': False},
                )
        except Exception as e:
            pass

    def clickLoadSAM(self):
        download_model(self.model_type)
        self.sam = sam_model_registry[self.model_type](checkpoint='{}.pth'.format(self.model_type))
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.sam.to(device=self.device)
        self.predictor = SamPredictor(self.sam)
        self.actions.loadSAM.setEnabled(False)
        self.actions.autoSeg.setEnabled(True)
        self.actions.promptSeg.setEnabled(True)
    
    def clickAutoSeg(self):

        #image = Image.open(self.image_path)
        #image = np.array(image)

        # Resize the image for SAM
        #transformer = ResizeLongestSide(self.sam.input_size)
        #image_tensor = transformer.apply_image(image)
        #image_tensor = torch.as_tensor(image_tensor).to(self.device)

        # Predict the mask
        #self.predictor.set_image(image_tensor)
        #masks, scores, _ = self.predictor.predict(boxes=None, masks=None)

        # Process the masks
        #annotated_image = self.apply_masks_to_image(image, masks)
        
        # Display the annotated image
        #self.display_image(Image.fromarray(annotated_image))
        pass
    
    def getMaxId(self):
        max_id = -1
        for label in self.labelList:
            if label.shape().group_id != None:
                max_id = max(max_id, int(label.shape().group_id))
        return max_id
        
    def show_proposals(self, masks=None, flag=1):
        if flag != 1:
            img = cv2.imread(self.current_img)
            if len(img.shape) == 2:
                img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            for msk_idx in range(masks.shape[0]):
                tmp_mask = masks[msk_idx]
                tmp_vis = img.copy()
                tmp_vis[tmp_mask > 0] = 0.5 * tmp_vis[tmp_mask > 0] + 0.5 * np.array([30,30,220])
                tmp_vis = cv2.resize(tmp_vis,(int(0.17 * global_w),int(0.14 * global_h)))
                tmp_vis = tmp_vis.astype(np.uint8)
                pixmap = QPixmap.fromImage(QImage(tmp_vis, tmp_vis.shape[1], tmp_vis.shape[0], tmp_vis.shape[1] * 3 , QImage.Format_RGB888))
                #self.button_proposal_list[msk_idx].setPixmap(pixmap)
                self.button_proposal_list[msk_idx].setIcon(QIcon(pixmap))
                self.button_proposal_list[msk_idx].setIconSize(QSize(tmp_vis.shape[1], tmp_vis.shape[0]))
                self.button_proposal_list[msk_idx].setShortcut(str(msk_idx+1))
        else:
            for idx, button_proposal in enumerate(self.button_proposal_list):
                button_proposal.setText('proprosal{}'.format(idx))
                button_proposal.setIconSize(QSize(0,0))
                self.button_proposal_list[idx].setShortcut(str(idx+1))

    def transform_input(self, image, box=None, points=None):
        if self.keep_input_size == True:
            return image, box, points
        else:
            h,w = image.shape[:2]
            scale_ratio = self.max_size / max(h,w)
            image = cv2.resize(image, (int(w*scale_ratio), int(h*scale_ratio)))
            if box is not None:
                box = box * scale_ratio
            if points is not None:
                points = points * scale_ratio
            return image, box, points
    
    def transform_output(self, masks, size):
        if self.keep_input_size == True:
            return masks
        else:
            h,w = size
            N = masks.shape[0]
            new_masks = np.zeros((N,h,w), dtype=np.uint8)
            for idx in range(N):
                new_masks[idx] = cv2.resize(masks[idx], (w,h))
            return new_masks

    def clickManualSegBBox(self):
        Box = self.canvas.currentBox
        if self.predictor is None or self.current_img == '' or Box == None:
            return
        img = cv2.imread(self.current_img)[:,:,::-1]
        rh, rw = img.shape[:2]
        input_box = np.array([Box[0].x(), Box[0].y(), Box[1].x(), Box[1].y()])
        img, input_box, _ = self.transform_input(img, box=input_box)
        if self.image_encoded_flag == False:
            self.predictor.set_image(img)
            self.image_encoded_flag = True
        masks, iou_prediction, _ = self.predictor.predict(
            point_coords=None,
            point_labels=None,
            box=input_box[None, :],
            multimask_output=True,
        )
        masks = self.transform_output(masks.astype(np.uint8), (rh,rw))

        target_idx = np.argmax(iou_prediction)
        self.show_proposals(masks, 0)
        self.sam_mask_proposal = []
        for msk_idx in range(masks.shape[0]):
            mask = masks[msk_idx].astype(np.uint8)

            points_list = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
            shape_type = 'polygon'
            tmp_sam_mask = []
            for points in points_list:
                area = cv2.contourArea(points)
                if area < 100 and len(points_list) > 1:
                    continue
                pointsx = points[:,0,0]
                pointsy = points[:,0,1]

                shape = Shape(
                    label='Object',
                    shape_type=shape_type,
                    group_id=self.getMaxId() + 1,
                )
                for point_index in range(pointsx.shape[0]):
                    shape.addPoint(QtCore.QPointF(pointsx[point_index], pointsy[point_index]))
                shape.close()
                #self.addLabel(shape)
                tmp_sam_mask.append(shape)
            if msk_idx == target_idx:
                self.sam_mask = tmp_sam_mask
            self.sam_mask_proposal.append(tmp_sam_mask)


    def clickManualSegBox(self):
        ClickPos = self.canvas.currentPos
        ClickNeg = self.canvas.currentNeg
        if self.predictor is None or self.current_img == '' or (ClickPos == None and ClickNeg == None):
            return
        img = cv2.imread(self.current_img)[:,:,::-1]
        rh, rw = img.shape[:2]

        input_clicks = []
        input_types = []
        if ClickPos != None:
            for pos in ClickPos:
                input_clicks.append([int(pos.x()), int(pos.y())])
                input_types.append(1)

        if ClickNeg != None:
            for neg in ClickNeg:
                input_clicks.append([int(neg.x()), int(neg.y())])
                input_types.append(0)
        if len(input_clicks) == 0:
            input_clicks = None
            input_types = None
        else:
            input_clicks = np.array(input_clicks)
            input_types = np.array(input_types)

        img, _, input_clicks = self.transform_input(img, points=input_clicks)

        if self.image_encoded_flag == False:
            self.predictor.set_image(img)
            self.image_encoded_flag = True
        masks, iou_prediction, _ = self.predictor.predict(
            point_coords=input_clicks,
            point_labels=input_types,
            multimask_output=True,
        )
        masks = self.transform_output(masks.astype(np.uint8), (rh,rw))
        
        target_idx = np.argmax(iou_prediction)
        self.show_proposals(masks,0)
        self.sam_mask_proposal = []
        
        for msk_idx in range(masks.shape[0]):
            mask = masks[msk_idx].astype(np.uint8)
            
            points_list = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
            shape_type = 'polygon'
            tmp_sam_mask = []
            for points in points_list:
                area = cv2.contourArea(points)
                if area < 100 and len(points_list) > 1:
                    continue
                pointsx = points[:,0,0]
                pointsy = points[:,0,1]

                shape = Shape(
                    label='Object',
                    shape_type=shape_type,
                    group_id=self.getMaxId() + 1,
                )
                for point_index in range(pointsx.shape[0]):
                    shape.addPoint(QtCore.QPointF(pointsx[point_index], pointsy[point_index]))
                shape.close()
                #self.addLabel(shape)
                tmp_sam_mask.append(shape)
            if msk_idx == target_idx:
                self.sam_mask = tmp_sam_mask
            self.sam_mask_proposal.append(tmp_sam_mask)
            
    def addSamMask(self):
        if len(self.sam_mask) > 0:
            label = 'Object'
            group_id = self.getMaxId() + 1
            if self.class_on_flag:
                xx = self.labelDialog.popUp(
                    text=label,
                    flags={},
                    group_id=group_id,
                )
                if len(xx) == 4:
                    label, _, group_id,_ = xx
                else:
                    label, _, group_id = xx
            if label == None:
                label = 'Object'
            if type(group_id) != int:
                group_id=self.getMaxId() + 1
            for sam_mask in self.sam_mask:
                sam_mask.label = label
                sam_mask.group_id = group_id
                self.addLabel(sam_mask)
        self.canvas.currentBox = None
        self.canvas.currentPos = None
        self.canvas.currentNeg = None
        self.sam_mask = []
        self.sam_mask_proposal = []
        self.show_proposals()
        self.canvas.loadShapes([item.shape() for item in self.labelList])
        self.actions.save.setEnabled(True)
        self.actions.editMode.setEnabled(True)



    def cleanPrompt(self):
        self.canvas.currentBox = None
        self.canvas.currentPos = None
        self.canvas.currentNeg = None
        self.canvas.current = None
        self.sam_mask = []
        self.sam_mask_proposal = []
        self.show_proposals()
        self.canvas.setHiding()
        self.canvas.update()
        self.actions.editMode.setEnabled(True)



    def zoomRequest(self, delta, pos):
        canvas_width_old = self.canvas.width()
        units = 1.1
        if delta < 0:
            units = 0.9
        self.addZoom(units)

        canvas_width_new = self.canvas.width()
        if canvas_width_old != canvas_width_new:
            canvas_scale_factor = canvas_width_new / canvas_width_old

            x_shift = round(pos.x() * canvas_scale_factor) - pos.x()
            y_shift = round(pos.y() * canvas_scale_factor) - pos.y()

            self.setScroll(
                Qt.Horizontal,
                self.scrollBars[Qt.Horizontal].value() + x_shift,
            )
            self.setScroll(
                Qt.Vertical,
                self.scrollBars[Qt.Vertical].value() + y_shift,
            )

    def scrollRequest(self, delta, orientation):
        units = -delta * 0.1  # natural scroll
        bar = self.scrollBars[orientation]
        value = bar.value() + bar.singleStep() * units
        self.setScroll(orientation, value)

    def newShape(self):
        """Pop-up and give focus to the label editor.

        position MUST be in global coordinates.
        """
        items = self.uniqLabelList.selectedItems()
        text = None
        if items:
            text = items[0].data(Qt.UserRole)
        flags = {}
        group_id = None
        if not text:
            previous_text = self.labelDialog.edit.text()
            xx = self.labelDialog.popUp(text)
            if len(xx) == 4:
                text, flags, group_id, _ = xx
            else:
                text, flags, group_id = xx
            if not text:
                self.labelDialog.edit.setText(previous_text)

        if text and not self.validateLabel(text):
            self.errorMessage(
                self.tr("Invalid label"),
                self.tr("Invalid label '{}' with validation type '{}'").format(
                    text, self._config["validate_label"]
                ),
            )
            text = ""
        if text:
            self.labelList.clearSelection()
            shape = self.canvas.setLastLabel(text, flags)
            shape.group_id = group_id
            self.addLabel(shape)
            self.actions.editMode.setEnabled(True)
            self.actions.undoLastPoint.setEnabled(False)
            self.actions.undo.setEnabled(True)
            self.setDirty()
        else:
            self.canvas.undoLastLine()
            self.canvas.shapesBackups.pop()

    def setDirty(self):
        # Even if we autosave the file, we keep the ability to undo
        self.actions.undo.setEnabled(self.canvas.isShapeRestorable)

        # if self._config["auto_save"] or self.actions.saveAuto.isChecked():
        #     label_file = osp.splitext(self.imagePath)[0] + ".json"
        #     if self.output_dir:
        #         label_file_without_path = osp.basename(label_file)
        #         label_file = osp.join(self.output_dir, label_file_without_path)
        #     self.saveLabels(label_file)
        #     return
        # self.dirty = True
        self.actions.save.setEnabled(True)
        # title = __appname__
        # if self.filename is not None:
        #     title = "{} - {}*".format(title, self.filename)
        # self.setWindowTitle(title)

    # React to canvas signals.
    def shapeSelectionChanged(self, selected_shapes):
        self._noSelectionSlot = True
        for shape in self.canvas.selectedShapes:
            shape.selected = False
        self.labelList.clearSelection()
        self.canvas.selectedShapes = selected_shapes
        for shape in self.canvas.selectedShapes:
            shape.selected = True
            item = self.labelList.findItemByShape(shape)
            self.labelList.selectItem(item)
            self.labelList.scrollToItem(item)
        self._noSelectionSlot = False
        n_selected = len(selected_shapes)
        self.actions.delete.setEnabled(n_selected)
        self.actions.duplicate.setEnabled(n_selected)
        self.actions.edit.setEnabled(n_selected == 1)

    def toggleDrawingSensitive(self, drawing=True):
        """Toggle drawing sensitive.

        In the middle of drawing, toggling between modes should be disabled.
        """
        self.actions.editMode.setEnabled(not drawing)
        # self.actions.undoLastPoint.setEnabled(drawing)
        # self.actions.undo.setEnabled(not drawing)
        # self.actions.delete.setEnabled(not drawing)
    def setScroll(self, orientation, value):
        self.scrollBars[orientation].setValue(int(value))
        self.scroll_values[orientation][self.current_img] = value

    def toolbar(self, title, actions=None):
        toolbar = self.addToolBar("%sToolBar" % title)
        # toolbar.setOrientation(Qt.Vertical)
        if actions:
            utils.addActions(toolbar, actions)
        return toolbar

    def setEditMode(self):
        self.toggleDrawMode(True)

    def toggleDrawMode(self, edit=True, createMode="polygon"):
        self.canvas.setEditing(edit)
        self.canvas.createMode = createMode
        if edit:
            self.actions.createMode.setEnabled(True)
            self.actions.createPointMode.setEnabled(True)
            self.actions.createRectangleMode.setEnabled(True)

        else:
            if createMode == "polygon":
                self.actions.createPointMode.setEnabled(True)
                self.actions.createMode.setEnabled(False)
                self.actions.createRectangleMode.setEnabled(True)

            elif createMode == "point":
                self.actions.createMode.setEnabled(True)
                self.actions.createPointMode.setEnabled(False)
                self.actions.createRectangleMode.setEnabled(True)
            elif createMode == "rectangle":
                self.actions.createMode.setEnabled(True)
                self.actions.createPointMode.setEnabled(True)
                self.actions.createRectangleMode.setEnabled(False)
            else:
                raise ValueError("Unsupported createMode: %s" % createMode)
        self.actions.editMode.setEnabled(not edit)

    def validateLabel(self, label):
        return True

    def labelSelectionChanged(self):
        if self._noSelectionSlot:
            return
        if self.canvas.editing():
            selected_shapes = []
            for item in self.labelList.selectedItems():
                selected_shapes.append(item.shape())
            if selected_shapes:
                self.canvas.selectShapes(selected_shapes)
            else:
                self.canvas.deSelectShape()

    def iou(self, target_mask, mask_list):
        target_mask = target_mask.reshape(1,-1)
        mask_list = mask_list.reshape(mask_list.shape[0], -1)
        i = (target_mask * mask_list)
        u = target_mask + mask_list - i
        return i.sum(1)/u.sum(1)


    def polygon2mask(self,polygon, size):
        mask = np.zeros((size)) # h,w
        contours = np.array(polygon)
        mask = cv2.fillPoly(mask, [contours.astype(np.int32)],1)
        return mask.astype(np.uint8)

    def mask2polygon(self, mask):
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = np.array(contours[0])
        return contours

    def editLabel(self, item=None):
        if item and not isinstance(item, LabelListWidgetItem):
            raise TypeError("item must be LabelListWidgetItem type")

        if not self.canvas.editing():
            return
        if not item:
            item = self.currentItem()
        if item is None:
            return
        shape = item.shape()
        if shape is None:
            return
        xx = self.labelDialog.popUp(
            text=shape.label,
            flags=shape.flags,
            group_id=shape.group_id,
        )
        if len(xx) == 4:
            text, flags, group_id,_ = xx
        else:
            text, flags, group_id = xx
        if text is None:
            return
        if not self.validateLabel(text):
            self.errorMessage(
                self.tr("Invalid label"),
                self.tr("Invalid label '{}' with validation type '{}'").format(
                    text, self._config["validate_label"]
                ),
            )
            return
        shape.label = text
        shape.flags = flags
        shape.group_id = group_id

        self._update_shape_color(shape)
        if shape.group_id is None:
            item.setText(
                '{} <font color="#{:02x}{:02x}{:02x}">●</font>'.format(
                    html.escape(shape.label), *shape.fill_color.getRgb()[:3]
                )
            )
        else:
            item.setText("({}) {}".format(shape.group_id, shape.label))
        self.setDirty()
        if self.uniqLabelList.findItemByLabel(shape.label) is None:
            item = self.uniqLabelList.createItemFromLabel(shape.label)
            self.uniqLabelList.addItem(item)
            # rgb = self._get_rgb_by_label(shape.label)
            rgb = self._get_rgb_by_label(shape.group_id)
            self.uniqLabelList.setItemLabel(item, shape.label, rgb)

    def labelItemChanged(self, item):
        shape = item.shape()
        self.canvas.setShapeVisible(shape, item.checkState() == Qt.Checked)

    def labelOrderChanged(self):
        self.setDirty()
        self.canvas.loadShapes([item.shape() for item in self.labelList])

    def addLabel(self, shape):
        if shape.group_id is None:
            text = shape.label
        else:
            text = "({}) {}".format(shape.group_id, shape.label)
        label_list_item = LabelListWidgetItem(text, shape)
        self.labelList.addItem(label_list_item)
        if self.uniqLabelList.findItemByLabel(shape.label) is None:
            item = self.uniqLabelList.createItemFromLabel(shape.label)
            self.uniqLabelList.addItem(item)
            # rgb = self._get_rgb_by_label(shape.label)
            rgb = self._get_rgb_by_label(shape.group_id)
            self.uniqLabelList.setItemLabel(item, shape.label, rgb)
        self.labelDialog.addLabelHistory(shape.label)
        for action in self.actions.onShapesPresent:
            action.setEnabled(True)

        self._update_shape_color(shape)
        label_list_item.setText(
            '{} <font color="#{:02x}{:02x}{:02x}">●</font>'.format(
                html.escape(text), *shape.fill_color.getRgb()[:3]
            )
        )
    def _get_rgb_by_label(self, label):
        label = str(label)
        item = self.uniqLabelList.findItemByLabel(label)
        if item is None:
            item = self.uniqLabelList.createItemFromLabel(label)
            self.uniqLabelList.addItem(item)
            rgb = self._get_rgb_by_label(label)
            self.uniqLabelList.setItemLabel(item, label, rgb)
        label_id = self.uniqLabelList.indexFromItem(item).row() + 1
        label_id += 0
        return LABEL_COLORMAP[label_id % len(LABEL_COLORMAP)]

    def togglePolygons(self, value):
        for item in self.labelList:
            item.setCheckState(Qt.Checked if value else Qt.Unchecked)

    def _update_shape_color(self, shape):
        # r, g, b = self._get_rgb_by_label(shape.label)
        r, g, b = self._get_rgb_by_label(shape.group_id)
        shape.line_color = QtGui.QColor(r, g, b)
        shape.vertex_fill_color = QtGui.QColor(r, g, b)
        shape.hvertex_fill_color = QtGui.QColor(255, 255, 255)
        shape.fill_color = QtGui.QColor(r, g, b, 128)
        shape.select_line_color = QtGui.QColor(255, 255, 255)
        shape.select_fill_color = QtGui.QColor(r, g, b, 155)

    def undoShapeEdit(self):
        self.canvas.restoreShape()
        self.labelList.clear()
        self.loadShapes(self.canvas.shapes)
        self.actions.undo.setEnabled(self.canvas.isShapeRestorable)

    def loadShapes(self, shapes, replace=True):
        self._noSelectionSlot = True
        for shape in shapes:
            self.addLabel(shape)
        self.labelList.clearSelection()
        self._noSelectionSlot = False
        self.canvas.loadShapes(shapes, replace=replace)


    def moveShape(self):
        self.canvas.endMove(copy=False)
        self.setDirty()

    def copyShape(self):
        self.canvas.endMove(copy=True)
        for shape in self.canvas.selectedShapes:
            self.addLabel(shape)
        self.labelList.clearSelection()
        self.setDirty()
    def deleteSelectedShape(self):
        #yes, no = QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No
        #msg = self.tr(
        #    "You are about to permanently delete {} polygons, "
        #    "proceed anyway?"
        #).format(len(self.canvas.selectedShapes))
        #if yes == QtWidgets.QMessageBox.warning(
        #    self, self.tr("Attention"), msg, yes | no, yes
        #):
        self.remLabels(self.canvas.deleteSelected())
        self.setDirty()
        if self.noShapes():
            for action in self.actions.onShapesPresent:
                action.setEnabled(False)
    def duplicateSelectedShape(self):
        added_shapes = self.canvas.duplicateSelectedShapes()
        self.labelList.clearSelection()
        for shape in added_shapes:
            self.addLabel(shape)
        self.setDirty()

    def reducePoint(self):
        def format_shape(s):
            data = s.other_data.copy()
            data.update(
                dict(
                    label=s.label.encode("utf-8") if PY2 else s.label,
                    points=[(p.x(), p.y()) for p in s.points],
                    group_id=s.group_id,
                    shape_type=s.shape_type,
                    flags=s.flags,
                )
            )
            return data
        shapes = self.current_img
        shapes = [format_shape(item.shape()) for item in self.labelList.selectedItems()]
        rm_shapes = [item.shape() for item in self.labelList.selectedItems()]
        self.remLabels(rm_shapes)
        for shape in shapes:
            points = shape['points']
            min_dis = self.get_min_dis(points)
            points_new = [points[0]]
            for i in range(1,len(points)):
                d = math.sqrt((points[i][0] - points_new[-1][0]) ** 2 + (points[i][1] - points_new[-1][1]) ** 2)
                if d > (min_dis * 1.5):
                    points_new.append(points[i])
            shape['points'] = points_new
        #self.labelList.clear()
        for tmp_shape in shapes:
            shape = Shape(
                label=tmp_shape['label'],
                shape_type=tmp_shape['shape_type'],
                group_id=tmp_shape['group_id'],
            )
            for point_index in range(len(tmp_shape['points'])):
                shape.addPoint(QtCore.QPointF(tmp_shape['points'][point_index][0], tmp_shape['points'][point_index][1]))
            shape.close()
            self.addLabel(shape)
            tmp_item = self.labelList.findItemByShape(shape)
            self.labelList.selectItem(tmp_item)
            self.labelList.scrollToItem(tmp_item)
        self.canvas.loadShapes([item.shape() for item in self.labelList])
        self.actions.save.setEnabled(True)

    def get_min_dis(self, points):
        min_dis = 10000
        if len(points) >= 2:
            points_new = [points[0]]
            for i in range(1,len(points)):
                d = math.sqrt((points[i][0] - points_new[-1][0]) ** 2 + (points[i][1] - points_new[-1][1]) ** 2)
                min_dis = min(min_dis, d)
                points_new.append(points[i])
        return min_dis



    def pasteSelectedShape(self):
        self.loadShapes(self._copied_shapes, replace=False)
        self.setDirty()

    def copySelectedShape(self):
        self._copied_shapes = [s.copy() for s in self.canvas.selectedShapes]
        self.actions.paste.setEnabled(len(self._copied_shapes) > 0)

    def currentItem(self):
        items = self.labelList.selectedItems()
        if items:
            return items[0]
        return None

    def remLabels(self, shapes):
        for shape in shapes:
            item = self.labelList.findItemByShape(shape)
            self.labelList.removeItem(item)


    def noShapes(self):
        return not len(self.labelList)

    def addZoom(self, increment=1.1):
        zoom_value = self.zoomWidget.value() * increment
        if increment > 1:
            zoom_value = math.ceil(zoom_value)
        else:
            zoom_value = math.floor(zoom_value)
        self.setZoom(zoom_value)

    def setZoom(self, value):
        self.zoomMode = self.MANUAL_ZOOM
        self.zoomWidget.setValue(value)
        self.zoom_values[self.current_img] = (self.zoomMode, value)

    def paintCanvas(self):
        self.canvas.scale = 0.01 * self.zoomWidget.value()
        self.canvas.adjustSize()
        self.canvas.update()


def get_parser():
    parser = argparse.ArgumentParser(description="pixel annotator by GroundedSAM")
    parser.add_argument(
        "--app_resolution",
        default='1100,1900',
    )
    parser.add_argument(
        "--model_type",
        default='vit_b',
    )
    parser.add_argument(
        "--keep_input_size",
        type=bool,
        default=True,
    )   
    parser.add_argument(
        "--max_size",
        default=720,
    )   
    return parser

if __name__ == '__main__':
    parser = get_parser()
    global_h, global_w = [int(i) for i in parser.parse_args().app_resolution.split(',')]
    model_type = parser.parse_args().model_type
    keep_input_size = parser.parse_args().keep_input_size
    max_size = parser.parse_args().max_size
    app = QApplication(sys.argv)
    main = MainWindow(global_h=global_h, global_w=global_w, model_type=model_type, keep_input_size=keep_input_size, max_size=max_size)
    main.show()
    sys.exit(app.exec_())

