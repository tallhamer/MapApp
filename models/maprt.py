import sys
import json
import uuid
import base64
import datetime as dt
from http.client import responses

import numpy as np

import trimesh
import open3d as o3d
import vtk
from vtkmodules.util import numpy_support

import pyqtgraph as pg

import PySide6.QtCore as qtc
import PySide6.QtNetwork as qtn

from models.dicom import DicomPlanContext

# "https://maprtpkr.adventhealth.com:5000"
# "82212e3b-7edb-40e4-b346-c4fe806a1a0b"
# "VisionRT.Integration.Saturn/1.2.8"

class ObjFileValidationError(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)

class MissingDataError(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)

class MapRTOrientTransform(object):
    def __init__(self):
        print('MapRTOrientTransform.__init__')
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
        print('MapRTOrientTransform.__getitem__')
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
    api_connection_error = qtc.Signal(str)

    def __init__(self, api_url, token, user_agent):
        print('MapRTAPIManager.__init__')
        super().__init__()

        self._api_url = api_url
        self._token = token
        self._user_agent = user_agent

        self.ssl_config = qtn.QSslConfiguration.defaultConfiguration()
        self.ssl_config.setPeerVerifyMode(qtn.QSslSocket.PeerVerifyMode.VerifyNone)
        self.ssl_config.setProtocol(qtn.QSsl.SslProtocol.AnyProtocol)

        self.manager = qtn.QNetworkAccessManager()

        self._status = None

        # Endpoints to code
        self._get_beam_delivery_status = f"/integration/GetBeamDeliveryStatus"

    @property
    def api_url(self):
        return self._api_url

    @api_url.setter
    def api_url(self, value):
        print('MapRTAPIManager.api_url.setter')
        self._api_url = str(value)

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, value):
        print('MapRTAPIManager.token.setter')
        self._token = str(value)

    @property
    def user_agent(self):
        return self._user_agent

    @user_agent.setter
    def user_agent(self, value):
        print('MapRTAPIManager.user_agent.setter')
        self._user_agent= str(value)

    @property
    def header(self):
        header = qtn.QHttpHeaders()
        header.insert(0, "Content-Type", "application/json")
        header.append("Authorization", f"Bearer {self.token}")
        header.append("User-Agent", self.user_agent)
        return header

    def get_status(self):
        print('MapRTAPIManager.get_status')
        url = self.api_url + "/integration/ping"
        attributes = f"Ping:"

        request = qtn.QNetworkRequest(qtc.QUrl(url))
        request.setHeaders(self.header)
        request.setSslConfiguration(self.ssl_config)
        request.setAttribute(qtn.QNetworkRequest.Attribute.User, attributes)
        request.setAttribute(qtn.QNetworkRequest.Attribute.CacheLoadControlAttribute,
                             qtn.QNetworkRequest.CacheLoadControl.PreferCache
                             )

        self.manager.get(request)

    def get_treatment_rooms(self):
        print('MapRTAPIManager.get_treatment_rooms')
        url = self.api_url + "/integration/rooms"
        attributes = f"Rooms:"

        request = qtn.QNetworkRequest(qtc.QUrl(url))
        request.setHeaders(self.header)
        request.setSslConfiguration(self.ssl_config)
        request.setAttribute(qtn.QNetworkRequest.Attribute.User, attributes)
        request.setAttribute(qtn.QNetworkRequest.Attribute.CacheLoadControlAttribute,
                             qtn.QNetworkRequest.CacheLoadControl.PreferCache
                             )

        self.manager.get(request)

    def get_treatment_room(self, room_name):
        print('MapRTAPIManager.get_treatment_room')
        url = self.api_url + f"/integration/rooms/{room_name}"
        attributes = f"Room:{room_name}"

        request = qtn.QNetworkRequest(qtc.QUrl(url))
        request.setHeaders(self.header)
        request.setSslConfiguration(self.ssl_config)
        request.setAttribute(qtn.QNetworkRequest.Attribute.User, attributes)
        request.setAttribute(qtn.QNetworkRequest.Attribute.CacheLoadControlAttribute,
                             qtn.QNetworkRequest.CacheLoadControl.PreferCache
                             )

        self.manager.get(request)

    def get_patient_surfaces(self, patient_id):
        print('MapRTAPIManager.get_patient_surfaces')
        url = self.api_url + f"/integration/patients/{patient_id}/surfaces"
        attributes = f"Surfaces:{patient_id}"

        request = qtn.QNetworkRequest(qtc.QUrl(url))
        request.setHeaders(self.header)
        request.setSslConfiguration(self.ssl_config)
        request.setAttribute(qtn.QNetworkRequest.Attribute.User, attributes)
        request.setAttribute(qtn.QNetworkRequest.Attribute.CacheLoadControlAttribute,
                             qtn.QNetworkRequest.CacheLoadControl.PreferCache
                             )

        self.manager.get(request)

    def get_surface(self, surface_id):
        print('MapRTAPIManager.get_surface')
        url = self.api_url + f"/integration/surfaces/{surface_id}"
        attributes = f"Surface:{surface_id}"

        request = qtn.QNetworkRequest(qtc.QUrl(url))
        request.setHeaders(self.header)
        request.setSslConfiguration(self.ssl_config)
        request.setAttribute(qtn.QNetworkRequest.Attribute.User, attributes)
        request.setAttribute(qtn.QNetworkRequest.Attribute.CacheLoadControlAttribute,
                             qtn.QNetworkRequest.CacheLoadControl.PreferCache
                             )

        self.manager.get(request)

    def get_map(self, ctx, x_shift=0, y_shift=0, z_shift=0):
        print('MapRTAPIManager.get_map')
        if ctx.plan_context is not None:
            # print('\tPlanContext found')
            if ctx.current_surface is not None:
                # print('\tMapRT Surfact found')
                url = self.api_url + f"/integration/GetMap"
                X, Y, Z = ctx.plan_context.isocenter
                X += (-10 * x_shift)    # x-1 to change the direction - x10 to change from cm to mm
                Y += (-10 * y_shift)    # x-1 to change the direction - x10 to change from cm to mm
                Z += (-10 * z_shift)    # x-1 to change the direction - x10 to change from cm to mm
                isocenter = [round(X,2), round(Y,2), round(Z,2)]
                couch_buff = ctx.couch_buffer * 10
                patient_buff = ctx.patient_buffer * 10
                surface_id = ctx.current_surface.id
                room_id, room_scale = ctx.treatment_rooms[ctx.current_room] # Room scale is ignored for now
                attributes = f"Map:{isocenter};{couch_buff};{patient_buff};{surface_id};{room_id};{room_scale}"

                # print(f"\t{isocenter} - {couch_buff} - {patient_buff} - {surface_id} - {ctx.current_room} - {room_id} - {room_scale}")
                # for k,v in ctx.treatment_rooms.items():
                #     print(f'\t{k},{v}')

                X, Y, Z = isocenter

                X += (-1 * x_shift)
                Y += (-1 * y_shift)
                Z += (-1 * z_shift)

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
                            "CoordinateSystem": "IEC_61217",
                        }
                    }

                    request = qtn.QNetworkRequest(qtc.QUrl(url))
                    request.setHeaders(self.header)
                    request.setSslConfiguration(self.ssl_config)
                    request.setAttribute(qtn.QNetworkRequest.Attribute.User, attributes)
                    request.setAttribute(qtn.QNetworkRequest.Attribute.CacheLoadControlAttribute,
                                         qtn.QNetworkRequest.CacheLoadControl.PreferCache
                                         )

                    data = json.dumps(body).encode('utf-8')
                    # print('\tCall Body:')
                    # print(f'\t{json.dumps(body, indent=2)}')
                    # print(data)
                    self.manager.post(request, data)
            else:
                print("No MapRTSurface provided")
        else:
            print("No PlanContext provided")

