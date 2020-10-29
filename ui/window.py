from pathlib import Path

import PIL.Image
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from matplotlib.figure import Figure
from ui.dialog.add_point_transform import AddPointTransformationDialog
from cg.transform.point import additive
import sys


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("Grafika Komputerowa")
        self.image = CGImage(self)
        self.init_img = None
        self.window = self
        self.image_canvas = FigureCanvas(Figure())
        self.image_ax = self.image_canvas.figure.subplots()

    def init_ui(self):
        self.image_layout = QVBoxLayout(self.imagewidget)
        self.image_layout.addWidget(NavigationToolbar(self.image_canvas, self))
        self.image_layout.addWidget(self.image_canvas)

        self.actionOpen.triggered.connect(self.load_image)
        # self.actionSave.triggered.connect(self.save_image)
        self.actionExit.triggered.connect(self.close_app)
        self.actionRevert.triggered.connect(self.revert_image)
        self.actionAdditive.triggered.connect(self.additive_point_transformation)

    def close_app(self):
        sys.exit(self.exec_())

    def revert_image(self):
        self.image = self.init_img

    def load_image(self):
        try:
            name, _ = QFileDialog.getOpenFileName(None, "Open image file", "", "Image files (*.png *.jpg)")
            # load image
            if name is not None:
                self.image.path = Path(name)
                self.image.img = PIL.Image.open(self.image.path)
                self.image.img = self.image.img.convert('RGB')
                self.image.pixelmap = self.image.img.load()
                self.image_ax.clear()
                self.image_ax.imshow(self.image.img)
                self.image_canvas.draw()

        except FileNotFoundError as fnfe:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("File not found")
            msg.setInformativeText(str(fnfe))
            msg.setWindowTitle("File error")
            msg.exec_()
        except PermissionError as pe:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Permision error")
            msg.setInformativeText(str(pe))
            msg.setWindowTitle("File error")
            msg.exec_()

    def additive_point_transformation(self):
        dlg = AddPointTransformationDialog()
        if dlg.exec_():
            result = additive(self.image.img, dlg.get_values())
            self.image.img = PIL.Image.fromarray(result.astype('uint8'), 'RGB')

    def update_image(self):
        self.image_ax.clear()
        self.image_ax.imshow(self.image.img, cmap=self.image.cmap)
        self.image_canvas.draw()

class CGImage:
    def __init__(self, window, *args, **kwargs):
        # initialization of image
        self._img = None
        self.path = None
        self.pixelmap = None
        self.cmap = None
        self.window = window

    @property
    def img(self):
        return self._img

    @img.setter
    def img(self, value):
        self._img = value
        self.window.update_image()


class NavigationToolbar(NavigationToolbar2QT):
    # only display the buttons we need
    toolitems = [t for t in NavigationToolbar2QT.toolitems if
                 t[0] in ('Home', 'Pan', 'Forward', 'Back', 'Zoom')]