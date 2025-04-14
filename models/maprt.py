import sys
import json
import base64
from http.client import responses

import numpy as np

import trimesh
import open3d as o3d
import vtk
from vtkmodules.util import numpy_support

import pyqtgraph as pg

import PySide6.QtCore as qtc
import PySide6.QtNetwork as qtn

from _dicom import DicomPlanContext

class MapRTOrientTransform(object):
    def __init__(self):
        super().__init__()
        self._store = {}
        self._store[None] = self._IDENTITY = np.array([[1, 0, 0],
                                                       [0, 1, 0],
                                                       [0, 0, 1]
                                                       ]
                                                      )

        self._store['HFS'] = self._HFS = np.array([[0, 1, 0],
                                                   [0, 0, 1],
                                                   [1, 0, 0]
                                                   ]
                                                  )

        self._store['HFP'] = self._HFP = np.array([[0, 1, 0],
                                                   [0, 0, -1],
                                                   [1, 0, 0]
                                                   ]
                                                  )

        self._store['FFS'] = self._FFS = np.array([[0, 1, 0],
                                                   [0, 0, 1],
                                                   [-1, 0, 0]
                                                   ]
                                                  )

        self._store['FFP'] = self._FFP = np.array([[0, 1, 0],
                                                   [0, 0, -1],
                                                   [-1, 0, 0]
                                                   ]
                                                  )

    def __getitem__(self, item):
        return self._store[item]

    @property
    def HFS(self):
        return self._HFS

    @property
    def HFP(self):
        return self._HFP

    @property
    def FFS(self):
        return self._FFS

    @property
    def FFP(self):
        return self._FFP

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

        self._status = None

        # Endpoints to code
        self._get_beam_delivery_status = f"/integration/GetBeamDeliveryStatus"

    def get_status(self, ctx):
        url = self._api_url + "/integration/ping"
        attributes = f"Ping:{id(ctx)}:"

        request = qtn.QNetworkRequest(qtc.QUrl(url))
        request.setHeaders(self._header)
        request.setSslConfiguration(self.ssl_config)
        request.setAttribute(qtn.QNetworkRequest.Attribute.User, attributes)
        request.setAttribute(qtn.QNetworkRequest.Attribute.CacheLoadControlAttribute,
                             qtn.QNetworkRequest.CacheLoadControl.PreferCache
                             )

        self.manager.get(request)

    def get_treatment_rooms (self, ctx):
        url = self._api_url + "/integration/rooms"
        attributes = f"Rooms:{id(ctx)}:"

        request = qtn.QNetworkRequest(qtc.QUrl(url))
        request.setHeaders(self._header)
        request.setSslConfiguration(self.ssl_config)
        request.setAttribute(qtn.QNetworkRequest.Attribute.User, attributes)
        request.setAttribute(qtn.QNetworkRequest.Attribute.CacheLoadControlAttribute,
                             qtn.QNetworkRequest.CacheLoadControl.PreferCache
                             )

        self.manager.get(request)

    def get_treatment_room(self, ctx, room_name):
        url = self._api_url + f"/integration/rooms/{room_name}"
        attributes = f"Room:{id(ctx)}:{room_name}"

        request = qtn.QNetworkRequest(qtc.QUrl(url))
        request.setHeaders(self._header)
        request.setSslConfiguration(self.ssl_config)
        request.setAttribute(qtn.QNetworkRequest.Attribute.User, attributes)
        request.setAttribute(qtn.QNetworkRequest.Attribute.CacheLoadControlAttribute,
                             qtn.QNetworkRequest.CacheLoadControl.PreferCache
                             )

        self.manager.get(request)

    def get_patient_surfaces(self, ctx, patient_id):
        url = self._api_url + f"/integration/patients/{patient_id}/surfaces"
        attributes = f"Surfaces:{id(ctx)}:{patient_id}"

        request = qtn.QNetworkRequest(qtc.QUrl(url))
        request.setHeaders(self._header)
        request.setSslConfiguration(self.ssl_config)
        request.setAttribute(qtn.QNetworkRequest.Attribute.User, attributes)
        request.setAttribute(qtn.QNetworkRequest.Attribute.CacheLoadControlAttribute,
                             qtn.QNetworkRequest.CacheLoadControl.PreferCache
                             )

        self.manager.get(request)

    def get_surface(self, ctx, surface_id):
        url = self._api_url + f"/integration/surfaces/{surface_id}"
        attributes = f"Surface:{id(ctx)}:{surface_id}"

        request = qtn.QNetworkRequest(qtc.QUrl(url))
        request.setHeaders(self._header)
        request.setSslConfiguration(self.ssl_config)
        request.setAttribute(qtn.QNetworkRequest.Attribute.User, attributes)
        request.setAttribute(qtn.QNetworkRequest.Attribute.CacheLoadControlAttribute,
                             qtn.QNetworkRequest.CacheLoadControl.PreferCache
                             )

        self.manager.get(request)

    def get_map(self, ctx):
        if ctx.plan_context is not None:
            url = self._api_url + f"/integration/GetMap"
            isocenter = ctx.plan_context.isocenter
            couch_buff = ctx.couch_buffer * 10
            patient_buff = ctx.patient_buffer * 10
            surface_id = "2e36321f-19de-49cd-899d-c772da051316" #ctx.current_surface.id
            # room_id, room_scale = ctx.treatment_rooms[ctx.current_room]
            room_id = "eaf6df9d-8e60-c46a-4e6f-ca55e7470545"
            room_scale = "IEC_61217"
            attributes = f"Map:{id(ctx)}:{isocenter};{couch_buff};{patient_buff};{surface_id};{room_id};{room_scale}"

            X, Y, Z = isocenter

            for res in (False, True):
                body = {
                    "CouchBuffer": couch_buff,
                    "PatientBuffer": patient_buff,
                    "HighResolution": res,
                    "PatientSurfaceId": f"{surface_id}",
                    "TreatmentRoomId": f"{room_id}",
                    "Isocenter": {
                        "x": X,
                        "y": Y,
                        "z": Z,
                        "CoordinateSystem": f"{room_scale}",
                    }
                }

                request = qtn.QNetworkRequest(qtc.QUrl(url))
                request.setHeaders(self._header)
                request.setSslConfiguration(self.ssl_config)
                request.setAttribute(qtn.QNetworkRequest.Attribute.User, attributes)
                request.setAttribute(qtn.QNetworkRequest.Attribute.CacheLoadControlAttribute,
                                     qtn.QNetworkRequest.CacheLoadControl.PreferCache
                                     )

                data = json.dumps(body).encode('utf-8')
                self.manager.post(request, qtc.QByteArray(data))
            else:
                print("No Plan context set")

