from PySide6.QtWidgets import QWidget, QHBoxLayout
from PySide6.QtCore import Qt
import pyqtgraph as pg  # type: ignore
import numpy as np
from hypmix.util_classes import CursorInfo
from hypmix.io import ModelResult
import cmap


class ModelViewerWidget(QWidget):
    """Shows the bar plot of the modeled fractions."""

    def __init__(self) -> None:
        super().__init__()

        layout = QHBoxLayout()

        self.spec_plot = pg.PlotWidget()
        self.bar_plot = pg.PlotWidget()

        self.spec_item = pg.PlotDataItem()
        self.model_item = pg.PlotDataItem()
        self.bar_items: list[pg.BarGraphItem] = []
        self._legend_curves: list[pg.PlotDataItem] = []

        self.spec_plot.addItem(self.spec_item)
        self.spec_plot.addItem(self.model_item)

        layout.addWidget(self.spec_plot)
        layout.addWidget(self.bar_plot)
        self.setLayout(layout)

        self._data_set = False
        self._bar_legend: pg.LegendItem = self.bar_plot.addLegend()

    def set_model(self, model: ModelResult):
        # Resetting Data from previous model
        for i in self.bar_items:
            self.bar_plot.removeItem(i)
        for j in self._legend_curves:
            self.bar_plot.removeItem(j)
        self._legend_curves = []
        self.bar_items = []

        self.wvl: np.ndarray = model.endmembers.endmember_list[0].spectrum.wvl
        self.model_cube: np.ndarray = model.unmixed_image.model
        self.frac_cube = model.unmixed_image.fracs
        self._num_endmembers = len(model.endmembers.endmember_list)

        base_cmap = cmap.Colormap("crameri:hawaii")
        ncolors = len(model.endmembers.endmember_list)
        cmap_lut = base_cmap.lut(ncolors) * 255
        for n, em in enumerate(model.endmembers.endmember_list):
            c = pg.mkColor(tuple(cmap_lut[n, :]))
            _curve = pg.PlotDataItem(
                pen=pg.mkPen(color=c, width=10), name=em.name
            )
            _brush = pg.mkBrush(color=c)
            _bar = pg.BarGraphItem(x=[n], height=0, width=0.8, brush=_brush)

            self.bar_items.append(_bar)
            self._legend_curves.append(_curve)

            self.bar_plot.addItem(_bar)
            self.bar_plot.addItem(_curve)

            print(f"{n}, added item.")

    def set_data(self, data: np.ndarray):
        if data is not None:
            self.spec_cube = data
            self._data_set = True
        else:
            self._data_set = False

    def update_plots(self, ci: CursorInfo):
        if self._data_set:
            self.spec_item.setData(
                x=self.wvl,
                y=self.spec_cube[ci.yint, ci.xint, :],
                pen=pg.mkPen(style=Qt.PenStyle.DashLine, width=1),
            )
        self.model_item.setData(
            x=self.wvl,
            y=self.model_cube[ci.yint, ci.xint, :-1],
            pen=pg.mkPen(color="red", width=1),
        )

        _sum = 0
        for n, i in enumerate(self.bar_items):
            h = self.frac_cube[ci.yint, ci.xint, n]
            _sum += h
            i.setOpts(height=[h])
