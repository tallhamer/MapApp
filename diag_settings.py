import json
from http.client import responses

import PySide6.QtWidgets as qtw
import PySide6.QtNetwork as qtn

from ui.app_settings_dialog import Ui_SettingsDialog
from models.maprt import MapRTAPIManager

class SettingsDialog(qtw.QDialog, Ui_SettingsDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.w_pb_dicom_directory.clicked.connect(self._browse_for_dicom_directory)
        self.w_pb_test_connection.clicked.connect(self._test_api_connection)

    def _browse_for_dicom_directory(self):
        dir = qtw.QFileDialog.getExistingDirectory(self,
                                                   "Select location for DICOM RT files",
                                                   "."
                                                   )

        self.w_le_dicom_directory.setText(dir)

    def _test_api_connection(self):
        self.w_te_test_connectio_results.clear()

        self.maprt_api = MapRTAPIManager("https://maprtpkr.adventhealth.com:5000",
                                         "82212e3b-7edb-40e4-b346-c4fe806a1a0b",
                                         "VisionRT.Integration.Saturn/1.2.8"
                                         )

        self.maprt_api.manager.finished.connect(self._handle_test_results)

        self.maprt_api.get_status()
        self.maprt_api.get_treatment_rooms()

    def _handle_test_results(self, reply):
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
                print(json.dumps(json_data, indent=2))

                self.w_te_test_connectio_results.append('\nHeader {Name: Value} Pairs:')
                for header_name, header_value in reply.rawHeaderPairs():
                    self.w_te_test_connectio_results.append(
                        f'    {header_name.data().decode()} : {header_value.data().decode()}')

                self.w_te_test_connectio_results.append(f'\nData received:')
                self.w_te_test_connectio_results.append(json.dumps(json_data, indent=2))

                self.w_te_test_connectio_results.append('\n')


            elif call_type == 'Rooms':
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