class MapRTSurface(qtc.QObject):
    def __init__(self, data, _id, label, orientation):
        print('MapRTSurface.__init__')
        super().__init__()
        self._id = _id
        self._label = label
        self._orientation = orientation
        self._vtk_polydata = self._process_data(data)

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
    def vtk_polydata(self):
        return self._vtk_polydata

    def _process_data(self, data):
        print('MapRTSurface._process_data')
        _mesh = trimesh.load(file_obj=trimesh.util.wrap_as_stream(data), file_type='obj')

        transformer = MapRTOrientTransform()
        points = _mesh.vertices
        oriented_points = (transformer[self._orientation] @ points.T).T

        pcloud = o3d.geometry.PointCloud()
        pcloud.points = o3d.utility.Vector3dVector(oriented_points)

        mesh = o3d.geometry.TriangleMesh()
        mesh.vertices = o3d.utility.Vector3dVector(oriented_points)
        mesh.triangles = o3d.utility.Vector3iVector(_mesh.faces)

        mesh.compute_vertex_normals()
        mesh.compute_triangle_normals()

        polydata = vtk.vtkPolyData()
        polydata.points = numpy_support.numpy_to_vtk(oriented_points)

        cells = vtk.vtkCellArray()

        for i in range(len(mesh.triangles)):
            cells.InsertNextCell(3, mesh.triangles[i])
        polydata.polys = cells

        return polydata

