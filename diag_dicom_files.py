import json

import PySide6.QtWidgets as qtw

from ui.dicom_dialog import Ui_DicomDialog

from models.settings import AppSettings

class DicomFileDialog(qtw.QDialog, Ui_DicomDialog):
    def __init__(self):
        print('OrientDialog.__init__')
        super().__init__()
        self.setupUi(self)

        with open(r'.\settings.json', 'r') as settings:
            settings_data = json.load(settings)
            self.settings = AppSettings(**settings_data)

            self.dicom_data_directory = self.settings.dicom.dicom_data_directory

        self.w_pb_dicom_plan_path.clicked.connect(self.ui_open_dicom_plan_file)
        self.w_pb_dicom_structure_path.clicked.connect(self.ui_open_dicom_struct_file)

    def ui_open_dicom_plan_file(self):
        print('MapRTPatientDialog.ui_open_dicom_plan_files')
        file_path, _ = qtw.QFileDialog.getOpenFileName(self,
                                                      "Select DICOM Plan File",
                                                       self.dicom_data_directory,
                                                      "DICOM Files (*.dcm)"
                                                      )

        if file_path:
            self.w_le_dicom_plan_path.setText(file_path)

    def ui_open_dicom_struct_file(self):
        print('MapRTPatientDialog.ui_open_dicom_plan_files')
        file_path, _ = qtw.QFileDialog.getOpenFileName(self,
                                                      "Select DICOM Structure Set File",
                                                       self.dicom_data_directory,
                                                      "DICOM Files (*.dcm)"
                                                      )

        if file_path:
            self.w_le_dicom_structure_path.setText(file_path)