import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from hypmix.mixview.main_window import MixView


def mixview(model_result_path: Path):
    app = QApplication(sys.argv)

    # For dev
    main = MixView(
        base=Path("D:/moon_data/m3/Gruithuisen_Region/GDOMES_Mosaic/"),
        model=model_result_path,
    )

    # main = MixView()
    main.show()
    app.exec()


if __name__ == "__main__":
    mixview(Path("D:/moon_data/m3/Gruithuisen_Region/model_results.hdf5"))
