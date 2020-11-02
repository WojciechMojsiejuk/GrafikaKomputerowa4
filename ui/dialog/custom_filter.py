from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QGroupBox, QTextEdit, QHBoxLayout
import numpy as np

class CustomFilterDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(CustomFilterDialog, self).__init__(*args, **kwargs)
        self.setWindowTitle("Custon Filter Dialog")
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.input_layout = QHBoxLayout()

        self.groupBox = QGroupBox('Custom Filter')

        self.input = QTextEdit()
        self.input.setText("0,0,0,0,0\n"
                           "0,0,0,0,0\n"
                           "0,0,1,0,0\n"
                           "0,0,0,0,0\n"
                           "0,0,0,0,0")

        self.input_layout.addWidget(self.input)
        self.groupBox.setLayout(self.input_layout)

        self.layout.addWidget(self.groupBox)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def get_values(self) -> np.ndarray:
        kernel_text = self.input.toPlainText()
        line_arr = kernel_text.split('\n')
        kernel_arr = []
        for line in line_arr:
            number_arr = line.split(',')
            temp_arr = []
            for number in number_arr:
                try:
                    temp_arr.append(int(number))
                except Exception:
                    pass
            kernel_arr.append(temp_arr)

        kernel = np.array(kernel_arr)
        if kernel.shape[0] % 2 != 1 and kernel.shape[1] % 2 != 1:
            raise ValueError("Invalid kernel size")
        return kernel
