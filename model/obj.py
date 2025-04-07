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


class ObjFileModel(qtc.QObject):

    file_path_changed = qtc.Signal(str)
    vtk_actor_updated = qtc.Signal(qtc.QObject)

    def __init__(self):
        super().__init__()

        self.original_mesh = None
        self._filepath = None
        self._patient_orientation = None
        self.orientation_coordinates = {}
        self.faces = None
        self.file_path_changed.connect(self.test)

    def test(self, text):
        print(text)


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

    def update_vtk_actor(self):
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
        print('signal emitted')