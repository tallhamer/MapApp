import PySide6.QtWidgets as qtw

from ui.maprt_patient_dialog import Ui_MapRTPatientDialog

import logging
logger = logging.getLogger('MapApp')

class MapRTPatientDialog(qtw.QDialog, Ui_MapRTPatientDialog):
    def __init__(self):
        print('OrientDialog.__init__')
        super().__init__()
        self.setupUi(self)

        self.w_cb_patient_orientation.addItems(["HFS", "HFP", "FFS", "FFP"])