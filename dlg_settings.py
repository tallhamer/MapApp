import json
import base64
import logging
import binascii
from http.client import responses

import PySide6.QtWidgets as qtw
import PySide6.QtNetwork as qtn

from ui.app_settings_dialog import Ui_SettingsDialog
from models.maprt import MapRTAPIManager
from models.settings import AppSettings

class SettingsDialog(qtw.QDialog, Ui_SettingsDialog):
    def __init__(self):
        self.logger = logging.getLogger('MapApp.dlg_settings.SettingsDialog')
        self.logger.debug("Setting up the SettingsDialog UI")
        super().__init__()
        self.setupUi(self)

        self.logger.debug("Accessing the setting.json file to load current settings in SettingsDialog")
        with open(r'.\settings.json', 'r') as settings:
            settings_data = json.load(settings)
            self.settings = AppSettings(**settings_data)

            dicom_dir = self.settings.dicom.dicom_data_directory
            self.w_le_dicom_directory.setText(dicom_dir)
            self.logger.info(f"Current DICOM directory {dicom_dir} loaded in SettingsDialog")

            arc_check_resolution = self.settings.dicom.arc_check_resolution
            self.w_sb_arc_check_resolution.setValue(arc_check_resolution)
            self.logger.info(f"Current arc validation resolution set to {arc_check_resolution} degree loaded in SettingsDialog")

            self.w_cb_recon_method.addItems(['Zero-Crossing',
                                             'Marching Cubes',
                                             'Contour Isosurface'
                                             ])
            surface_recon_method = self.settings.dicom.surface_recon_method
            self.logger.info(
                f"Current surface reconstruction method for DICOM contours is set to {surface_recon_method} in SettingsDialog")
            self.w_cb_recon_method.currentIndexChanged.connect(self._surface_recon_method_changed)
            self.w_cb_recon_method.setCurrentText(surface_recon_method)
            self._surface_recon_method_changed()

            pixel_spacing_x = self.settings.dicom.pixel_spacing_x
            self.logger.info(
                f"Current pixel spacing 'x' is set to {pixel_spacing_x} for surface reconstruction in SettingsDialog")
            self.w_dsb_pixel_spacing_x.setValue(pixel_spacing_x)

            pixel_spacing_y = self.settings.dicom.pixel_spacing_y
            self.logger.info(
                f"Current pixel spacing 'y' is set to {pixel_spacing_y} for surface reconstruction in SettingsDialog")
            self.w_dsb_pixel_spacing_y.setValue(pixel_spacing_y)

            self.w_cb_contours_to_keep.addItems(['ALL', 'CCW', 'CW'])
            contours_to_keep = self.settings.dicom.contours_to_keep
            self.w_cb_contours_to_keep.setCurrentText(contours_to_keep)
            self.logger.info(
                f"Contours to keep from DICOM RT Structure File is set to {contours_to_keep} in SettingsDialog")

            maprt_api_url = self.settings.maprt.api_url
            self.w_le_api_url.setText(maprt_api_url)
            self.logger.info(f"Current MapRT API URL of {maprt_api_url} loaded in SettingsDialog")

            maprt_api_token = binascii.unhexlify(base64.b64decode(self.settings.maprt.api_token.encode('utf-8'))).decode('utf-8')
            self.w_le_api_token.setText(maprt_api_token)
            self.logger.info(f"Current MapRT API token of {maprt_api_token} loaded in SettingsDialog")

            maprt_api_user_agent = self.settings.maprt.api_user_agent
            self.w_le_api_user_agent.setText(maprt_api_user_agent)
            self.logger.info(f"Current MapRT API User Agent of {maprt_api_user_agent} loaded in SettingsDialog")

        self.w_pb_dicom_directory.clicked.connect(self._browse_for_dicom_directory)
        self.w_pb_test_connection.clicked.connect(self._test_api_connection)

    def _browse_for_dicom_directory(self):
        self.logger.debug("User browsing for new DICOM directory in SettingsDialog")
        dir = qtw.QFileDialog.getExistingDirectory(self,
                                                   "Select location for DICOM RT files",
                                                   "."
                                                   )

        # TODO: Check results before setting
        self.w_le_dicom_directory.setText(dir)

    def _surface_recon_method_changed(self):
        if self.w_cb_recon_method.currentText() in ["Marching Cubes", "Contour Isosurface"]:
            self.w_l_pixel_spacing_x.setVisible(True)
            self.w_dsb_pixel_spacing_x.setVisible(True)
            self.w_l_pixel_spacing_y.setVisible(True)
            self.w_dsb_pixel_spacing_y.setVisible(True)
        else:
            self.w_l_pixel_spacing_x.setVisible(False)
            self.w_dsb_pixel_spacing_x.setVisible(False)
            self.w_l_pixel_spacing_y.setVisible(False)
            self.w_dsb_pixel_spacing_y.setVisible(False)

    def _test_api_connection(self):
        self.logger.debug("User testing MapRT API connection in SettingsDialog")
        self.w_te_test_connectio_results.clear()

        self.maprt_api = MapRTAPIManager(self.w_le_api_url.text(),
                                         self.w_le_api_token.text(),
                                         self.w_le_api_user_agent.text()
                                         )

        self.maprt_api.manager.finished.connect(self._handle_test_results)

        self.maprt_api.get_status()
        # self.maprt_api.get_treatment_rooms()

    def _handle_test_results(self, reply):
        self.logger.debug("Handling MapRT API connection test results in SettingsDialog")
        if reply.error() == qtn.QNetworkReply.NetworkError.NoError:
            attributes = reply.request().attribute(qtn.QNetworkRequest.Attribute.User)
            call_type, args = attributes.split(':')
            status_code = reply.attribute(qtn.QNetworkRequest.Attribute.HttpStatusCodeAttribute)

            self.w_te_test_connectio_results.append(#00aaff
                f"Call to: {reply.request().url().toString()}")
            self.w_te_test_connectio_results.append(f'HTTP Status Code: {status_code} {responses[status_code]}')
            self.w_te_test_connectio_results.append(f'Call Type Code: {call_type}')

            data = reply.readAll()
            text = str(data, 'utf-8')

            # Process reply based on call type that was executed
            if call_type == 'Ping':
                json_data = json.loads(text)

                if json_data["success"]:
                    qtw.QMessageBox.information(self, "Information",
                                                "MapRT API Ping Successful!",
                                                qtw.QMessageBox.Ok
                                                )
                    self.logger.debug("MapRT API Ping Successful!")
                else:
                    msg = f"MapRT API Ping Failed\nError Code: {json_data["errorCode"]}"
                    qtw.QMessageBox.critical(self, "Connection Errors Detected",
                                                msg,
                                                qtw.QMessageBox.Ok
                                                )
                    self.logger.debug(msg)

                self.w_te_test_connectio_results.append('\nHeader {Name: Value} Pairs:')
                for header_name, header_value in reply.rawHeaderPairs():
                    self.w_te_test_connectio_results.append(
                        f'    {header_name.data().decode()} : {header_value.data().decode()}')

                self.w_te_test_connectio_results.append(f'\nData received:')
                self.w_te_test_connectio_results.append(json.dumps(json_data, indent=2))

                self.w_te_test_connectio_results.append('\n')

            # elif call_type == 'Rooms':
            #     print('SettingsDialog._handle_test_results.Rooms')
            #     json_data = json.loads(text)
            #
            #     self.w_te_test_connectio_results.append('\nHeader {Name: Value} Pairs:')
            #     for header_name, header_value in reply.rawHeaderPairs():
            #         self.w_te_test_connectio_results.append(
            #             f'    {header_name.data().decode()} : {header_value.data().decode()}')
            #
            #     self.w_te_test_connectio_results.append(f'\nData received:')
            #     self.w_te_test_connectio_results.append(json.dumps(json_data, indent=2))
            #
            #     self.w_te_test_connectio_results.append('\n')
            # else:
            #     pass

        else:
            status_code = reply.attribute(qtn.QNetworkRequest.Attribute.HttpStatusCodeAttribute)
            call = f'Call to: {reply.request().url().toString()}'
            status = f"Status Code: {status_code}"
            error = f"Error: {reply.errorString()}"
            msg = f'{call}\n{status}\n{error}'

            self.logger.debug(msg)
            qtw.QMessageBox.critical(self, "Connection Errors Detected",
                                     msg,
                                     qtw.QMessageBox.Ok
                                     )

            self.w_te_test_connectio_results.append(msg)
            self.w_te_test_connectio_results.append('\n')


        reply.deleteLater()