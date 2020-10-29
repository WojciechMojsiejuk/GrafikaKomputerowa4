from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QGroupBox, QSpinBox, QHBoxLayout


class AddPointTransformationDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(AddPointTransformationDialog, self).__init__(*args, **kwargs)
        self.setWindowTitle("Additive Transformation Dialog")
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.input_layout = QHBoxLayout()

        self.groupBox = QGroupBox('Value')

        self.input = QSpinBox()
        self.input.setMinimum(-255)
        self.input.setMaximum(255)
        self.input.setValue(0)
        self.input.setSingleStep(5)

        self.input_layout.addWidget(self.input)
        self.groupBox.setLayout(self.input_layout)

        self.layout.addWidget(self.groupBox)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def get_values(self):
        return self.input.value()