class MapRTContext(qtc.QObject):
    api_status_changed = qtc.Signal(str)
    api_connection_error = qtc.Signal(str)
    treatment_rooms_updated = qtc.Signal(list)
    patient_surfaces_updated = qtc.Signal(list)
    collision_maps_updated = qtc.Signal(list)
    current_surface_changed = qtc.Signal(vtk.vtkActor)
    current_room_changed = qtc.Signal()
    current_map_data_changed = qtc.Signal(tuple)
    plan_context_changed = qtc.Signal(bool)

    def __init__(self, api_manager):
        print('MapRTContext.__init__')
        super().__init__()
        self._plan_context = None

        # network.MapRTAPIManager
        self._api_manager = api_manager
        self._api_manager.manager.finished.connect(self._handle_api_results)

        self._api_status = None             # str
        self._couch_buffer = 2.0            # float
        self._patient_buffer = 2.0          # float
        self.__surface_id_map = {}          # surface_id: surface_label
        self._patient_surfaces = {}         # surface_id: vtk_polydata
        self._current_surface = None        # vtk_polydata
        self._treatment_room_names = {}     # room_name: (room_id, room_scale)
        self._treatment_room_ids = {}       # room_id: (room_name, room_scale)
        self._current_room_label = None           # str
        self._current_room_id = None        # str
        self._current_room_scale = None     # str
        self._collision_maps = {}           # str: (map_view, x_ticks, y_ticks)
        self._current_map_label = ''        # str
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
        return self._current_room_label

    @property
    def current_map_label(self):
        return self._current_map_label

    @property
    def current_map_data(self):
        return self._current_map_data

    def clear(self):
        print('MapRTContext.clear')
        self._plan_context = None

        self._api_status = None  # str
        self.api_status_changed.emit('')
        self._couch_buffer = 2.0  # float
        self._patient_buffer = 2.0  # float
        self.__surface_id_map = {}  # surface_id: surface_label
        self._patient_surfaces = {}  # surface_id: vtk_polydata
        self._current_surface = None  # vtk_polydata
        self.patient_surfaces_updated.emit([])
        self._treatment_room_names = {}  # room_name: (room_id, room_scale)
        self._treatment_room_ids = {}  # room_id: (room_name, room_scale)
        self._current_room_label = None  # str
        self._current_room_id = None  # str
        self._current_room_scale = None  # str
        self.treatment_rooms_updated.emit([])
        self._collision_maps = {}  # str: (map_view, x_ticks, y_ticks)
        self._current_map_label = ''  # str
        self._current_map_data = None  # (map_view, x_ticks, y_ticks)
        self.collision_maps_updated.emit([])

    def update_plan_context(self, ctx):
        print('MapRTContext.update_plan_context')
        if isinstance(ctx, DicomPlanContext):
            self._plan_context = ctx
        else:
            raise TypeError("'_plan_context' attribute must be set to instance of a PlanContext")

    def update_couch_buffer(self, value):
        print('MapRTContext.update_couch_buffer')
        self._couch_buffer = value

    def update_patient_buffer(self, value):
        print('MapRTContext.update_patient_buffer')
        self._patient_buffer = value

    def update_room(self, room_label):
        print('MapRTContext.update_room')
        if room_label in self._treatment_room_names: # needed for clearing
            self._current_room_label = room_label
            self._current_room_id, self._current_room_scale = self.treatment_rooms[room_label]
            self.current_room_changed.emit()

    def update_surface(self, surface_label):
        print('MapRTContext.update_surface')
        for k, v in self.__surface_id_map.items():
            if v == surface_label:
                self._current_surface = self._patient_surfaces[k]
                self.current_surface_changed.emit(self._current_surface)

    def update_current_map_data(self, map_label):
        print('MapRTContext.update_current_map_data')
        if map_label in self._collision_maps:
            self._current_map_label = map_label
            self._current_map_data = self._collision_maps[map_label]
            self.current_map_data_changed.emit(self._current_map_data)

    def load_surface_file(self, file_path, orientation):
        print('MapRTContext.load_surface_file')
        try:
            mesh = trimesh.load(file_path)
            _id = uuid.uuid4().hex
            label = dt.datetime.strftime(dt.datetime.now(), '%Y%m%d %H%M%S') + " <- File"
            self.__surface_id_map[_id] = label
            obj = open(file_path, 'rb')
            self._patient_surfaces[_id] = MapRTSurface(obj.read(),
                                                       _id,
                                                       self.__surface_id_map[_id],
                                                       orientation
                                                       )
            name_list = [value for key, value in self.__surface_id_map.items()]
            self.patient_surfaces_updated.emit(name_list)
            self.update_surface(label)
        except Exception as e:
            raise ObjFileValidationError(e)

    def generate_map_label(self):
        print('MapRTContext.generate_map_label')
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
            raise MissingDataError("Missing PlanContext is required for Isocenter location.")

    def get_collision_map(self):
        print('MapRTContext.get_collision_map')
        label = self.generate_map_label()
        if label in self._collision_maps:
            self._current_map_data = self._collision_maps[label]
            self.current_map_data_changed.emit(self._current_map_data)
        else:
            if self._plan_context is not None:
                self.api_manager.get_map(self)
            else:
                raise MissingDataError("Missing PlanContext is required for Isocenter location.")

    def _handle_api_results(self, reply):
        print('MapRTContext._handle_api_results')
        if reply.error() == qtn.QNetworkReply.NetworkError.NoError:
            attributes = reply.request().attribute(qtn.QNetworkRequest.Attribute.User)
            call_type, args = attributes.split(':')
            status_code = reply.attribute(qtn.QNetworkRequest.Attribute.HttpStatusCodeAttribute)


            data = reply.readAll()
            text = str(data, 'utf-8')

            # Process reply based on call type that was executed
            if call_type == 'Ping':
                print('MapRTContext._handle_api_results.Ping')
                self._api_status = f'HTTP Status Code: {status_code} {responses[status_code]}'
                self.api_status_changed.emit(self._api_status)

            elif call_type == 'Rooms':
                print('MapRTContext._handle_api_results.Rooms')
                json_data = json.loads(text)

                for room in json_data['data']:
                    self._treatment_room_names[room['name']] = (room['id'], room['coordinateSystem'])
                    self._treatment_room_ids[room['id']] = (room['name'], room['coordinateSystem'])

                room_names = [key for key in self._treatment_room_names.keys()]
                self.treatment_rooms_updated.emit(room_names)

            elif call_type == 'Room':
                print('MapRTContext._handle_api_results.Room')
                json_data = json.loads(text)

            elif call_type == 'Surfaces':
                print('MapRTContext._handle_api_results.Surfaces')
                json_data = json.loads(text)

                for surface in json_data['data']:
                    self.__surface_id_map[surface['id']] = surface['label']

                for _id, label in self.__surface_id_map.items():
                    self.api_manager.get_surface(_id)

            elif call_type == 'Surface':
                print('MapRTContext._handle_api_results.Surface')
                if self._plan_context is not None:
                    _id, = args.split(',')
                    json_data = json.loads(text)

                    base64_data = json_data["data"].split(',')[-1]
                    decoded_data = base64.b64decode(base64_data)
                    self._patient_surfaces[_id] = MapRTSurface(decoded_data,
                                                               _id,
                                                               self.__surface_id_map[_id],
                                                               self._plan_context.patient_orientation
                                                               )

                    if len(self.__surface_id_map.keys()) == len(self._patient_surfaces.keys()):
                        name_list = [value for key, value in self.__surface_id_map.items()]
                        self.patient_surfaces_updated.emit(name_list)
                else:
                    print('No plan context is set')
                    raise MissingDataError("Missing PlanContext is required for patient orientation.")


            elif call_type == 'Map':
                print('MapRTContext._handle_api_results.Map')

                lst = text.split()

                # Determine the sampling for the gantry and couch axes
                couch_samples, gantry_samples = lst[0].split(',')
                gantry_step_size = 360 / int(gantry_samples)
                couch_step_size = 180 / (int(couch_samples) - 1)

                # Construct csv string and read into array using numpy
                new_str = ','.join(lst[1:-1])
                a = np.fromstring(new_str, dtype=int, sep=',')
                a = a.reshape((int(len(a) / 3), 3))

                # Grab the couch and gantry position arrays along with the safe flag
                couch, gantry, isOK = a.T

                # Construct a unique set of gantry and couch positions used to construct the 2D image
                unique_couch = np.unique(couch)
                unique_gantry = np.unique(gantry)

                # Order them to match the MapRT collision map display settings
                gantry_idx = np.hstack((unique_gantry[np.where(unique_gantry >= 180)],
                                        unique_gantry[np.where(unique_gantry < 180)]
                                        )
                                       )

                couch_idx = np.hstack((unique_couch[np.where(unique_couch >= 180)],
                                       unique_couch[np.where(unique_couch <= 90)]
                                       )
                                      )

                # Construct mappings from gantry and couch readouts to array index positions
                x_map = dict([(str(couch_idx[i]), i) for i in range(len(couch_idx))])
                y_map = dict([(str(gantry_idx[i]), i) for i in range(len(gantry_idx))])

                # Construct the initial 2D collision map image and assign the values to each pixel
                _collision_map = np.zeros((len(gantry_idx), len(couch_idx)), dtype=int)
                for j in range(len(couch)):
                    _collision_map[y_map[str(gantry[j])], x_map[str(couch[j])]] = isOK[j]

                collision_map = None

                # If the gantry and couch are low resolution upsample to get consistent indices
                if not gantry_step_size == 1 or not couch_step_size == 1:
                    collision_map = np.repeat(np.repeat(_collision_map,
                                                        int(gantry_step_size),
                                                        axis=0
                                                        ),
                                              int(couch_step_size),
                                              axis=1
                                              )
                else:
                    collision_map = _collision_map

                # construct couch index positions for resampled map
                c0 = np.arange(270, 360, 1)
                c1 = np.arange(0, 91, 1)
                couch_values = np.hstack((c0, c1))

                # construct gantry index positions for resampled map
                g0 = np.arange(180, 360, 1)
                g1 = np.arange(0, 180, 1)
                gantry_values = np.hstack((g0, g1))

                # construct the mappings for the tick labels for the couch and gantry axes
                x_labels = [(int(x), str(couch_values[x])) for x in np.arange(0, len(couch_values), 10)]
                x_ticks = [x_labels]

                y_labels = [(int(y), str(gantry_values[y])) for y in np.arange(0, len(gantry_values), 10)]
                y_ticks = [y_labels]

                map_view = pg.ImageItem(axisOrder='row-major')
                map_view.setZValue(0)
                map_view.setImage(collision_map)

                iso, cb, pb, sid, rid, rs = args.split(';')
                surface_namee = self.__surface_id_map[sid]
                room_name, _ = self._treatment_room_ids[rid]

                map_label = f"{room_name} -- {surface_namee} -- {iso} -- CB: {cb} -- PB: {pb}"

                self._collision_maps[map_label] = (map_view, x_ticks, y_ticks)
                map_labels = [key for key in self._collision_maps.keys()]
                self.collision_maps_updated.emit(map_labels)
                self.update_current_map_data(map_label)
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

    # map_ctx2 = MapRTContext(api_manager)
    # map_ctx2.update_plan_context(DicomPlanContext())
    # map_ctx2.load_surface_file(r"C:\__python__\Projects\MapApp\data\matched_mergedSurface.obj", "HFS")

    map_ctx1.api_connection_error.connect(handle_error)

    print('Calling Ping')
    map_ctx1.api_manager.get_status()
    print('Calling Rooms')
    map_ctx1.api_manager.get_treatment_rooms()
    print('Calling Room')
    map_ctx1.api_manager.get_treatment_room('TrueBeam')
    print('Calling Surfaces')
    map_ctx1.api_manager.get_patient_surfaces('PHY0019')
    print('Calling Map')
    map_ctx1.api_manager.get_map(map_ctx1)
    # print('Calling Surface')
    # map_ctx.api_caller.get_surface("2e36321f-19de-49cd-899d-c772da051316")

    # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Surface: ", map_ctx2.current_surface.id, map_ctx2.current_surface.label)

    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Elapsed Time:", time.time() - start)

    sys.exit(app.exec())