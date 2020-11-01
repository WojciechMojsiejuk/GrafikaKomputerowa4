from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QGroupBox, QHBoxLayout, QDoubleSpinBox


class BrightnessDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(BrightnessDialog, self).__init__(*args, **kwargs)
        self.setWindowTitle("Brightness Dialog")
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.input_layout = QHBoxLayout()

        self.groupBox = QGroupBox('Gamma')

        self.input = QDoubleSpinBox()
        self.input.setMinimum(0.01)
        self.input.setMaximum(10)
        self.input.setValue(1)
        self.input.setSingleStep(0.1)

        self.input_layout.addWidget(self.input)
        self.groupBox.setLayout(self.input_layout)

        self.layout.addWidget(self.groupBox)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def get_values(self):
        return self.input.value()