class MapRTSurface(qtc.QObject):
    def __init__(self, data, _id, label, orientation):
        super().__init__()
        self._id = _id
        self._label = label
        self._orientation = orientation
        self._vtk_actor = self._process_data(data)

    @property
    def id(self):
        return self._id

    @property
    def label(self):
        return self._label

    @property
    def orientation(self):
        return self._orientation

    @property
    def vtk_actor(self):
        return self._vtk_actor

    def _process_data(self, data):
        _mesh = trimesh.load(file_obj=trimesh.util.wrap_as_stream(data), file_type='obj')

        transformer = MapRTOrientTransform()
        points = _mesh.vertices
        oriented_points = (transformer[self._orientation] @ points.T).T

        obj_pcloud = o3d.geometry.PointCloud()
        obj_pcloud.points = o3d.utility.Vector3dVector(oriented_points)

        obj_mesh = o3d.geometry.TriangleMesh()
        obj_mesh.vertices = o3d.utility.Vector3dVector(oriented_points)
        obj_mesh.triangles = o3d.utility.Vector3iVector(_mesh.faces)

        obj_mesh.compute_vertex_normals()
        obj_mesh.compute_triangle_normals()

        obj_polydata = vtk.vtkPolyData()
        obj_polydata.points = numpy_support.numpy_to_vtk(oriented_points)

        obj_cells = vtk.vtkCellArray()

        for i in range(len(obj_mesh.triangles)):
            obj_cells.InsertNextCell(3, obj_mesh.triangles[i])
        obj_polydata.polys = obj_cells

        # self.obj_mapper = vtk.vtkOpenGLPolyDataMapper()
        obj_mapper = vtk.vtkPolyDataMapper()
        obj_polydata >> obj_mapper

        return vtk.vtkActor(mapper=obj_mapper)

