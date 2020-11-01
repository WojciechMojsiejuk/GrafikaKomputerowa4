from pathlib import Path

import PIL.Image
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from matplotlib.figure import Figure
from ui.dialog.add_point_transform import AddPointTransformationDialog
from ui.dialog.brightness import BrightnessDialog
from ui.dialog.multiply_point_transform import MultiplyPointTransformationDialog
from cg.transform.point import *
from cg.transform.convolution import Filters as filters
from cg.transform.convolution import FilterConvolution as fc
from cg.transform.convolution import MedianFilterConvolution as mfc


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
        self.actionExit.triggered.connect(self.close_app)
        self.actionRevert.triggered.connect(self.revert_image)
        self.actionAdditive.triggered.connect(self.additive_point_transformation)
        self.actionMultiplicative.triggered.connect(self.multiplicative_point_transformation)
        self.actionLuminosity.triggered.connect(self.luminosity_grayscale)
        self.actionAverage.triggered.connect(self.average_grayscale)
        self.actionLightness.triggered.connect(self.lightness_grayscale)
        self.actionBrightness.triggered.connect(self.change_brightness)

        # Filter
        self.actionMean.triggered.connect(self.mean_filter)
        self.actionMedian.triggered.connect(self.median_filter)
        self.actionHorizontal.triggered.connect(self.horizontal_sobel_filter)
        self.actionVertical.triggered.connect(self.vertical_sobel_filter)
        self.actionSharpen.triggered.connect(self.sharpen_filter)
        self.actionGaussian_Blur.triggered.connect(self.gaussian_blur_filter)

    def close_app(self):
        sys.exit(self.exec_())

    def revert_image(self):
        self.image.img = self.init_img

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
                self.init_img = self.image.img.copy()

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
            self.image.img = additive(self.image.img, dlg.get_values())

    def multiplicative_point_transformation(self):
        dlg = MultiplyPointTransformationDialog()
        if dlg.exec_():
            self.image.img = multiplicative(self.image.img, dlg.get_values())

    def luminosity_grayscale(self):
        self.image.img = luminosity_grayscale(self.image.img)

    def lightness_grayscale(self):
        self.image.img = lightness_grayscale(self.image.img)

    def average_grayscale(self):
        self.image.img = average_grayscale(self.image.img)

    def change_brightness(self):
        dlg = BrightnessDialog()
        if dlg.exec_():
            self.image.img = brightness(self.image.img, dlg.get_values())

    def mean_filter(self):
        mean_f = fc(kernel=filters.box_blur, image=self.image.img)
        mean_f.apply_filter()
        self.image.img = mean_f.return_img()

    def median_filter(self):
        median_f = mfc(kernel=filters.box_blur, image=self.image.img)
        median_f.apply_filter()
        self.image.img = median_f.return_img()

    def horizontal_sobel_filter(self):
        h_sobel_f = fc(kernel=filters.sobel_horizontal, image=self.image.img)
        h_sobel_f.apply_filter()
        self.image.img = h_sobel_f.return_img()

    def vertical_sobel_filter(self):
        v_sobel_f = fc(kernel=filters.sobel_vertical, image=self.image.img)
        v_sobel_f.apply_filter()
        self.image.img = v_sobel_f.return_img()

    def sharpen_filter(self):
        sharpen_f = fc(kernel=filters.sharpen, image=self.image.img)
        sharpen_f.apply_filter()
        self.image.img = sharpen_f.return_img()

    def gaussian_blur_filter(self):
        gaussian_f = fc(kernel=filters.gaussian_blur, image=self.image.img)
        gaussian_f.apply_filter()
        self.image.img = gaussian_f.return_img()

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

