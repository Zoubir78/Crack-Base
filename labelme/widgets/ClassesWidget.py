from qtpy import QtCore, QtGui, QtWidgets
import os

# Add ClassesWidget to allow the user to select among coco classes using checkboxes
class ClassesWidget(QtWidgets.QDialog):
    def __init__(self):
        super(ClassesWidget, self).__init__()
        self.setModal(True)
        self.setWindowTitle("Select Classes")
        self.class_names = set()  # Use a set to store selected classes
        self.classCheckboxes = self._createCheckBoxes()
        self.addButton = self._createAddButton()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(QtWidgets.QLabel("Select Classes:"))
        for checkbox in self.classCheckboxes:
            layout.addWidget(checkbox)
        layout.addWidget(self.addButton)
        self.setLayout(layout)

    def _createCheckBoxes(self):
        class_names = ['non_classee', 'cable', 'passe_cable', 'lumiere', 'joint', 'camera', 'prisme_sos_telephone', 'bouche_incendie', 'reflecteur', 'prisme_issue_en_face', 'indication_issue_de_secours', 'plaque_numerotee', 'issue_de_secours', 'plaque_anneau', 'indication_id_sos', 'issue_sos_telephone', 'panneau_signalisation', 'coffrage', 'boitier_elec', 'non_definie_1', 'non_definie_2', 'non_definie_3', 'non_definie_4', 'non_definie_5']
        checkboxes = []
        for class_name in class_names:
            checkbox = QtWidgets.QCheckBox(class_name)
            checkbox.stateChanged.connect(self.onCheckboxStateChanged)
            checkboxes.append(checkbox)
        return checkboxes

    def _createAddButton(self):
        addButton = QtWidgets.QPushButton("Add Class")
        addButton.clicked.connect(self.onAddClass)
        return addButton

    def onCheckboxStateChanged(self, state):
        checkbox = self.sender()
        class_name = checkbox.text()
        if state == QtCore.Qt.Checked:
            self.class_names.add(class_name)
        else:
            self.class_names.discard(class_name)

    def onAddClass(self):
        text, ok = QtWidgets.QInputDialog.getText(self, "Add Class", "Enter the new class name:")
        if ok and text:
            self.classCheckboxes.append(QtWidgets.QCheckBox(text))
            self.layout().insertWidget(len(self.classCheckboxes) - 1, self.classCheckboxes[-1])

    def getValues(self):
        return list(self.class_names)

    def setValues(self, values):
        self.class_names = set(values)
        for checkbox in self.classCheckboxes:
            checkbox.setChecked(checkbox.text() in self.class_names)

    def exec_(self):
        super(ClassesWidget, self).exec_()
        return self.class_names
    
class ThresholdWidget(QtWidgets.QDialog):
    def __init__(self):
        super(ThresholdWidget, self).__init__()
        self.setModal(True)
        self.setWindowTitle("Enter Threshold")
        self.threshold = 0.5
        self.threshold = self._createQLineEdit()
    
    def _createQLineEdit(self):
        threshold = QtWidgets.QLineEdit()
        threshold.setValidator(QtGui.QDoubleValidator(0.0, 1.0, 2))
        threshold.setText("0.5")
        threshold.textChanged.connect(self.onNewValue)
        return threshold

    def onNewValue(self, text):
        try:
            value = float(text)
            if 0.0 <= value <= 1.0:
                self.threshold = value
        except ValueError:
            pass


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Main Window")

        menu = self.menuBar()
        options = menu.addMenu("Options")
        classes_action = QtWidgets.QAction("Classes", self)
        classes_action.triggered.connect(lambda: self.executer6("Classes"))
        options.addAction(classes_action)

        confidence_action = QtWidgets.QAction("Confidence", self)
        confidence_action.triggered.connect(lambda: self.executer6("Confidence"))
        options.addAction(confidence_action)

    def executer6(self, action_name):
        if action_name == "Classes":
            classes_dialog = ClassesWidget()
            if classes_dialog.exec_():
                selected_classes = classes_dialog.getValues()
                print("Selected classes:", selected_classes)
        elif action_name == "Confidence":
            threshold_dialog = ThresholdWidget()
            if threshold_dialog.exec_():
                threshold_value = threshold_dialog.threshold
                print("Threshold:", threshold_value)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
