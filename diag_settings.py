import json
import base64
import binascii
from http.client import responses

import PySide6.QtWidgets as qtw
import PySide6.QtNetwork as qtn

from ui.app_settings_dialog import Ui_SettingsDialog
from models.maprt import MapRTAPIManager
from models.settings import AppSettings

class SettingsDialog(qtw.QDialog, Ui_SettingsDialog):
    def __init__(self):
        print('SettingsDialog.__init__')
        super().__init__()
        self.setupUi(self)

        with open(r'.\settings.json', 'r') as settings:
            settings_data = json.load(settings)
            self.settings = AppSettings(**settings_data)

            dicom_dir = self.settings.dicom.dicom_data_directory
            self.w_le_dicom_directory.setText(dicom_dir)

            arc_check_resolution = self.settings.dicom.arc_check_resolution
            self.w_sb_arc_check_resolution.setValue(arc_check_resolution)

            maprt_api_url = self.settings.maprt.api_url
            self.w_le_api_url.setText(maprt_api_url)

            maprt_api_token = binascii.unhexlify(base64.b64decode(self.settings.maprt.api_token.encode('utf-8'))).decode('utf-8')
            self.w_le_api_token.setText(maprt_api_token)

            maprt_api_user_agent = self.settings.maprt.api_user_agent
            self.w_le_api_user_agent.setText(maprt_api_user_agent)

        self.w_pb_dicom_directory.clicked.connect(self._browse_for_dicom_directory)
        self.w_pb_test_connection.clicked.connect(self._test_api_connection)

    def _browse_for_dicom_directory(self):
        print('SettingsDialog._browse_for_dicom_directory')
        dir = qtw.QFileDialog.getExistingDirectory(self,
                                                   "Select location for DICOM RT files",
                                                   "."
                                                   )

        self.w_le_dicom_directory.setText(dir)

    def _test_api_connection(self):
        print('SettingsDialog._test_api_connection')
        self.w_te_test_connectio_results.clear()

        self.maprt_api = MapRTAPIManager(self.w_le_api_url.text(),
                                         self.w_le_api_token.text(),
                                         self.w_le_api_user_agent.text()
                                         )

        self.maprt_api.manager.finished.connect(self._handle_test_results)

        self.maprt_api.get_status()
        self.maprt_api.get_treatment_rooms()

    def _handle_test_results(self, reply):
        print('SettingsDialog._handle_test_results')
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
                print('SettingsDialog._handle_test_results.Ping')
                json_data = json.loads(text)

                self.w_te_test_connectio_results.append('\nHeader {Name: Value} Pairs:')
                for header_name, header_value in reply.rawHeaderPairs():
                    self.w_te_test_connectio_results.append(
                        f'    {header_name.data().decode()} : {header_value.data().decode()}')

                self.w_te_test_connectio_results.append(f'\nData received:')
                self.w_te_test_connectio_results.append(json.dumps(json_data, indent=2))

                self.w_te_test_connectio_results.append('\n')


            elif call_type == 'Rooms':
                print('SettingsDialog._handle_test_results.Rooms')
                json_data = json.loads(text)

                self.w_te_test_connectio_results.append('\nHeader {Name: Value} Pairs:')
                for header_name, header_value in reply.rawHeaderPairs():
                    self.w_te_test_connectio_results.append(
                        f'    {header_name.data().decode()} : {header_value.data().decode()}')

                self.w_te_test_connectio_results.append(f'\nData received:')
                self.w_te_test_connectio_results.append(json.dumps(json_data, indent=2))

                self.w_te_test_connectio_results.append('\n')
            else:
                pass

        else:
            status_code = reply.attribute(qtn.QNetworkRequest.Attribute.HttpStatusCodeAttribute)
            call = f'Call to: {reply.request().url().toString()}'
            status = f"Status Code: {status_code}"
            error = f"Error: {reply.errorString()}"
            msg = f'{call}\n{status}\n{error}'

            self.w_te_test_connectio_results.append(msg)
            self.w_te_test_connectio_results.append('\n')

        reply.deleteLater()