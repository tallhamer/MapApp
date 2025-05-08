import json
import logging

import PySide6.QtWidgets as qtw

from ui.dicom_dialog import Ui_DicomDialog

from models.settings import AppSettings

class DicomFileDialog(qtw.QDialog, Ui_DicomDialog):
    def __init__(self):
        self.logger = logging.getLogger('MapApp.dlg_dicom_files.DicomFileDialog')
        self.logger.debug("Setting up the DicomFileDialog UI")
        super().__init__()
        self.setupUi(self)

        with open(r'.\settings.json', 'r') as settings:
            settings_data = json.load(settings)
            self.settings = AppSettings(**settings_data)

            self.dicom_data_directory = self.settings.dicom.dicom_data_directory

        self.w_pb_dicom_plan_path.clicked.connect(self.ui_open_dicom_plan_file)
        self.w_pb_dicom_structure_path.clicked.connect(self.ui_open_dicom_struct_file)

    def ui_open_dicom_plan_file(self):
        self.logger.debug("Select DICOM RT Plan File")
        file_path, _ = qtw.QFileDialog.getOpenFileName(self,
                                                      "Select DICOM RT Plan File",
                                                       self.dicom_data_directory,
                                                      "DICOM Files (*.dcm)"
                                                      )

        if file_path:
            self.logger.debug(f"'{file_path}' plan file selected in DicomFileDialog")
            self.w_le_dicom_plan_path.setText(file_path)

    def ui_open_dicom_struct_file(self):
        self.logger.debug("Select DICOM RT Structure Set File")
        file_path, _ = qtw.QFileDialog.getOpenFileName(self,
                                                      "Select DICOM RT Structure Set File",
                                                       self.dicom_data_directory,
                                                      "DICOM Files (*.dcm)"
                                                      )

        if file_path:
            self.logger.debug(f"'{file_path}' structure file selected in DicomFileDialog")
            self.w_le_dicom_structure_path.setText(file_path)