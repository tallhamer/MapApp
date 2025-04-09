import sys
import json
from enum import IntEnum

import PySide6.QtCore as qtc
import PySide6.QtNetwork as qtn

class MapRTCallType(IntEnum):
    Ping = 0
    Rooms = 1
    Room = 2
    Surfaces = 3
    Surface = 4
    Map = 5
    Beam = 6

class MapRTAPIManager(qtc.QObject):
    status_returned = qtc.Signal(str)

    def __init__(self, api_url, token, user_agent):
        super().__init__()

        self._api_url = api_url
        self._token = token
        self._user_agent = user_agent

        self._header = qtn.QHttpHeaders()
        self._header.insert(0, "Content-Type", "application/json")
        self._header.append("Authorization", f"Bearer {self._token}")
        self._header.append("User-Agent", self._user_agent)

        self.ssl_config = qtn.QSslConfiguration.defaultConfiguration()
        self.ssl_config.setPeerVerifyMode(qtn.QSslSocket.PeerVerifyMode.VerifyNone)
        self.ssl_config.setProtocol(qtn.QSsl.SslProtocol.AnyProtocol)

        self.manager = qtn.QNetworkAccessManager()

        self._treatment_room_map = {}
        self._surface_map = {}
        self.surface_cache = {}
        self._map_cache = {}

        self._patient_id = None

        # Endpoints to code
        self._get_beam_delivery_status = f"/integration/GetBeamDeliveryStatus"

    def get_status(self):
        url = self._api_url + "/integration/ping"

        request = qtn.QNetworkRequest(qtc.QUrl(url))
        request.setHeaders(self._header)
        request.setSslConfiguration(self.ssl_config)
        request.setAttribute(qtn.QNetworkRequest.Attribute.User, MapRTCallType.Ping)
        request.setAttribute(qtn.QNetworkRequest.Attribute.CacheLoadControlAttribute,
                             qtn.QNetworkRequest.CacheLoadControl.PreferCache
                             )

        self.manager.get(request)

    def get_treatment_rooms (self):
        url = self._api_url + "/integration/rooms"

        request = qtn.QNetworkRequest(qtc.QUrl(url))
        request.setHeaders(self._header)
        request.setSslConfiguration(self.ssl_config)
        request.setAttribute(qtn.QNetworkRequest.Attribute.User, MapRTCallType.Rooms)
        request.setAttribute(qtn.QNetworkRequest.Attribute.CacheLoadControlAttribute,
                             qtn.QNetworkRequest.CacheLoadControl.PreferCache
                             )

        self.manager.get(request)

        # for room in response.json()['data']:
        #     self._treatment_room_map[room['name']] = (room['id'], room['coordinateSystem'])


    def get_treatment_room(self, room_name):
        url = self._api_url + f"/integration/rooms/{room_name}"

        request = qtn.QNetworkRequest(qtc.QUrl(url))
        request.setHeaders(self._header)
        request.setSslConfiguration(self.ssl_config)
        request.setAttribute(qtn.QNetworkRequest.Attribute.User, MapRTCallType.Room)
        request.setAttribute(qtn.QNetworkRequest.Attribute.CacheLoadControlAttribute,
                             qtn.QNetworkRequest.CacheLoadControl.PreferCache
                             )

        self.manager.get(request)

    def get_patient_surfaces(self, patient_id):
        url = self._api_url + f"/integration/patients/{patient_id}/surfaces"

        request = qtn.QNetworkRequest(qtc.QUrl(url))
        request.setHeaders(self._header)
        request.setSslConfiguration(self.ssl_config)
        request.setAttribute(qtn.QNetworkRequest.Attribute.User, MapRTCallType.Surfaces)
        request.setAttribute(qtn.QNetworkRequest.Attribute.CacheLoadControlAttribute,
                             qtn.QNetworkRequest.CacheLoadControl.PreferCache
                             )

        self.manager.get(request)

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
        request.setAttribute(qtn.QNetworkRequest.Attribute.User, MapRTCallType.Surface)
        request.setAttribute(qtn.QNetworkRequest.Attribute.CacheLoadControlAttribute,
                             qtn.QNetworkRequest.CacheLoadControl.PreferCache
                             )

        self.manager.get(request)

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
        request.setHeaders(self._header)
        request.setSslConfiguration(self.ssl_config)
        request.setAttribute(qtn.QNetworkRequest.Attribute.User, MapRTCallType.Map)
        request.setAttribute(qtn.QNetworkRequest.Attribute.CacheLoadControlAttribute,
                             qtn.QNetworkRequest.CacheLoadControl.PreferCache
                             )

        data = json.dumps(body).encode('utf-8')
        self.manager.post(request, qtc.QByteArray(data))

    def handle_reply(self, reply):
        if reply.error() == qtn.QNetworkReply.NetworkError.NoError:
            status_code = reply.attribute(qtn.QNetworkRequest.HttpStatusCodeAttribute)
            print(f'Call to: {reply.request().url().toString()}')
            print(f"Status Code: {status_code}")
            call_type = reply.request().attribute(qtn.QNetworkRequest.Attribute.User)
            print(f"Call Type Code: {call_type}")
            data = reply.readAll()
            text = str(data, 'utf-8')

            # Process based on call type that finished
            if call_type == MapRTCallType.Ping:
                json_data = json.loads(text)
                print(f"Call Type Name: Ping")
                print("Data received:")
                print(json.dumps(json_data, indent=2))

            elif call_type == MapRTCallType.Rooms:
                json_data = json.loads(text)
                print(f"Call Type Name: Rooms")
                print("Data received:")
                print(json.dumps(json_data, indent=2))
            elif call_type == MapRTCallType.Room:
                json_data = json.loads(text)
                print(f"Call Type Name: Room")
                print("Data received:")
                print(json.dumps(json_data, indent=2))
            elif call_type == MapRTCallType.Surfaces:
                json_data = json.loads(text)
                print(f"Call Type Name: Surfaces")
                print("Data received:")
                print(json.dumps(json_data, indent=2))
            elif call_type == MapRTCallType.Surface:
                json_data = json.loads(text)
                json_data['data'] = json_data['data'][0:1000]
                print(f"Call Type Name: Surface")
                print("Data received:")
                print(json.dumps(json_data, indent=2))
            elif call_type == MapRTCallType.Map:
                print(f"Call Type Name: Map")
                print("Data received:")
                print(text)

        else:
            status_code = reply.attribute(qtn.QNetworkRequest.HttpStatusCodeAttribute)
            print(f'Call to: {reply.request().url().toString()}')
            print(f"Status Code: {status_code}")
            print("Error:", reply.errorString())
            print(reply.request().rawHeaderList())

        reply.deleteLater()

if __name__ == '__main__':
    import time
    import PySide6.QtWidgets as qtw

    app = qtw.QApplication(sys.argv)

    start = time.time()
    network_manager = MapRTAPIManager("https://maprtpkr.adventhealth.com:5000",
                                      "82212e3b-7edb-40e4-b346-c4fe806a1a0b",
                                      "VisionRT.Integration.Saturn/1.2.8"
                                      )
    network_manager.manager.finished.connect(network_manager.handle_reply)

    print('Calling Ping')
    network_manager.get_status()
    print('Calling Rooms')
    network_manager.get_treatment_rooms()
    print('Calling Room')
    network_manager.get_treatment_room('TrueBeam')
    print('Calling Surfaces')
    network_manager.get_patient_surfaces('PHY0019')
    print('Calling Surface')
    network_manager.get_surface("2e36321f-19de-49cd-899d-c772da051316")
    print('Calling Map')
    network_manager.get_map()
    # # Extra calls
    # print('Calling Map')
    # network_manager.get_map()
    # network_manager.get_map()
    print("Elapsed Time:", time.time() - start)

    sys.exit(app.exec())