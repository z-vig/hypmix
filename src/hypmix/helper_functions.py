from PySide6.QtWidgets import QApplication
from hypmix.mixview.main_window import MixView
import sys


def open_mixview():
    app = QApplication(sys.argv)
    main = MixView()
    main.show()
    app.exec()


if __name__ == "__main__":
    open_mixview()
