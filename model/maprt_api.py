import inspect
import requests

import PySide6.QtCore as qtc

class MapRTCaller(qtc.QObject):

    maprt_patient_id_updated = qtc.Signal()
    maprt_treatment_rooms_updated = qtc.Signal(dict)
    maprt_surfaces_updated = qtc.Signal(dict)

    def __init__(self, url, token, aget):
        print('MapRTCaller Function: ', inspect.stack()[0][3])
        print('\tCaller: ', inspect.stack()[1][3])

        super().__init__()
        self._api_url = url     # "https://maprtpkr.adventhealth.com:5000"
        self._token = token     # "82212e3b-7edb-40e4-b346-c4fe806a1a0b"
        self._user_agent = aget # "VisionRT.Integration.Saturn/1.2.8"

        self._header = {
            "Authorization": f"Bearer {self._token}",
            "User-Agent": self._user_agent
        }

        self._treatment_room_map = {}
        self._surface_map = {}
        self.surface_cache = {}
        self._map_cache = {}

        self._patient_id = None

        # Endpoints to code
        self._get_beam_delivery_status = f"/integration/GetBeamDeliveryStatus"

    @property
    def patient_id(self):
        return self._patient_id

    @patient_id.setter
    def patient_id(self, id):
        self._patient_id = id
        self.maprt_patient_id_updated.emit()

    def get_status(self):
        print('MapRTCaller Function: ', inspect.stack()[0][3])
        print('\tCaller: ', inspect.stack()[1][3])

        url = self._api_url + "/integration/ping"

        response = requests.get(url, headers=self._header, verify=False)

        if response.status_code == 200:
            print("Ping Request Successful!")
            # print(response.headers)
            # print(response.json())

        else:
            print(f"Request failed with status code: {response.status_code}")
            print(response.text)

        return (response.status_code)

    def get_all_treatment_rooms(self):
        print('MapRTCaller Function: ', inspect.stack()[0][3])
        print('\tCaller: ', inspect.stack()[1][3])

        url = self._api_url + "/integration/rooms"

        response = requests.get(url, headers=self._header, verify=False)

        if response.status_code == 200:
            print("Get All Treatment Rooms Request Successful!")
            # print(response.headers)
            # print(response.json())

            for room in response.json()['data']:
                self._treatment_room_map[room['name']] = (room['id'], room['coordinateSystem'])

            self.maprt_treatment_rooms_updated.emit(self._treatment_room_map)

            # for k, v in self._treatment_room_map.items():
            #     print(k, v)
        else:
            print(f"Request failed with status code: {response.status_code}")
            print(response.text)

    def get_single_treatment_room(self, room_name):
        print('MapRTCaller Function: ', inspect.stack()[0][3])
        print('\tCaller: ', inspect.stack()[1][3])

        url = self._api_url + f"/integration/rooms/{room_name}"

        response = requests.get(url, headers=self._header, verify=False)

        if response.status_code == 200:
            print("Set Treatment Room Request Successful!")
            # print(response.headers)
            # print(response.json())
        else:
            print(f"Request failed with status code: {response.status_code}")
            print(response.text)

    def get_surfaces_for_patient(self, patient_id):
        print('MapRTCaller Function: ', inspect.stack()[0][3])
        print('\tCaller: ', inspect.stack()[1][3])

        url = self._api_url + f"/integration/patients/{patient_id}/surfaces"

        response = requests.get(url, headers=self._header, verify=False)

        if response.status_code == 200:
            print("Get Patient Surfaces Request Successful!")
            # print(response.headers)
            # print(response.json())

            for surface in response.json()['data']:
                self._surface_map[surface['label']] = (surface['id'], surface['timeStamp'])

            self.maprt_surfaces_updated.emit(self._surface_map)

            for k, v in self._surface_map.items():
                print(k, v)

        else:
            print(f"Request failed with status code: {response.status_code}")
            print(response.text)

    def get_surface(self, surface_label):
        print('MapRTCaller Function: ', inspect.stack()[0][3])
        print('\tCaller: ', inspect.stack()[1][3])

        if surface_label in self.surface_cache:
            print("Using Cached Surface")
            return self.surface_cache[surface_label]

        surface_id, surface_timestamp = self._surface_map[surface_label]
        url = self._api_url + f"/integration/surfaces/{surface_id}"

        response = requests.get(url, headers=self._header, verify=False)

        if response.status_code == 200:
            print("Get Surface Request Successful!")
            # print(response.headers)
            # print(response.json())

            self.surface_cache[surface_label] = response.json()
            return response.json()
        else:
            print(f"Request failed with status code: {response.status_code}")
            print(response.text)
            return None

    def get_map(self, isocenter, couch_buffer, patient_buffer, surface_label, room_name, high_res=True):
        print('MapRTCaller Function: ', inspect.stack()[0][3])
        print('\tCaller: ', inspect.stack()[1][3])

        surface_id, surface_timestamp = self._surface_map[surface_label]
        treatment_room_id, coordinate_system = self._treatment_room_map[room_name]
        X, Y, Z = isocenter

        url = self._api_url + f"/integration/GetMap"

        body = {
            "CouchBuffer": couch_buffer,
            "PatientBuffer": patient_buffer,
            "HighResolution": high_res,
            "PatientSurfaceId": f"{surface_id}",
            "TreatmentRoomId": f"{treatment_room_id}",
            "Isocenter": {
                "x": X,
                "y": Y,
                "z": Z,
                "CoordinateSystem": f"{coordinate_system}",
            }
        }

        response = requests.post(url, json=body, headers=self._header, verify=False)

        if response.status_code == 200:
            print("Get Map Request Successful!")
            # print(response.headers)
            # print(response.text)
        else:
            print(f"Request failed with status code: {response.status_code}")
            print(response.text)



if __name__ == '__main__':
    caller = MapRTCaller("https://maprtpkr.adventhealth.com:5000",
                         "82212e3b-7edb-40e4-b346-c4fe806a1a0b",
                         "VisionRT.Integration.Saturn/1.2.8"
                         )
    caller.get_status()
    caller.get_all_treatment_rooms()
    caller.get_single_treatment_room('Truebeam e15')
    caller.get_surfaces_for_patient('PHY0019')
    caller.get_surface('20250404 222044')
    # caller.get_map([0,0,0],
    #                20,
    #                20,
    #                '20250404 222044',
    #                'Truebeam',
    #                high_res=False)