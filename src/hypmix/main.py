# flake8: noqa

from PySide6.QtWidgets import QApplication
from hypmix.mixview.main_window import MixView
import sys
from pathlib import Path


def cubeview():
    app = QApplication(sys.argv)
    main = MixView(
        base=Path("D:/moon_data/m3/Gruithuisen_Region/Gruithuisen_Mosaics/"),
        model=Path(
            "D:/moon_data/m3/Gruithuisen_Region/Gruithuisen_Mosaics/M3G_GDOMES_mixmodel.hdf5"
        ),
    )
    main.show()
    app.exec()


def main():
    cubeview()
