import json
import PySide6.QtCore as qtc
import PySide6.QtNetwork as qtn

from maprt import MapRTContext

class PlanContext(qtc.QObject):
    def __init__(self):
        super().__init__()

        self._isocenter = None              # list
        self._patient_orientation = None    # str
        self._structures = {}               # structure name: vtk_actor
        self._current_structure = None      # vtk_actor
        self._beams = []                    # list of lists for beam table
        self._maprt_context = None          # MapRTContext

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
    ctx.api_manager.get_status()
    print('Calling Rooms')
    ctx.api_manager.get_treatment_rooms()
    print('Calling Room')
    ctx.api_manager.get_treatment_room('TrueBeam')
    print('Calling Surfaces')
    ctx.api_manager.get_patient_surfaces('PHY0019')
    print('Calling Surface')
    ctx.api_manager.get_surface("2e36321f-19de-49cd-899d-c772da051316")
    print('Calling Map')
    ctx.api_manager.get_map()
    print("Elapsed Time:", time.time() - start)

    sys.exit(app.exec())