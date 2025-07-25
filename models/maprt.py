import sys
import json
import uuid
import binascii
import base64
import logging
import datetime as dt
from http.client import responses

import numpy as np

import vtk
from vtkmodules.util.numpy_support import vtk_to_numpy, numpy_to_vtk

import PySide6.QtCore as qtc
import PySide6.QtNetwork as qtn
import pyqtgraph as pg

from models.dicom import DicomPlanContext
from models.settings import app_settings


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
        self.logger = logging.getLogger('MapApp.models.maprt.MapRTOrientTransform')
        self.logger.debug(f'Initializing attributes for MapRTOrientTransform object')
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
        self.logger.debug(f'Returning transform for {item} from MapRTOrientTransform object')
        return self._store[item]

    @property
    def HFS(self):
        self.logger.debug(f'Returning HFS transform from MapRTOrientTransform object')
        return self._HFS

    @property
    def HFP(self):
        self.logger.debug(f'Returning HFP transform from MapRTOrientTransform object')
        return self._HFP

    @property
    def FFS(self):
        self.logger.debug(f'Returning FFS transform from MapRTOrientTransform object')
        return self._FFS

    @property
    def FFP(self):
        self.logger.debug(f'Returning FFP transform from MapRTOrientTransform object')
        return self._FFP

class MapRTAPIManager(qtc.QObject):
    status_returned = qtc.Signal(str)
    api_connection_error = qtc.Signal(str)
    status_bar_coms = qtc.Signal(str)
    status_bar_clear = qtc.Signal()
    progress_coms = qtc.Signal(int)

    def __init__(self, api_url=None, token=None, user_agent=None):
        self.logger = logging.getLogger('MapApp.models.maprt.MapRTAPIManager')
        self.logger.debug(f'Initializing attributes for MapRTAPIManager object')
        super().__init__()

        if api_url is None:
            self._api_url = app_settings.maprt.api_url
        else:
            self._api_url = api_url

        if token is None:
            token = binascii.unhexlify(base64.b64decode(app_settings.maprt.api_token.encode('utf-8'))).decode('utf-8')
            self._token = token
        else:
            self._token = token

        if user_agent is None:
            self._user_agent = app_settings.maprt.api_user_agent
        else:
            self._user_agent = user_agent

        self.logger.debug(f'Setting SSL Configuration for MapRTAPIManager')
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
        self.logger.debug(f'Setting api_url to {value} in MapRTAPIManager')
        self._api_url = str(value)

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, value):
        self.logger.debug(f'Setting token to {value} in MapRTAPIManager')
        self._token = str(value)

    @property
    def user_agent(self):
        return self._user_agent

    @user_agent.setter
    def user_agent(self, value):
        self.logger.debug(f'Setting user_agent to {value} in MapRTAPIManager')
        self._user_agent= str(value)

    @property
    def header(self):
        header = qtn.QHttpHeaders()
        header.insert(0, "Content-Type", "application/json")
        header.append("Authorization", f"Bearer {self.token}")
        header.append("User-Agent", self.user_agent)
        return header

    def get_status(self):
        url = self.api_url + "/integration/ping"
        self.logger.debug(f'Ping call made to "{url}" API endpoint in MapRTAPIManager')
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
        url = self.api_url + "/integration/rooms"
        self.logger.debug(f'Get Rooms call made to "{url}" API endpoint in MapRTAPIManager')
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
        url = self.api_url + f"/integration/rooms/{room_name}"
        self.logger.debug(f'Get Room call made to "{url}" API endpoint in MapRTAPIManager')
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
        url = self.api_url + f"/integration/patients/{patient_id}/surfaces"
        self.logger.debug(f'Get Surfaces call made to "{url}" API endpoint in MapRTAPIManager')
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
        url = self.api_url + f"/integration/surfaces/{surface_id}"
        self.logger.debug(f'Get Surfaces call made to "{url}" API endpoint in MapRTAPIManager')
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
        if ctx.plan_context is not None:
            # print('\tPlanContext found')
            if ctx.current_surface is not None:
                # print('\tMapRT Surfact found')
                url = self.api_url + f"/integration/GetMap"
                self.logger.debug(f'Get Map call made to "{url}" API endpoint in MapRTAPIManager')

                # Perform Isocenter manipulation for any correction applied in the interface
                X, Y, Z = ctx.plan_context.isocenter

                x_shift *= -10 # Multiply by -10 to change direction (surface shift) and to convert cm to mm
                y_shift *= -10 # Multiply by -10 to change direction (surface shift) and to convert cm to mm
                z_shift *= -10 # Multiply by -10 to change direction (surface shift) and to convert cm to mm

                X += x_shift # Shifted Isocenter X
                Y += y_shift # Shifted Isocenter Y
                Z += z_shift # Shifted Isocenter Z

                isocenter = [round(X,2), round(Y,2), round(Z,2)]
                couch_buff = ctx.couch_buffer * 10
                patient_buff = ctx.patient_buffer * 10
                surface_id = ctx.current_surface.id
                room_id, room_scale = ctx.treatment_rooms[ctx.current_room] # Room scale is ignored for now
                attributes = f"Map:{isocenter};{couch_buff};{patient_buff};{surface_id};{room_id};{room_scale}"

                self.logger.debug(f'Isocenter being explored: {ctx.plan_context.isocenter}')
                self.logger.debug(f'Isocenter shifts')
                self.logger.debug(f'\t"X Shift": {x_shift}')
                self.logger.debug(f'\t"Y Shift": {y_shift}')
                self.logger.debug(f'\t"Z Shift": {z_shift}')

                for res in (False, True):
                    body = {
                        "CouchBuffer": couch_buff,
                        "PatientBuffer": patient_buff,
                        "HighResolution": res,
                        "PatientPosition": ctx.plan_context.patient_orientation,
                        "PatientSurfaceId": f"{surface_id}",
                        "TreatmentRoomId": f"{room_id}",
                        "Isocenter": {
                            "x": X,
                            "y": Y,
                            "z": Z,
                            "CoordinateSystem": "IEC_61217",
                        }
                    }

                    self.logger.debug(f'Get Map call parameters:')
                    self.logger.debug(f'\t"CouchBuffer": {couch_buff}')
                    self.logger.debug(f'\t"PatientBuffer": {patient_buff}')
                    self.logger.debug(f'\t"HighResolution": {res}')
                    self.logger.debug(f'\t"PatientPosition": {ctx.plan_context.patient_orientation}')
                    self.logger.debug(f'\t"PatientSurfaceId": {surface_id}')
                    self.logger.debug(f'\t"TreatmentRoomId": {room_id}')
                    self.logger.debug(f'\t"Isocenter"')
                    self.logger.debug(f'\t\t"X": {X}')
                    self.logger.debug(f'\t\t"Y": {Y}')
                    self.logger.debug(f'\t\t"Z": {Z}')

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
                self.logger.debug("No MapRTSurface provided")
        else:
            self.logger.debug("No PlanContext provided")

