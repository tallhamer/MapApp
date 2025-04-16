import PySide6.QtCore as qtc
import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg

from ui.obj_orientation_dialog import Ui_OrientationDialog

class OrientDialog(qtw.QDialog, Ui_OrientationDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.w_cb_obj_surface_orientation.addItems(["Current Plan", "HFS", "HFP", "FFS", "FFP"])