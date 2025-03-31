import sys

import PySide6.QtCore as qtc
import PySide6.QtWidgets as qtw
# import PySide6.QtGui as qtg

import pydicom
import numpy as np
from skimage import measure
from scipy.spatial import cKDTree

import trimesh
import open3d as o3d

import vtk
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from ui.test_window import Ui_MainWindow
from model.dicom import DicomFileSyncModel

DFS = DicomFileSyncModel()

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

def has_actor(renderer, actor_to_check):
    """
    Checks if a vtkRenderer contains a specific actor.

    Args:
        renderer: The vtkRenderer.
        actor_to_check: The actor to check for.

    Returns:
        True if the renderer contains the actor, False otherwise.
    """
    actors = renderer.GetActors()
    actors.InitTraversal()
    current_actor = actors.GetNextActor()
    while current_actor is not None:
        if current_actor == actor_to_check:
            return True
        current_actor = actors.GetNextActor()
    return False

# Define helper functions
# def get_dcm_body_point_cloud(dcm_filename):
#     # Read DICOM Structure Set
#     ds = pydicom.dcmread(dcm_filename)
#
#     # Generate ROI Look Up Table using the ROI Number as the key
#     roi_lut = {}
#     for structure in ds.StructureSetROISequence:
#         # print(f'{structure.ROIName} ({structure.ROIName.lower()})',
#         #       structure.ROINumber
#         #       )
#         roi_lut[structure.ROINumber] = structure.ROIName.lower()
#
#     # Grab the Body structure points
#     body_contours = []
#     for roi in ds.ROIContourSequence:
#         if (roi.ReferencedROINumber in roi_lut) and \
#                 roi_lut[roi.ReferencedROINumber] == 'body':
#             # print('Found Body')
#             for contour in roi.ContourSequence:
#                 # print(contour.ContourData)
#                 body_contours.append([[float(contour.ContourData[i]),
#                                        float(contour.ContourData[i + 1]),
#                                        float(contour.ContourData[i + 2])
#                                        ] \
#                                       for i in range(0,
#                                                      len(contour.ContourData),
#                                                      3
#                                                      )
#                                       ]
#                                      )
#
#     dcm_points = np.array([point for contour in body_contours \
#                            for point in contour
#                            ]
#                           )
#
#     dcm_colors = np.zeros(dcm_points.shape)
#     dcm_colors[:, :] = [0.0, 0.5, 0.0]
#
#     dcm_pcloud = o3d.geometry.PointCloud()
#     dcm_pcloud.points = o3d.utility.Vector3dVector(dcm_points)
#     dcm_pcloud.colors = o3d.utility.Vector3dVector(dcm_colors)
#     dcm_pcloud.estimate_normals()
#
#     return dcm_pcloud
#
# def pcloud_to_mesh(pcd, voxel_size=3, iso_level_percentile=5):
#     # Convet Open3D point cloud to numpy array
#     points = np.asarray(pcd.points)
#
#     # Compute the bounds of the point cloud
#     mins = pcd.get_min_bound()
#     maxs = pcd.get_max_bound()
#
#     # print(mins)
#     # print(maxs)
#
#     x = np.arange(mins[0], maxs[0], voxel_size)
#     y = np.arange(mins[1], maxs[1], voxel_size)
#     z = np.arange(mins[2], maxs[2], voxel_size)
#     x, y, z = np.meshgrid(x, y, z, indexing='ij')
#
#     # Create a KD-tree for efficient nearest neighbor search
#     tree = cKDTree(points)
#
#     # Compute the scalar field (distance to nearest point)
#     grid_points = np.vstack([x.ravel(), y.ravel(), z.ravel()]).T
#     print(f'Using {len(x.ravel())} grid_points for marching cubes')
#     distances, _ = tree.query(grid_points, workers=-1)
#     scalar_field = distances.reshape(x.shape)
#
#     # Determine the iso_level based on the percentile of distance
#     iso_level = np.percentile(distances, iso_level_percentile)
#
#     # Apply Marching Cubes
#     verts, faces, _, _ = measure.marching_cubes(scalar_field, level=iso_level)
#
#     # Scale and translate vertices back to original coordinate system
#     verts = verts * voxel_size + mins
#
#     # Create the mesh
#     mesh = o3d.geometry.TriangleMesh()
#     mesh.vertices = o3d.utility.Vector3dVector(verts)
#     mesh.triangles = o3d.utility.Vector3iVector(faces)
#
#     mesh.compute_vertex_normals()
#     mesh.compute_triangle_normals()
#
#     return mesh

