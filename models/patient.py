import json
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
        self._maprt = None                  # MapRTContext

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