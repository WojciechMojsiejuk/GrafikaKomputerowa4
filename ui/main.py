import sys

from PyQt5.QtWidgets import QApplication
from PyQt5 import uic
from ui.window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    uic.loadUi('main.ui', window)
    window.init_ui()
    window.show()

    sys.exit(app.exec_())
