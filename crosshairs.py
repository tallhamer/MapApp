import pyqtgraph as pg
import PySide6.QtWidgets as qtw
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np

# Create application and window
app = qtw.QApplication([])
win = pg.GraphicsLayoutWidget(show=True, title="Image with Crosshairs")

# Add a ViewBox to manage the plot area
vb = pg.ViewBox()
image_item = pg.ImageItem()
vb.addItem(image_item)
win.addItem(vb)

# Load or generate image data
img_data = np.random.normal(size=(100, 100))
image_item.setImage(img_data)

# Create crosshair lines
v_line = pg.InfiniteLine(angle=90, movable=False)
h_line = pg.InfiniteLine(angle=0, movable=False)
vb.addItem(v_line, ignoreBounds=True)
vb.addItem(h_line, ignoreBounds=True)

# Create text item to display coordinates
text_item = pg.TextItem("", anchor=(0, 1))
win.addItem(text_item)

# Function to update crosshair and text position
def mouse_moved(evt):
    pos = evt[0]  # using signal proxy turns original event into tuple
    if vb.sceneBoundingRect().contains(pos):
        mouse_point = vb.mapSceneToView(pos)
        v_line.setPos(mouse_point.x())
        h_line.setPos(mouse_point.y())
        text_item.setText(f"x={mouse_point.x():.2f}, y={mouse_point.y():.2f}")
    else:
        text_item.setText("")

# Create signal proxy to track mouse movements
proxy = pg.SignalProxy(app.desktop().eventFilter, rateLimit=60, slot=mouse_moved)
vb.scene().sigMouseMoved.connect(proxy.signal)

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()