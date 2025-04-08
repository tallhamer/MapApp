import sys
import json

import PySide6.QtCore as qtc
import PySide6.QtNetwork as qtn
import PySide6.QtWidgets as qtw



class NetworkManager(qtc.QObject):
    status_returned = qtc.Signal(str)

    def __init__(self):
        super().__init__()

        self._api_url = "https://maprtpkr.adventhealth.com:5000"
        self._token = "82212e3b-7edb-40e4-b346-c4fe806a1a0b"
        self._user_agent = "VisionRT.Integration.Saturn/1.2.8"

        self._header = qtn.QHttpHeaders()
        self._header.insert(0, "Content-Type", "application/json")
        self._header.append("Authorization", f"Bearer {self._token}")
        self._header.append("User-Agent", self._user_agent)

        self.manager = qtn.QNetworkAccessManager()
        self.manager.finished.connect(self.handle_reply)

        self.ssl_config = qtn.QSslConfiguration.defaultConfiguration()
        self.ssl_config.setPeerVerifyMode(qtn.QSslSocket.PeerVerifyMode.VerifyNone)
        self.ssl_config.setProtocol(qtn.QSsl.SslProtocol.AnyProtocol)

        self._treatment_room_map = {}
        self._surface_map = {}
        self.surface_cache = {}
        self._map_cache = {}

        self._patient_id = None

        # Endpoints to code
        self._get_beam_delivery_status = f"/integration/GetBeamDeliveryStatus"

    def get_status(self):
        url = self._api_url + self._get_status

        request = qtn.QNetworkRequest(qtc.QUrl(url))
        request.setHeaders(self._header)
        request.setSslConfiguration(self.ssl_config)

        reply = self.manager.get(request)

    def get_treatment_rooms (self):
        url = self._api_url + self._get_treatment_rooms

        request = qtn.QNetworkRequest(qtc.QUrl(url))
        request.setHeaders(self._header)
        request.setSslConfiguration(self.ssl_config)

        reply = self.manager.get(request)

        # for room in response.json()['data']:
        #     self._treatment_room_map[room['name']] = (room['id'], room['coordinateSystem'])


    def get_treatment_room(self, room_name):
        url = self._api_url + self._get_treatment_rooms + f"/{room_name}"

        request = qtn.QNetworkRequest(qtc.QUrl(url))
        request.setHeaders(self._header)
        request.setSslConfiguration(self.ssl_config)

        reply = self.manager.get(request)

    def get_patient_surfaces(self, patient_id):
        url = self._api_url + f"/integration/patients/{patient_id}/surfaces"

        request = qtn.QNetworkRequest(qtc.QUrl(url))
        request.setHeaders(self._header)
        request.setSslConfiguration(self.ssl_config)

        reply = self.manager.get(request)

        # for surface in response.json()['data']:
        #     self._surface_map[surface['label']] = (surface['id'], surface['timeStamp'])
        #
        # self.maprt_surfaces_updated.emit(self._surface_map)

    def get_surface(self, surface_id):
        # if surface_label in self.surface_cache:
        #     print("Using Cached Surface")
        #     return self.surface_cache[surface_label]
        #
        # surface_id, surface_timestamp = self._surface_map[surface_label]
        url = self._api_url + f"/integration/surfaces/{surface_id}"

        request = qtn.QNetworkRequest(qtc.QUrl(url))
        request.setHeaders(self._header)
        request.setSslConfiguration(self.ssl_config)

        reply = self.manager.get(request)

    def get_map(self):
        url = self._api_url + f"/integration/GetMap"

        body = {
            "CouchBuffer": 20,
            "PatientBuffer": 20,
            "HighResolution": False,
            "PatientSurfaceId": "2e36321f-19de-49cd-899d-c772da051316",
            "TreatmentRoomId": "eaf6df9d-8e60-c46a-4e6f-ca55e7470545",
            "Isocenter": {
                "x": 0,
                "y": 0,
                "z": 0,
                "CoordinateSystem": "IEC_61217"
            }
        }

        request = qtn.QNetworkRequest(qtc.QUrl(url))
        # Set a header
        request.setHeaders(self._header)
        request.setSslConfiguration(self.ssl_config)

        data = json.dumps(body).encode('utf-8')
        self.manager.post(request, qtc.QByteArray(data))

    def handle_reply(self, reply):
        if reply.error() == qtn.QNetworkReply.NetworkError.NoError:
            status_code = reply.attribute(qtn.QNetworkRequest.HttpStatusCodeAttribute)
            print(f'Call to: {reply.request().url().toString()}')
            print(f"Status Code: {status_code}")
            data = reply.readAll()
            text = str(data, 'utf-8')

            try:
                json_data = json.loads(text)
                print("Data received:")
                print(json.dumps(json_data, indent=4))
            except:
                print(text)

            # if reply.request().url() == self._api_url + self._get_status:
            #     data = reply.readAll()
            #     text = str(data, 'utf-8')
            #     json_data = json.loads(text)
            #     print("Data received:")
            #     print(json.dumps(json_data, indent=4))
            # elif reply.request().url() == self._api_url + self._get_treatment_rooms:
            #     data = reply.readAll()
            #     text = str(data, 'utf-8')
            #     json_data = json.loads(text)
            #     print("Data received:")
            #     print(json.dumps(json_data, indent=4))

        else:
            status_code = reply.attribute(qtn.QNetworkRequest.HttpStatusCodeAttribute)
            print(f'Call to: {reply.request().url().toString()}')
            print(f"Status Code: {status_code}")
            print("Error:", reply.errorString())
            print(reply.request().rawHeaderList())

        reply.deleteLater()

if __name__ == '__main__':
    import time


    app = qtw.QApplication(sys.argv)

    start = time.time()
    network_manager = NetworkManager()
    network_manager.get_status()
    network_manager.get_treatment_rooms()
    network_manager.get_treatment_room('TrueBeam')
    network_manager.get_patient_surfaces('PHY0019')
    # network_manager.get_surface("2e36321f-19de-49cd-899d-c772da051316")
    network_manager.get_map()
    network_manager.get_map()
    network_manager.get_map()
    print("Elapsed Time:", time.time() - start)

    sys.exit(app.exec())