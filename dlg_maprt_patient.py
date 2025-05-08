import logging

import PySide6.QtWidgets as qtw

from ui.maprt_patient_dialog import Ui_MapRTPatientDialog

class MapRTPatientDialog(qtw.QDialog, Ui_MapRTPatientDialog):
    def __init__(self):
        self.logger = logging.getLogger('MapApp.dlg_maprt_patient.MapRTPatientDialog')
        self.logger.debug("Setting up the MapRTPatientDialog UI")
        super().__init__()
        self.setupUi(self)

        self.w_cb_patient_orientation.addItems(["HFS", "HFP", "FFS", "FFP"])