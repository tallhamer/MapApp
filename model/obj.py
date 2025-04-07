import inspect
import base64
import numpy as np
import trimesh
import open3d as o3d

import vtk
from vtkmodules.util import numpy_support

import PySide6.QtCore as qtc


obj2dcm_transform_map = {None: np.array([[1, 0, 0], # Identity
                                         [0, 1, 0],
                                         [0, 0, 1]
                                         ]
                                        ),
                         'HFS': np.array([[0, 1, 0],
                                          [0, 0, 1],
                                          [1, 0, 0]
                                          ]
                                         ),
                         'HFP': np.array([[0, 1, 0],
                                          [0, 0, -1],
                                          [1, 0, 0]
                                          ]
                                         ),
                         'FFS': np.array([[0, 1, 0],
                                          [0, 0, 1],
                                          [-1, 0, 0]
                                          ]
                                         ),
                         'FFP': np.array([[0, 1, 0],
                                          [0, 0, -1],
                                          [-1, 0, 0]
                                          ]
                                         ),
                         }


class Surface(qtc.QObject):

    file_path_changed = qtc.Signal(str)
    url_changed = qtc.Signal(str)
    vtk_actor_updated = qtc.Signal(qtc.QObject)

    def __init__(self):
        print(inspect.stack()[0][3])
        print(inspect.stack()[1][3])

        super().__init__()

        # self.original_mesh = None
        self._filepath = None
        self._url = None
        self._patient_orientation = None
        self.orientation_coordinates = {}

    @property
    def filepath(self):
        return self._filepath

    @filepath.setter
    def filepath(self, new_path):
        self.update_filepath(new_path)

    @property
    def patient_orientation(self):
        return self._patient_orientation

    @patient_orientation.setter
    def patient_orientation(self, value):
        self._patient_orientation = value
        if hasattr(self, 'obj_actor'):
            self.update_vtk_actor()

    # qtc.Slot(str)
    def update_filepath(self, new_path):
        print(inspect.stack()[0][3])
        print(inspect.stack()[1][3])

        print("In ObjFileModel update_filepath Slot")

        if self._filepath != new_path:
            self.original_mesh = trimesh.load(new_path)

            self._filepath = new_path
            self.file_path_changed.emit(new_path)
            print('file_path_changed signal emitted')

            #  Axes should match the DICOM orientation
            points = self.original_mesh.vertices

            for k, m in obj2dcm_transform_map.items():
                self.orientation_coordinates[k] = (obj2dcm_transform_map[k] @ points.T).T

            # S = obj2dcm_transform_map[self.patient_orientation]

        self.update_vtk_actor()

    def update_from_api(self, api_data):
        print(inspect.stack()[0][3])
        print(inspect.stack()[1][3])

        # Extract the base64 encoded file.
        # Splitting the data on a ',' gets rid of the leading information attached to the base64 encoded file by the
        # MapRT API.
        base64_data = api_data["data"].split(',')[-1]

        # Decode the base64 data
        decoded_data = base64.b64decode(base64_data)

        # # You can now read what was in the obj file sent back from the MapRT API
        # print(decoded_data.decode('utf-8'))
        self.original_mesh = trimesh.load(file_obj=trimesh.util.wrap_as_stream(decoded_data), file_type='obj')

        #  Axes should match the DICOM orientation
        points = self.original_mesh.vertices

        for k, m in obj2dcm_transform_map.items():
            self.orientation_coordinates[k] = (obj2dcm_transform_map[k] @ points.T).T

        self.update_vtk_actor()

    def update_vtk_actor(self):
        print(inspect.stack()[0][3])
        print(inspect.stack()[1][3])

        print("In ObjFileModel update_actor")
        new_points = self.orientation_coordinates[self.patient_orientation]

        obj_pcloud = o3d.geometry.PointCloud()
        obj_pcloud.points = o3d.utility.Vector3dVector(new_points)

        obj_mesh = o3d.geometry.TriangleMesh()
        obj_mesh.vertices = o3d.utility.Vector3dVector(new_points)
        obj_mesh.triangles = o3d.utility.Vector3iVector(self.original_mesh.faces)

        obj_mesh.compute_vertex_normals()
        obj_mesh.compute_triangle_normals()

        self.obj_polydata = vtk.vtkPolyData()
        self.obj_polydata.points = numpy_support.numpy_to_vtk(new_points)


        obj_cells = vtk.vtkCellArray()

        for i in range(len(obj_mesh.triangles)):
            obj_cells.InsertNextCell(3, obj_mesh.triangles[i])
        self.obj_polydata.polys = obj_cells

        # self.obj_mapper = vtk.vtkOpenGLPolyDataMapper()
        self.obj_mapper = vtk.vtkPolyDataMapper()
        self.obj_polydata >> self.obj_mapper

        self.obj_actor = vtk.vtkActor(mapper=self.obj_mapper)

        self.vtk_actor_updated.emit(self)