import PySide6.QtWidgets as qtw

from ui.obj_orientation_dialog import Ui_OrientationDialog

import logging
logger = logging.getLogger('MapApp')

class OrientDialog(qtw.QDialog, Ui_OrientationDialog):
    def __init__(self):
        logger.debug("Setting up the OrientDialog UI")
        super().__init__()
        self.setupUi(self)

        self.w_cb_obj_surface_orientation.addItems(["Current Plan", "HFS", "HFP", "FFS", "FFP"])