class MapRTSurface(qtc.QObject):
    def __init__(self, data, _id, label, orientation):
        self.logger = logging.getLogger('MapApp.models.maprt.MapRTSurface')
        self.logger.debug(f'Initializing attributes for MapRTSurface object')
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
        self.logger.debug(f'Process surface data stream returned from MapRT API in MapRTSurface object')

        # Setup a MemoryResourceStream to hold the decoded data from the api payload
        obj_stream = vtk.vtkMemoryResourceStream()

        # Set the buffer for the stream to the decoded data from the api payload
        obj_stream.SetBuffer(data, len(data))

        # Create an OBJ reader
        reader = vtk.vtkOBJReader()

        # Set the stream as the input for the reader
        reader.SetStream(obj_stream)

        # Update the reader to process the data
        reader.Update()
        polydata = reader.GetOutput()

        # Grab the vertices in the obj file stream
        points = vtk_to_numpy(polydata.GetPoints().GetData())

        # Make sure the cells are triangles
        cell_type = vtk.VTK_TRIANGLE

        # Iterate through the cells and determine their types
        for i in range(polydata.GetNumberOfCells()):
            if polydata.GetCellType(i) != vtk.VTK_TRIANGLE:
                raise Exception("Cell types not a triangle")

        # Store the cells
        cells = polydata.GetPolys()

        # Transform the obj coordinates in the proper DICOM orientation
        transformer = MapRTOrientTransform()
        oriented_points = (transformer[self._orientation] @ points.T).T

        # Construct a new VTK PolyData using the transformed vertices and the cells from the original .obj
        oriented_polydata = vtk.vtkPolyData()
        oriented_polydata.points = numpy_to_vtk(oriented_points)
        oriented_polydata.polys = cells

        return oriented_polydata

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
    status_bar_coms = qtc.Signal(str)
    status_bar_clear = qtc.Signal()
    progress_coms = qtc.Signal(int)

    def __init__(self, api_manager):
        self.logger = logging.getLogger('MapApp.models.maprt.MapRTContext')
        self.logger.debug(f'Initializing attributes for MapRTContext object')
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
        self.logger.debug(f'Clearing attribute values for MapRTContext object')
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
        self.logger.debug(f'Updating the plan_context value in MapRTContext')
        if isinstance(ctx, DicomPlanContext):
            self._plan_context = ctx
        else:
            raise TypeError("'_plan_context' attribute must be set to instance of a PlanContext")

    def update_couch_buffer(self, value):
        self.logger.debug(f'Updating the couch_buffer value to {value} in MapRTContext')
        self._couch_buffer = value

    def update_patient_buffer(self, value):
        self.logger.debug(f'Updating the patient_buffer value to {value} in MapRTContext')
        self._patient_buffer = value

    def update_room(self, room_label):
        self.logger.debug(f'Updating the current_room to {room_label} in MapRTContext')
        if room_label in self._treatment_room_names: # needed for clearing
            self._current_room_label = room_label
            self._current_room_id, self._current_room_scale = self.treatment_rooms[room_label]
            self.current_room_changed.emit()

    def update_surface(self, surface_label):
        self.logger.debug(f'Updating the current_surface to {surface_label} in MapRTContext')
        for k, v in self.__surface_id_map.items():
            if v == surface_label:
                self._current_surface = self._patient_surfaces[k]
                self.current_surface_changed.emit(self._current_surface)

    def update_current_map_data(self, map_label):
        self.logger.debug(f'Updating the current collision map data to {map_label} in MapRTContext')
        if map_label in self._collision_maps:
            self._current_map_label = map_label
            self._current_map_data = self._collision_maps[map_label]
            self.current_map_data_changed.emit(self._current_map_data)

    def load_surface_file(self, file_path, orientation):
        self.logger.debug(f'Loading surface from file in MapRTContext')
        try:
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
            # self.update_surface(label)
        except Exception as e:
            raise ObjFileValidationError(e)

    def generate_map_label(self):
        self.logger.debug(f'Generating collision map label from setting used during creation in MapRTContext')
        if self._plan_context is not None:
            iso = self.plan_context.isocenter
            couch_buff = self.couch_buffer * 10
            patient_buff = self.patient_buffer * 10
            surface = self.__surface_id_map[self.current_surface.id]
            room_name, room_scale = self._treatment_room_names[self.current_room]
            label = f"{room_name} -- {surface} -- {iso} -- CB: {couch_buff} -- PB: {patient_buff}"
            return label
        else:
            self.logger.error("Missing PlanContext is required for Isocenter location.")
            raise MissingDataError("Missing PlanContext is required for Isocenter location.")

    def get_collision_map(self):
        self.logger.debug(f'Call MapRT API for collision map in MapRTContext')

        label = self.generate_map_label()
        self.logger.info(f'Looking for cached collision map with current context settings in MapRTContext')
        if label in self._collision_maps:
            self.logger.info(f'Cached collision map found in MapRTContext')
            self._current_map_data = self._collision_maps[label]
            self.current_map_data_changed.emit(self._current_map_data)
        else:
            if self._plan_context is not None:
                self.logger.info(f'No cached collision map found calling API for new collision map in MapRTContext')
                self.api_manager.get_map(self)
            else:
                self.logger.error("Missing PlanContext is required for Isocenter location.")
                raise MissingDataError("Missing PlanContext is required for Isocenter location.")

    def _handle_api_results(self, reply):
        self.logger.debug(f'Handling incoming API call results in MapRTContext')
        if reply.error() == qtn.QNetworkReply.NetworkError.NoError:
            attributes = reply.request().attribute(qtn.QNetworkRequest.Attribute.User)
            call_type, args = attributes.split(':')
            status_code = reply.attribute(qtn.QNetworkRequest.Attribute.HttpStatusCodeAttribute)


            data = reply.readAll()
            text = str(data, 'utf-8')

            # Process reply based on call type that was executed
            if call_type == 'Ping':
                self.logger.debug(f'Handling incoming "Ping" results in MapRTContext')
                self._api_status = f'HTTP Status Code: {status_code} {responses[status_code]}'
                self.api_status_changed.emit(self._api_status)

            elif call_type == 'Rooms':
                self.logger.debug(f'Handling incoming "Rooms" results in MapRTContext')
                json_data = json.loads(text)

                for room in json_data['data']:
                    self._treatment_room_names[room['name']] = (room['id'], room['coordinateSystem'])
                    self._treatment_room_ids[room['id']] = (room['name'], room['coordinateSystem'])

                room_names = [key for key in self._treatment_room_names.keys()]
                self.treatment_rooms_updated.emit(room_names)

            elif call_type == 'Room':
                self.logger.debug(f'Handling incoming "Room" results in MapRTContext')
                json_data = json.loads(text)

            elif call_type == 'Surfaces':
                self.logger.debug(f'Handling incoming "Surfaces" results in MapRTContext')
                json_data = json.loads(text)

                for surface in json_data['data']:
                    # self.__surface_id_map[surface['id']] = surface['label']
                    self.__surface_id_map[surface['id']] = surface['timeStamp']

                for _id, label in self.__surface_id_map.items():
                    self.api_manager.get_surface(_id)

            elif call_type == 'Surface':
                self.logger.debug(f'Handling incoming "Surface" results in MapRTContext')
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
                    self.logger.error("Missing PlanContext is required for patient orientation.")
                    raise MissingDataError("Missing PlanContext is required for patient orientation.")


            elif call_type == 'Map':
                self.logger.debug(f'Handling incoming "Map" results in MapRTContext')

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
            # Looged in main application
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