class MapRTContext(qtc.QObject):
    api_status_changed = qtc.Signal(str)
    treatment_rooms_updated = qtc.Signal(list)
    patient_surfaces_updated = qtc.Signal(list)
    collision_maps_updated = qtc.Signal(dict)
    current_surface_changed = qtc.Signal(vtk.vtkActor)
    current_room_changed = qtc.Signal()
    current_map_data_changed = qtc.Signal(tuple)
    api_connection_error = qtc.Signal(str)

    def __init__(self, api_manager):
        super().__init__()
        self._plan_context = None

        # network.MapRTAPIManager
        self._api_manager = api_manager
        self._api_manager.manager.finished.connect(self._handle_api_results)

        self._api_status = None  # str
        self._couch_buffer = 2.0            # float
        self._patient_buffer = 2.0          # float
        self.__surface_id_map = {}          # surface_id: surface_label
        self._patient_surfaces = {}         # surface_id: vtk_actor
        self._current_surface = None        # vtk_actor
        self._treatment_room_names = {}     # room_name: (room_id, room_scale)
        self._treatment_room_ids = {}       # room_id: (room_name, room_scale)
        self._current_room = None           # str
        self._current_room_id = None        # str
        self._current_room_scale = None     # str
        self._collision_maps = {}           # str: (map_view, x_ticks, y_ticks)
        self._current_map_data = None       # (map_view, x_ticks, y_ticks)

    @property
    def plan_context(self):
        return self._plan_context

    @property
    def api_manager(self):
        return self._api_manager

    @property
    def api_status(self):
        return self._api_status

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
        return self._treatment_room_names

    @property
    def current_room(self):
        return self._current_room

    @property
    def current_map_data(self):
        return self._current_map_data

    def update_plan_context(self, ctx):
        if isinstance(ctx, DicomPlanContext):
            self._plan_context = ctx
        else:
            raise TypeError("'_plan_context' attribute must be set to instance of a PlanContext")

    def update_couch_buffer(self, value):
        self._couch_buffer = value

    def update_patient_buffer(self, value):
        self._couch_buffer = value

    def update_room(self, room_name):
        self._current_room_id, self._current_room_scale = self.treatment_rooms[room_name]
        self.current_room_changed.emit()

    def update_surface(self, surface_label):
        for k, v in self.__surface_id_map.items():
            if v == surface_label:
                self._current_surface = self._patient_surfaces[k]
                self.current_surface_changed.emit(self._current_surface)

    def update_current_map_data(self, map_label):
        self._current_map_data = self._collision_maps[map_label]
        self.current_map_data_changed.emit(self._current_map_data)

    def generate_map_label(self):
        if self._plan_context is not None:
            iso = self.plan_context.isocenter
            couch_buff = self.couch_buffer * 10
            patient_buff = self.patient_buffer * 10
            surface = self.__surface_id_map[self.current_surface.id]
            room_name, room_scale = self._treatment_room_names[self.current_room]
            label = f"{room_name} -- {surface} -- {iso} -- CB: {couch_buff} -- PB: {patient_buff}"
            return label
        else:
            print('No plan context is set')

    def get_collision_map(self):
        label = self.generate_map_label()
        if label in self._collision_maps:
            self._current_map_data = self._collision_maps[label]
            self.current_map_data_changed.emit(self._current_map_data)
        else:
            self.api_manager.get_map(self)

    def _handle_api_results(self, reply):
        if reply.error() == qtn.QNetworkReply.NetworkError.NoError:
            attributes = reply.request().attribute(qtn.QNetworkRequest.Attribute.User)
            call_type, caller_id, args = attributes.split(':')
            status_code = reply.attribute(qtn.QNetworkRequest.Attribute.HttpStatusCodeAttribute)

            mine = caller_id == str(id(self))

            if mine:
                print(f"Mine! {id(self)} ({caller_id})")
            else:
                print(f"Not It! {id(self)} ({caller_id})")

            if mine:
                print(f'\tCall to: {reply.request().url().toString()}')
                print(f'\tHTTP Status Code: {status_code} {responses[status_code]}')
                print(f"\tCall Type Code: {call_type}")


            data = reply.readAll()
            text = str(data, 'utf-8')

            # Process reply based on call type that was executed
            if call_type == 'Ping' and mine:
                json_data = json.loads(text)
                # print('Passed Args: ', *args.split(','))
                # print("Data received:")
                # print(json.dumps(json_data, indent=2))
                self._api_status = f'HTTP Status Code: {status_code} {responses[status_code]}'
                self.api_status_changed.emit(self._api_status)

            elif call_type == 'Rooms' and mine:
                json_data = json.loads(text)
                # print('Passed Args: ', *args.split(','))
                # print("Data received:")
                # print(json.dumps(json_data, indent=2))

                for room in json_data['data']:
                    self._treatment_room_names[room['name']] = (room['id'], room['coordinateSystem'])
                    self._treatment_room_ids[room['id']] = (room['name'], room['coordinateSystem'])

                room_names = [key for key in self._treatment_room_names.keys()]
                self.treatment_rooms_updated.emit(room_names)

            elif call_type == 'Room' and mine:
                json_data = json.loads(text)
                # print('Passed Args: ', *args.split(','))
                # print("Data received:")
                # print(json.dumps(json_data, indent=2))

            elif call_type == 'Surfaces' and mine:
                json_data = json.loads(text)
                # print('Passed Args: ', *args.split(','))
                # print("Data received:")
                # print(json.dumps(json_data, indent=2))
                for surface in json_data['data']:
                    self.__surface_id_map[surface['id']] = surface['label']

                for _id, label in self.__surface_id_map.items():
                    self.api_manager.get_surface(self, _id)

            elif call_type == 'Surface' and mine:
                if self._plan_context is not None:
                    _id, = args.split(',')
                    json_data = json.loads(text)
                    # print('Passed Args: ', *args.split(','))
                    # print("Data received:")
                    # print(json.dumps(json_data, indent=2))

                    base64_data = json_data["data"].split(',')[-1]
                    decoded_data = base64.b64decode(base64_data)
                    self._patient_surfaces[_id] = MapRTSurface(decoded_data,
                                                               _id,
                                                               self.__surface_id_map[_id],
                                                               self._plan_context.patient_orientation
                                                               )

                    if len(self.__surface_id_map.keys()) == len(self._patient_surfaces.keys()):
                        name_list = [key for key in self._patient_surfaces.keys()]
                        self.patient_surfaces_updated.emit(name_list)
                else:
                    print('No plan context is set')

            elif call_type == 'Map' and mine:
                # print('Passed Args: ', *args.split(','))
                # print("Data received:")

                lst = text.split()
                new_str = ','.join(lst[1:-1])
                a = np.fromstring(new_str, dtype=int, sep=',')
                a = a.reshape((int(len(a) / 3), 3))
                couch, gantry, isOK = a.T
                unique_couch = np.unique(couch)
                unique_gantry = np.unique(gantry)

                # print(unique_couch)
                # print(len(unique_couch))
                # print(unique_gantry)
                # print(len(unique_gantry))

                gantry_idx = np.hstack((unique_gantry[np.where(unique_gantry >= 180)],
                                        unique_gantry[np.where(unique_gantry < 180)]
                                        )
                                       )

                couch_idx = np.hstack((unique_couch[np.where(unique_couch >= 180)],
                                       unique_couch[np.where(unique_couch <= 90)]
                                       )
                                      )

                # print(couch_idx)
                # print(len(couch_idx))
                # print(gantry_idx)
                # print(len(gantry_idx))

                x_map = dict([(str(couch_idx[i]), i) for i in range(len(couch_idx))])
                y_map = dict([(str(gantry_idx[i]), i) for i in range(len(gantry_idx))])

                x_labels = [(i, str(couch_idx[i])) for i in np.arange(0, len(couch_idx), 10)]
                x_ticks = [x_labels]
                # bottom_axis = self.plot_widget.getAxis('bottom')
                # bottom_axis.setTicks(x_ticks)

                y_labels = [(j, str(gantry_idx[j])) for j in np.arange(0, len(gantry_idx), 10)]
                y_ticks = [y_labels]
                # left_axis = self.plot_widget.getAxis('left')
                # left_axis.setTicks(y_ticks)

                map_view = pg.ImageItem(axisOrder='row-major')
                map_view.setZValue(0)
                # map_view.setLookupTable(self.map_lut)

                collision_map = np.zeros((len(gantry_idx), len(couch_idx)), dtype=int)
                for j in range(len(couch)):
                    collision_map[y_map[str(gantry[j])], x_map[str(couch[j])]] = isOK[j]

                map_view.setImage(collision_map)

                iso, cb, pb, sid, rid, rs = args.split(';')
                surface_namee = self.__surface_id_map[sid]
                room_name, _ = self._treatment_room_ids[rid]

                map_label = f"{room_name} -- {surface_namee} -- {iso} -- CB: {cb} -- PB: {pb}"
                print(map_label)

                self._collision_maps[map_label] = (map_view, x_ticks, y_ticks)
                map_labels = [key for key in self._collision_maps.keys()]
                self.collision_maps_updated.emit(map_labels)
        else:
            status_code = reply.attribute(qtn.QNetworkRequest.Attribute.HttpStatusCodeAttribute)
            call = f'Call to: {reply.request().url().toString()}'
            status = f"Status Code: {status_code}"
            error = f"Error: {reply.errorString()}"
            msg = f'{call}\n{status}\n{error}'
            self.api_connection_error.emit(msg)

        reply.deleteLater()

