import json
from http.client import responses
import PySide6.QtCore as qtc
import PySide6.QtNetwork as qtn

from network import MapRTAPIManager, MapRTCallType

class PlanContext(qtc.QObject):
    def __init__(self):
        super().__init__()

        self._isocenter = None              # list
        self._patient_orientation = None    # str
        self._structures = {}               # structure name: vtk_actor
        self._current_structure = None      # vtk_actor
        self._beams = []                    # list of lists for beam table

class MapRTContext(qtc.QObject):
    api_status_changed = qtc.Signal(str)
    treatment_rooms_updated = qtc.Signal(dict)

    def __init__(self, api_url, token, user_agent):
        super().__init__()

        # network.MapRTAPIManager
        self._api_caller = MapRTAPIManager(api_url, token, user_agent)
        self._api_caller.manager.finished.connect(self._handle_api_replies)

        self._status = None                 # str
        self._couch_buffer = 2.0            # float
        self._patient_buffer = 2.0          # float
        self._patient_surfaces = {}         # surface_label: (surface_id, surface_timestamp, vtk_actor)
        self._current_surface = None        # vtk_actor
        self._treatment_rooms = {}          # room_name: (room_id, room_scale)

    @property
    def api_caller(self):
        return self._api_caller

    @property
    def status(self):
        return self._status

    @property
    def couch_buffer(self):
        return self._couch_buffer

    @property
    def patient_buffer(self):
        return self._patient_buffer

    @property
    def patient_surfaces(self):
        return self._patient_surfaces

    @property
    def current_surface(self):
        return self._current_surface

    @property
    def treatment_rooms(self):
        return self._treatment_rooms

    def _handle_api_replies(self, reply):
        if reply.error() == qtn.QNetworkReply.NetworkError.NoError:
            status_code = reply.attribute(qtn.QNetworkRequest.HttpStatusCodeAttribute)
            print(f'Call to: {reply.request().url().toString()}')
            print(f'HTTP Status Code: {status_code} {responses[status_code]}')
            call_type = reply.request().attribute(qtn.QNetworkRequest.Attribute.User)
            print(f"Call Type Code: {call_type}")

            data = reply.readAll()
            text = str(data, 'utf-8')

            # Process reply based on call type that was executed
            if call_type == MapRTCallType.Ping:
                json_data = json.loads(text)
                print(f"Call Type Name: Ping")
                print("Data received:")
                print(json.dumps(json_data, indent=2))
                self._status = f'HTTP Status Code: {status_code} {responses[status_code]}'
                self.api_status_changed.emit(self._status)

            elif call_type == MapRTCallType.Rooms:
                json_data = json.loads(text)
                print(f"Call Type Name: Rooms")
                print("Data received:")
                print(json.dumps(json_data, indent=2))

                for room in json_data['data']:
                    self._treatment_rooms[room['name']] = (room['id'], room['coordinateSystem'])
                print(self.treatment_rooms)

                self.treatment_rooms_updated.emit(self.treatment_rooms)

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
            call = f'Call to: {reply.request().url().toString()}'
            status = f"Status Code: {status_code}"
            error = f"Error: {reply.errorString()}"
            print(f'{call}\n{status}\n{error}')

        reply.deleteLater()

    @property
    def status(self):
        return self._api_manager.get_status()

class PatientContext(qtc.QObject):
    patient_id_changed = qtc.Signal(str, str) # (old new)
    patient_first_name_changed = qtc.Signal(str, str)  # (old, new)
    patient_last_name_changed = qtc.Signal(str, str)  # (old, new)
    plans_updated = qtc.Signal(dict)
    current_plan_changed = qtc.Signal(PlanContext)

    def __init__(self):
        super().__init__()

        self._patient_id = None         # str
        self._fisrt_name = None         # str
        self._last_name = None          # str
        self._plans = {}                # PlanContext.plan_id: PlanContext
        self._current_plan = None       # PlanContext
        self._maprt = None              # MapRTContext

if __name__ == '__main__':
    import sys
    import time
    import PySide6.QtWidgets as qtw

    app = qtw.QApplication(sys.argv)

    start = time.time()
    ctx = MapRTContext("https://maprtpkr.adventhealth.com:5000",
                       "82212e3b-7edb-40e4-b346-c4fe806a1a0b",
                       "VisionRT.Integration.Saturn/1.2.8"
                       )

    print('Calling Ping')
    ctx.api_caller.get_status()
    print('Calling Rooms')
    ctx.api_caller.get_treatment_rooms()
    print('Calling Room')
    ctx.api_caller.get_treatment_room('TrueBeam')
    print('Calling Surfaces')
    ctx.api_caller.get_patient_surfaces('PHY0019')
    print('Calling Surface')
    ctx.api_caller.get_surface("2e36321f-19de-49cd-899d-c772da051316")
    print('Calling Map')
    ctx.api_caller.get_map()
    print("Elapsed Time:", time.time() - start)

    sys.exit(app.exec())