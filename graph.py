import sys
import pyqtgraph as pg
from PySide2 import QtWidgets
import numpy as np

class PlotWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.plot_widget = pg.PlotWidget()
        self.setCentralWidget(self.plot_widget)

        self.crosshair_v = pg.InfiniteLine(angle=90, movable=False)
        self.crosshair_h = pg.InfiniteLine(angle=0, movable=False)
        self.plot_widget.addItem(self.crosshair_v, ignoreBounds=True)
        self.plot_widget.addItem(self.crosshair_h, ignoreBounds=True)

        self.plot_widget.scene().sigMouseMoved.connect(self.mouse_moved)
        self.data = np.random.normal(size=100)
        self.plot_widget.plot(self.data)

    def mouse_moved(self, event):
        pos = event
        if self.plot_widget.sceneBoundingRect().contains(pos):
            mouse_point = self.plot_widget.vb.mapSceneToView(pos)
            self.crosshair_v.setPos(mouse_point.x())
            self.crosshair_h.setPos(mouse_point.y())

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = PlotWindow()
    window.show()
    sys.exit(app.exec_())