if __name__ == '__main__':
    import time
    import PySide6.QtWidgets as qtw

    def handle_error(msg):
        qtw.QMessageBox.information(qtw.QWidget(), "Information", msg, qtw.QMessageBox.Ok)

    class DicomPlanContext(object):
        def __init__(self):
            super().__init__()
            self.isocenter = [0,0,0]
            self.patient_orientation = 'HFS'

    app = qtw.QApplication(sys.argv)

    start = time.time()
    api_manager = MapRTAPIManager("https://maprtpkr.adventhealth.com:5000",
                                  "82212e3b-7edb-40e4-b346-c4fe806a1a0b",
                                  "VisionRT.Integration.Saturn/1.2.8")

    map_ctx1 = MapRTContext(api_manager)
    map_ctx1.update_plan_context(DicomPlanContext())

    map_ctx2 = MapRTContext(api_manager)
    # map_ctx2.update_plan_context(DicomPlanContext())

    map_ctx1.api_connection_error.connect(handle_error)

    print('Calling Ping')
    map_ctx1.api_manager.get_status(map_ctx1)
    print('Calling Rooms')
    map_ctx1.api_manager.get_treatment_rooms(map_ctx1)
    print('Calling Room')
    map_ctx1.api_manager.get_treatment_room(map_ctx1, 'TrueBeam')
    print('Calling Surfaces')
    map_ctx1.api_manager.get_patient_surfaces(map_ctx1, 'PHY0019')
    print('Calling Map')
    map_ctx1.api_manager.get_map(map_ctx1)
    # print('Calling Surface')
    # map_ctx.api_caller.get_surface("2e36321f-19de-49cd-899d-c772da051316")

    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Elapsed Time:", time.time() - start)

    sys.exit(app.exec())