import PySide6.QtWidgets as qtw

from ui.obj_orientation_dialog import Ui_OrientationDialog

class OrientDialog(qtw.QDialog, Ui_OrientationDialog):
    def __init__(self):
        print('OrientDialog.__init__')
        super().__init__()
        self.setupUi(self)

        self.w_cb_obj_surface_orientation.addItems(["Current Plan", "HFS", "HFP", "FFS", "FFP"])