class MainWindow(qtw.QMainWindow, Ui_MainWindow):
    def __init__(self):
        print(">>Application __init__")
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("VTK Test Window")

        # VTK rendering setup
        self.dcm_actor = None
        self.obj_actor = None

        self.vtk_renderer = vtk.vtkRenderer()
        self.vtk_render_window = self.vtk_widget.GetRenderWindow()
        self.vtk_render_window.AddRenderer(self.vtk_renderer)
        self.vtk_interactor = self.vtk_widget.GetRenderWindow().GetInteractor()

        self.named_colors = vtk.vtkNamedColors()
        color_names_string = self.named_colors.GetColorNames()
        color_names_list = color_names_string.split('\n')

        self.w_pb_dcm_plan_file.clicked.connect(self.openDcmPlanFile)
        self.w_pb_dcm_struct_file.clicked.connect(self.openDcmStructFile)
        self.w_cb_dcm_color.addItems(color_names_list)
        self.w_cb_dcm_color.currentTextChanged.connect(self.dcmColorNameChanged)
        self.w_cb_dcm_color.setCurrentText('green')
        self.w_hs_dcm_transparency.valueChanged.connect(self.dcmTransparencyChanged)

        self.w_le_dcm_plan_file.textChanged.connect(DFS.update_plan_file)
        self.w_le_dcm_struct_file.textChanged.connect(DFS.update_structure_file)

        DFS.vtk_body_actor_updated.connect(self.visualizeDicom)

        self.patient_orientation = None

        self.w_pb_obj_file.clicked.connect(self.openObjFile)
        self.w_cb_obj_color.addItems(color_names_list)
        self.w_cb_obj_color.currentTextChanged.connect(self.objColorNameChanged)
        self.w_cb_obj_color.setCurrentText('light_grey')
        self.w_hs_obj_transparency.valueChanged.connect(self.objTransparencyChanged)

        self.w_rb_hfs.toggled.connect(self.orientationChanged)
        self.w_rb_hfp.toggled.connect(self.orientationChanged)
        self.w_rb_ffs.toggled.connect(self.orientationChanged)
        self.w_rb_ffp.toggled.connect(self.orientationChanged)

        self.w_cb_background_color.addItems(color_names_list)
        self.w_cb_background_color.currentTextChanged.connect(self.backgroundColorNameChanged)
        self.w_cb_background_color.setCurrentText('black')

        self.w_pb_save_image.clicked.connect(self.saveImage)

        self.w_rb_plusX.toggled.connect(self.setCameraToPlusX)
        self.w_rb_minusX.toggled.connect(self.setCameraToMinusX)
        self.w_rb_plusY.toggled.connect(self.setCameraToPlusY)
        self.w_rb_minusY.toggled.connect(self.setCameraToMinusY)
        self.w_rb_plusZ.toggled.connect(self.setCameraToPlusZ)
        self.w_rb_minusZ.toggled.connect(self.setCameraToMinusZ)

        self.vtk_interactor.Initialize()
        self.vtk_widget.show()

    def openDcmPlanFile(self):
        print(">>openDcmPlanFile")
        filename, _ = qtw.QFileDialog.getOpenFileName(self,
                                                      "Select DICOM Structureset File",
                                                      ".",
                                                      "DICOM Files (*.dcm)"
                                                      )
        if filename:
            self.w_le_dcm_plan_file.setText(filename)

            # ds = pydicom.dcmread(filename)
            #
            # current_orientation = None
            # bypass = False
            #
            # for setup in ds.PatientSetupSequence:
            #     if current_orientation is None:
            #         current_orientation = setup.PatientPosition
            #     elif current_orientation != setup.PatientPosition:
            #         print("There are multiple patient orientations reported in the DICOM Plan")
            #     else:
            #         pass
            #
            #     if (self.patient_orientation is None) or \
            #             (self.patient_orientation != setup.PatientPosition and not bypass):
            #         print("In Bypass loop")
            #         if setup.PatientPosition == 'HFS':
            #             self.w_rb_hfs.setChecked(True)
            #         elif setup.PatientPosition == 'HFP':
            #             self.w_rb_hfp.setChecked(True)
            #         elif setup.PatientPosition == 'FFS':
            #             self.w_rb_ffs.setChecked(True)
            #         elif setup.PatientPosition == 'FFP':
            #             self.w_rb_ffp.setChecked(True)
            #         else:
            #             pass
            #         bypass = True
            #     else:
            #         pass

    def openDcmStructFile(self):
        print(">>openDcmStructFile")
        filename, _ = qtw.QFileDialog.getOpenFileName(self,
                                                      "Select DICOM Structureset File",
                                                      ".",
                                                      "DICOM Files (*.dcm)"
                                                      )
        if filename:
            self.w_le_dcm_struct_file.setText(filename)

            # Load the DICOM mesh
            # self._loadDcmMesh(filename)

    def visualizeDicom(self):
        if self.dcm_actor is None:
            self.dcm_actor = DFS.dcm_body_actor

            R, G, B = self.named_colors.GetColor3ub(self.w_cb_dcm_color.currentText())
            self.dcm_actor.GetProperty().SetColor(R / 255.0, G / 255.0, B / 255.0)
            self.dcm_actor.property.opacity = self.w_hs_dcm_transparency.value() / 100.0

            self.vtk_renderer.AddActor(self.dcm_actor)
            self.vtk_renderer.ResetCamera()
        else:
            self.vtk_renderer.RemoveActor(self.dcm_actor)
            self.dcm_actor = DFS.dcm_body_actor

            R, G, B = self.named_colors.GetColor3ub(self.w_cb_dcm_color.currentText())
            self.dcm_actor.GetProperty().SetColor(R / 255.0, G / 255.0, B / 255.0)
            self.dcm_actor.property.opacity = self.w_hs_dcm_transparency.value() / 100.0

            self.vtk_renderer.AddActor(self.dcm_actor)
            self.vtk_renderer.ResetCamera()

        self.vtk_render_window.Render()


    # def _loadDcmMesh(self, dcm_filename):
    #     print(">>_loadDcmMesh")
    #     # DICOM Point Cloud and Surface Mesh
    #     print('Reading in DICOM "Body" structure from DICOM file')
    #     dcm_pcloud = get_dcm_body_point_cloud(dcm_filename)
    #
    #     print("Generating DICOM surface using marchine cubes.")
    #     dcm_mesh = pcloud_to_mesh(dcm_pcloud, voxel_size=3, iso_level_percentile=3)
    #     print('DICOM Surface complete')
    #
    #     self.w_le_dcm_struct_file.setText(dcm_filename)
    #
    #     #############################
    #     # START: DICOM Surface Data #
    #     #############################
    #
    #     colors = vtk.vtkNamedColors()
    #
    #     dcm_verts = vtk.vtkPoints()
    #     for vert in dcm_mesh.vertices:
    #         dcm_verts.InsertNextPoint(*vert)
    #
    #     # Create a polydata object and add the points
    #     self.dcm_polydata = vtk.vtkPolyData()
    #     self.dcm_polydata.points = dcm_verts
    #
    #     # Create a vertex cell array to hold the triagles
    #     dcm_triangles = vtk.vtkCellArray()
    #     for i in range(len(dcm_mesh.triangles)):
    #         dcm_triangles.InsertNextCell(3, dcm_mesh.triangles[i])
    #     self.dcm_polydata.polys = dcm_triangles
    #
    #     # Create a mapper and actor
    #     dcm_mesh_mapper = vtk.vtkPolyDataMapper()
    #     self.dcm_polydata >> dcm_mesh_mapper
    #
    #     if self.dcm_actor is None:
    #         # Create the scene actor that represents the point cloud
    #         self.dcm_actor = vtk.vtkActor(mapper=dcm_mesh_mapper)
    #         R, G, B = self.named_colors.GetColor3ub(self.w_cb_dcm_color.currentText())
    #         self.dcm_actor.GetProperty().SetColor(R / 255.0, G / 255.0, B / 255.0)
    #         self.dcm_actor.property.opacity = self.w_hs_dcm_transparency.value() / 100.0
    #
    #         self.vtk_renderer.AddActor(self.dcm_actor)
    #         self.vtk_renderer.ResetCamera()
    #     else:
    #         self.vtk_renderer.RemoveActor(self.dcm_actor)
    #
    #         # Create the scene actor that represents the point cloud
    #         self.dcm_actor = vtk.vtkActor(mapper=dcm_mesh_mapper)
    #         self.dcm_actor.property.color = colors.GetColor3d('Green')
    #         self.dcm_actor.property.opacity = self.w_hs_dcm_transparency.value() / 100.0
    #
    #         self.vtk_renderer.AddActor(self.dcm_actor)
    #         self.vtk_renderer.ResetCamera()
    #
    #     self.vtk_render_window.Render()

    def openObjFile(self):
        print(">>openObjFile")
        filename, _ = qtw.QFileDialog.getOpenFileName(self,
                                                      "Select DICOM Structureset File",
                                                      ".",
                                                      "OBJ Files (*.obj)"
                                                      )
        if filename:
            # Load the .obj mesh
            obj_mesh = self._loadOBJMesh(filename)

    def _loadOBJMesh(self, obj_filename):
        print(">>_loadOBJMesh")
        # OBJ  File Processing
        original_mesh = trimesh.load(obj_filename)

        self.w_le_obj_file.setText(obj_filename)

        #  Transpose the axes to match the DICOM orientation
        points = np.asarray(original_mesh.vertices)

        S = obj2dcm_transform_map[self.patient_orientation]
        # S = obj2dcm_transform_map['FFS']

        new_points = (S @ points.T).T

        obj_pcloud = o3d.geometry.PointCloud()
        obj_pcloud.points = o3d.utility.Vector3dVector(new_points)

        obj_mesh = o3d.geometry.TriangleMesh()
        obj_mesh.vertices = o3d.utility.Vector3dVector(new_points)
        obj_mesh.triangles = o3d.utility.Vector3iVector(np.array(original_mesh.faces))

        obj_mesh.compute_vertex_normals()
        obj_mesh.compute_triangle_normals()

        R, G, B = self.named_colors.GetColor3ub(self.w_cb_obj_color.currentText())

        obj_points = vtk.vtkPoints()
        obj_cells = vtk.vtkCellArray()

        for point in obj_mesh.vertices:
            obj_points.InsertNextPoint(*point)

        self.obj_polydata = vtk.vtkPolyData()
        self.obj_polydata.points = obj_points

        for i in range(len(obj_mesh.triangles)):
            obj_cells.InsertNextCell(3, obj_mesh.triangles[i])
        self.obj_polydata.polys = obj_cells

        # self.obj_mapper = vtk.vtkOpenGLPolyDataMapper()
        self.obj_mapper = vtk.vtkPolyDataMapper()
        self.obj_polydata >> self.obj_mapper

        if self.obj_actor is None:
            self.obj_actor = vtk.vtkActor(mapper=self.obj_mapper)
            self.obj_actor.GetProperty().SetColor(R / 255.0, G / 255.0, B / 255.0)

            self.vtk_renderer.AddActor(self.obj_actor)
            self.vtk_renderer.ResetCamera()
        else:
            self.vtk_renderer.RemoveActor(self.obj_actor)

            self.obj_actor = vtk.vtkActor(mapper=self.obj_mapper)
            self.obj_actor.GetProperty().SetColor(R / 255.0, G / 255.0, B / 255.0)

            self.vtk_renderer.AddActor(self.obj_actor)
            self.vtk_renderer.ResetCamera()

        self.vtk_render_window.Render()

    def dcmColorNameChanged(self):
        print(">>dcmColorNameChanged")
        R, G, B = self.named_colors.GetColor3ub(self.w_cb_dcm_color.currentText())
        self.w_dcm_color_frame.setStyleSheet(f"background-color: rgb({R}, {G}, {B});")
        self.w_dcm_color_frame.show()

        if self.dcm_actor is not None:
            self.dcm_actor.GetProperty().SetColor(R / 255.0, G / 255.0, B / 255.0)
            self.vtk_render_window.Render()

    def dcmTransparencyChanged(self):
        print(">>dcmTransparencyChanged")
        self.w_l_dcm_transparency.setText(str(self.w_hs_dcm_transparency.value()))
        if self.dcm_actor.property is not None:
            self.dcm_actor.property.opacity = self.w_hs_dcm_transparency.value() / 100.0
            self.vtk_render_window.Render()
        else:
            pass

    def objColorNameChanged(self):
        print(">>objColorNameChanged")
        R, G, B = self.named_colors.GetColor3ub(self.w_cb_obj_color.currentText())
        self.w_obj_color_frame.setStyleSheet(f"background-color: rgb({R}, {G}, {B});")
        self.w_obj_color_frame.show()

        if self.obj_actor is not None:
            self.obj_actor.GetProperty().SetColor(R / 255.0, G / 255.0, B / 255.0)
            self.vtk_render_window.Render()

    def objTransparencyChanged(self):
        print(">>objTransparencyChanged")
        self.w_l_obj_transparency.setText(str(self.w_hs_obj_transparency.value()))
        if self.obj_actor.property is not None:
            self.obj_actor.property.opacity = self.w_hs_obj_transparency.value() / 100.0
            self.vtk_render_window.Render()
        else:
            pass

    def backgroundColorNameChanged(self):
        print(">>backgroundColorNameChanged")
        R, G, B = self.named_colors.GetColor3ub(self.w_cb_background_color.currentText())
        self.w_background_color_frame.setStyleSheet(f"background-color: rgb({R}, {G}, {B});")
        self.w_background_color_frame.show()

        self.vtk_renderer.SetBackground(R/255.0, G/255.0, B/255.0)
        self.vtk_render_window.Render()

    def orientationChanged(self, checked):
        print(">>orientationChanged")
        print(f"{self.sender()} is checked: {checked}")
        if checked:
            if self.sender().objectName() == 'w_rb_hfs':
                self.patient_orientation = 'HFS'

                if self.obj_actor is not None:
                    self._loadOBJMesh(self.w_le_obj_file.text())


            elif self.sender().objectName() == 'w_rb_hfp':
                self.patient_orientation = 'HFP'

                if self.obj_actor is not None:
                    self._loadOBJMesh(self.w_le_obj_file.text())

            elif self.sender().objectName() == 'w_rb_ffs':
                self.patient_orientation = 'FFS'

                if self.obj_actor is not None:
                    self._loadOBJMesh(self.w_le_obj_file.text())

            elif self.sender().objectName() == 'w_rb_ffp':
                self.patient_orientation = 'FFP'

                if self.obj_actor is not None:
                    self._loadOBJMesh(self.w_le_obj_file.text())

    def saveImage(self):
        filename, _ = qtw.QFileDialog.getSaveFileName(self,
                                                      "Save Render Window as Image",
                                                      ".",
                                                      "PNG Image (*.png);;BitMap Image (*.bmp)"
                                                      )

        print(filename)

        if filename:
            # Create a window-to-image filter
            window_to_image_filter = vtk.vtkWindowToImageFilter()
            window_to_image_filter.SetInput(self.vtk_render_window)
            window_to_image_filter.SetInputBufferTypeToRGBA()  # Optional: Ensure RGBA format
            window_to_image_filter.ReadFrontBufferOff()  # Optional: Read from the front buffer
            window_to_image_filter.Update()

            # Create a writer (e.g., PNG writer)
            ext = filename[-3:]
            writer = vtk.vtkPNGWriter() if ext == 'png' else vtk.vtkBMPWriter() #, vtkTIFFWriter, etc.
            writer.SetFileName(filename)
            writer.SetInputConnection(window_to_image_filter.GetOutputPort())
            writer.Write()

    def _getViewingFlag(self):
        if self.dcm_actor is None:
            if self.obj_actor is None:
                return None
            else:
                return 2
        else:
            if self.obj_actor is None:
                return 1
            else:
                return 3

    def _getViewingBounds(self):
        flag = self._getViewingFlag()
        if flag == 1:
            print('Viewport contains DICOM only')
            print(self.dcm_polydata.bounds)

            return self.dcm_polydata.bounds
        elif flag == 2:
            print('Viewport contains OBJ only')
            print(self.obj_polydata.bounds)

            return self.obj_polydata.bounds
        elif flag == 3:
            print('Viewport contains both DICOM and OBJ')
            print(self.dcm_polydata.bounds)
            print(self.obj_polydata.bounds)

            _x_min, _x_max, _y_min, _y_max, _z_min, _z_max = self.dcm_polydata.bounds
            __x_min, __x_max, __y_min, __y_max, __z_min, __z_max = self.obj_polydata.bounds

            x_min = _x_min if _x_min <= __x_min else __x_min
            x_max = _x_max if _x_max >= __x_max else __x_max
            y_min = _y_min if _y_min <= __y_min else __y_min
            y_max = _y_max if _y_max >= __y_max else __y_max
            z_min = _z_min if _z_min <= __z_min else __z_min
            z_max = _z_max if _z_max >= __z_max else __z_max

            return (x_min, x_max, y_min, y_max, z_min, z_max)

    def setCameraToPlusX(self):
        if self.w_rb_plusX.isChecked():
            camera = self.vtk_renderer.GetActiveCamera()
            x_min, x_max, y_min, y_max, z_min, z_max = self._getViewingBounds()
            center = [(x_min + x_max) / 2.0, (y_min + y_max) / 2.0, (z_min + z_max) / 2.0]

            x_length = x_max - x_min
            y_length = y_max - y_min
            z_length = z_max - z_min
            max_length = max(x_length, y_length, z_length)

            # # Set near clipping distance to a small fraction of the max length
            # near_clipping = max_length / 1000.0
            # # Set far clipping distance to a value larger than the max length
            # far_clipping = max_length * 10
            # camera.SetClippingRange(near_clipping, far_clipping)

            camera.SetPosition(x_max + max_length, center[1], center[2])
            camera.SetFocalPoint(center[0], center[1], center[2])
            camera.SetViewUp(0, 1, 0)
            camera.SetParallelProjection(True)
            self.vtk_renderer.ResetCameraClippingRange()
            self.vtk_render_window.Render()

    def setCameraToMinusX(self):
        if self.w_rb_minusX.isChecked():
            camera = self.vtk_renderer.GetActiveCamera()
            x_min, x_max, y_min, y_max, z_min, z_max = self._getViewingBounds()
            center = [(x_min + x_max) / 2.0, (y_min + y_max) / 2.0, (z_min + z_max) / 2.0]

            x_length = x_max - x_min
            y_length = y_max - y_min
            z_length = z_max - z_min
            max_length = max(x_length, y_length, z_length)

            camera.SetPosition(x_min - max_length, center[1], center[2])
            camera.SetFocalPoint(center[0], center[1], center[2])
            camera.SetViewUp(0, 1, 0)
            camera.SetParallelProjection(True)
            self.vtk_renderer.ResetCameraClippingRange()
            self.vtk_render_window.Render()

    def setCameraToPlusY(self):
        if self.w_rb_plusY.isChecked():
            camera = self.vtk_renderer.GetActiveCamera()
            x_min, x_max, y_min, y_max, z_min, z_max = self._getViewingBounds()
            center = [(x_min + x_max) / 2.0, (y_min + y_max) / 2.0, (z_min + z_max) / 2.0]

            x_length = x_max - x_min
            y_length = y_max - y_min
            z_length = z_max - z_min
            max_length = max(x_length, y_length, z_length)

            camera.SetPosition(center[0], y_max + max_length, center[2])
            camera.SetFocalPoint(center[0], center[1], center[2])
            camera.SetViewUp(0, 0, -1)
            camera.SetParallelProjection(True)
            self.vtk_renderer.ResetCameraClippingRange()
            self.vtk_render_window.Render()

    def setCameraToMinusY(self):
        if self.w_rb_minusY.isChecked():
            camera = self.vtk_renderer.GetActiveCamera()
            x_min, x_max, y_min, y_max, z_min, z_max = self._getViewingBounds()
            center = [(x_min + x_max) / 2.0, (y_min + y_max) / 2.0, (z_min + z_max) / 2.0]

            x_length = x_max - x_min
            y_length = y_max - y_min
            z_length = z_max - z_min
            max_length = max(x_length, y_length, z_length)

            camera.SetPosition(center[0], y_min - max_length, center[2])
            camera.SetFocalPoint(center[0], center[1], center[2])
            camera.SetViewUp(0, 0, -1)
            camera.SetParallelProjection(True)
            self.vtk_renderer.ResetCameraClippingRange()
            self.vtk_render_window.Render()

    def setCameraToPlusZ(self):
        if self.w_rb_plusZ.isChecked():
            camera = self.vtk_renderer.GetActiveCamera()
            x_min, x_max, y_min, y_max, z_min, z_max = self._getViewingBounds()
            center = [(x_min + x_max) / 2.0, (y_min + y_max) / 2.0, (z_min + z_max) / 2.0]

            x_length = x_max - x_min
            y_length = y_max - y_min
            z_length = z_max - z_min
            max_length = max(x_length, y_length, z_length)

            camera.SetPosition(center[0], center[1], z_max + max_length)
            camera.SetFocalPoint(center[0], center[1], center[2])
            camera.SetViewUp(0, 1, 0)
            camera.SetParallelProjection(True)
            self.vtk_renderer.ResetCameraClippingRange()
            self.vtk_render_window.Render()

    def setCameraToMinusZ(self):
        if self.w_rb_minusZ.isChecked():
            camera = self.vtk_renderer.GetActiveCamera()
            x_min, x_max, y_min, y_max, z_min, z_max = self._getViewingBounds()
            center = [(x_min + x_max) / 2.0, (y_min + y_max) / 2.0, (z_min + z_max) / 2.0]

            x_length = x_max - x_min
            y_length = y_max - y_min
            z_length = z_max - z_min
            max_length = max(x_length, y_length, z_length)

            camera.SetPosition(center[0], center[1], z_min - max_length)
            camera.SetFocalPoint(center[0], center[1], center[2])
            camera.SetViewUp(0, 1, 0)
            camera.SetParallelProjection(True)
            self.vtk_renderer.ResetCameraClippingRange()
            self.vtk_render_window.Render()


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())