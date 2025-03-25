import sys

import pydicom
import numpy as np
from skimage import measure
from scipy.spatial import cKDTree

import PySide6.QtCore as qtc
import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg

import trimesh
import open3d as o3d

import vtk
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from MapApp.ui.test_window import Ui_MainWindow

dcm_filename = r'C:\__python__\Projects\PythonUIProjectsWithQt\VTK_Window\data\matched_dicom_ss.dcm'
obj_filename = r'C:\__python__\Projects\PythonUIProjectsWithQt\VTK_Window\data\matched_mergedSurface.obj'

# Define helper functions
def get_dcm_body_point_cloud(dcm_filename):
    # Read DICOM Structure Set
    ds = pydicom.dcmread(dcm_filename)

    # Generate ROI Look Up Table using the ROI Number as the key
    roi_lut = {}
    for structure in ds.StructureSetROISequence:
        # print(f'{structure.ROIName} ({structure.ROIName.lower()})',
        #       structure.ROINumber
        #       )
        roi_lut[structure.ROINumber] = structure.ROIName.lower()

    # Grab the Body structure points
    body_contours = []
    for roi in ds.ROIContourSequence:
        if (roi.ReferencedROINumber in roi_lut) and \
                roi_lut[roi.ReferencedROINumber] == 'body':
            # print('Found Body')
            for contour in roi.ContourSequence:
                # print(contour.ContourData)
                body_contours.append([[float(contour.ContourData[i]),
                                       float(contour.ContourData[i + 1]),
                                       float(contour.ContourData[i + 2])
                                       ] \
                                      for i in range(0,
                                                     len(contour.ContourData),
                                                     3
                                                     )
                                      ]
                                     )

    dcm_points = np.array([point for contour in body_contours \
                           for point in contour
                           ]
                          )

    dcm_colors = np.zeros(dcm_points.shape)
    dcm_colors[:, :] = [0.0, 0.5, 0.0]

    dcm_pcloud = o3d.geometry.PointCloud()
    dcm_pcloud.points = o3d.utility.Vector3dVector(dcm_points)
    dcm_pcloud.colors = o3d.utility.Vector3dVector(dcm_colors)
    dcm_pcloud.estimate_normals()

    return dcm_pcloud

def pcloud_to_mesh(pcd, voxel_size=3, iso_level_percentile=5):
    # Convet Open3D point cloud to numpy array
    points = np.asarray(pcd.points)

    # Compute the bounds of the point cloud
    mins = pcd.get_min_bound()
    maxs = pcd.get_max_bound()

    # print(mins)
    # print(maxs)

    x = np.arange(mins[0], maxs[0], voxel_size)
    y = np.arange(mins[1], maxs[1], voxel_size)
    z = np.arange(mins[2], maxs[2], voxel_size)
    x, y, z = np.meshgrid(x, y, z, indexing='ij')

    # Create a KD-tree for efficient nearest neighbor search
    tree = cKDTree(points)

    # Compute the scalar field (distance to nearest point)
    grid_points = np.vstack([x.ravel(), y.ravel(), z.ravel()]).T
    print(f'Using {len(x.ravel())} grid_points for marching cubes')
    distances, _ = tree.query(grid_points, workers=-1)
    scalar_field = distances.reshape(x.shape)

    # Determine the iso_level based on the percentile of distance
    iso_level = np.percentile(distances, iso_level_percentile)

    # Apply Marching Cubes
    verts, faces, _, _ = measure.marching_cubes(scalar_field, level=iso_level)

    # Scale and translate vertices back to original coordinate system
    verts = verts * voxel_size + mins

    # Create the mesh
    mesh = o3d.geometry.TriangleMesh()
    mesh.vertices = o3d.utility.Vector3dVector(verts)
    mesh.triangles = o3d.utility.Vector3iVector(faces)

    mesh.compute_vertex_normals()
    mesh.compute_triangle_normals()

    return mesh

def load_dicom_mesh(dcm_filename):
    # DICOM Point Cloud and Surface Mesh
    print('Reading in DICOM "Body" structure from DICOM file')
    dcm_pcloud = get_dcm_body_point_cloud(dcm_filename)
    print("Generating DICOM surface using marchine cubes.")
    mesh = pcloud_to_mesh(dcm_pcloud, voxel_size=3, iso_level_percentile=3)
    print('DICOM Surface complete')

    return mesh

def load_obj_mesh(obj_filename):
    # OBJ  File Processing
    print('Loading .obj surface')
    obj_mesh = trimesh.load(obj_filename)

    #  Transpose the axes to match the DICOM orientation
    points = np.asarray(obj_mesh.vertices)
    S = np.array([[0, 1, 0],
                  [0, 0, 1],
                  [1, 0, 0]
                  ]
                 )
    new_points = (S @ points.T).T
    new_point_colors = np.random.rand(*new_points.shape)

    obj_pcloud = o3d.geometry.PointCloud()
    obj_pcloud.points = o3d.utility.Vector3dVector(new_points)
    obj_pcloud.colors = o3d.utility.Vector3dVector(new_point_colors)

    mesh = o3d.geometry.TriangleMesh()
    mesh.vertices = o3d.utility.Vector3dVector(new_points)
    mesh.triangles = o3d.utility.Vector3iVector(np.array(obj_mesh.faces))

    mesh.compute_vertex_normals()
    mesh.compute_triangle_normals()
    mesh.paint_uniform_color([0.5, 0, 0.5])

    return mesh

class MainWindow(qtw.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("VTK Test Window")

        self.w_pb_dicom_file.clicked.connect(self.openDicomFile)
        self.w_pb_obj_file.clicked.connect(self.openObjFile)


        # VTK rendering setup
        self.vtk_renderer = vtk.vtkRenderer()

        self.vtk_render_window = self.vtk_widget.GetRenderWindow()
        self.vtk_render_window.AddRenderer(self.vtk_renderer)
        self.vtk_interactor = self.vtk_widget.GetRenderWindow().GetInteractor()

        self.vtk_interactor.Initialize()
        self.vtk_widget.show()

    def openDicomFile(self):
        filename, _ = qtw.QFileDialog.getOpenFileName(self,
                                                      "Select DICOM Structureset File",
                                                      ".",
                                                      "DICOM Files (*.dcm)"
                                                      )
        if filename:
            self.w_le_dicom_file.setText(filename)

            # Load the DICOM mesh
            dcm_mesh = load_dicom_mesh(filename)

            #############################
            # START: DICOM Surface Data #
            #############################

            colors = vtk.vtkNamedColors()

            dcm_verts = vtk.vtkPoints()
            for vert in dcm_mesh.vertices:
                dcm_verts.InsertNextPoint(*vert)

            # Create a polydata object and add the points
            dcm_mesh_poly = vtk.vtkPolyData()
            dcm_mesh_poly.points = dcm_verts

            # Create a vertex cell array to hold the triagles
            dcm_triangles = vtk.vtkCellArray()
            for i in range(len(dcm_mesh.triangles)):
                dcm_triangles.InsertNextCell(3, dcm_mesh.triangles[i])
            dcm_mesh_poly.polys = dcm_triangles

            # Create a mapper and actor
            dcm_mesh_mapper = vtk.vtkPolyDataMapper()
            dcm_mesh_poly >> dcm_mesh_mapper

            # Create the scene actor that represents the point cloud
            dcm_mesh_actor = vtk.vtkActor(mapper=dcm_mesh_mapper)
            dcm_mesh_actor.property.color = colors.GetColor3d('Green')
            dcm_mesh_actor.property.opacity = 1


            self.vtk_renderer.AddActor(dcm_mesh_actor)
            self.vtk_renderer.ResetCamera()

            self.vtk_render_window.Render()


            ###########################
            # END: DICOM Surface Data #
            ###########################

    def openObjFile(self):
        filename, _ = qtw.QFileDialog.getOpenFileName(self,
                                                      "Select DICOM Structureset File",
                                                      ".",
                                                      "OBJ Files (*.obj)"
                                                      )
        if filename:
            self.w_le_obj_file.setText(filename)

            # Load the .obj mesh
            obj_mesh = load_obj_mesh(filename)

            ###########################
            # START: OBJ Surface Data #
            ###########################

            colors = vtk.vtkNamedColors()

            obj_points = vtk.vtkPoints()
            obj_cells = vtk.vtkCellArray()

            for point in obj_mesh.vertices:
                obj_points.InsertNextPoint(*point)

            obj_poly = vtk.vtkPolyData()
            obj_poly.points = obj_points

            for i in range(len(obj_mesh.triangles)):
                obj_cells.InsertNextCell(3, obj_mesh.triangles[i])
            obj_poly.polys = obj_cells

            obj_mapper = vtk.vtkOpenGLPolyDataMapper()
            obj_poly >> obj_mapper

            obj_mesh_actor = vtk.vtkActor(mapper=obj_mapper)
            obj_mesh_actor.property.color = colors.GetColor3d('LightBlue')

            self.vtk_renderer.AddActor(obj_mesh_actor)
            self.vtk_renderer.ResetCamera()

            self.vtk_render_window.Render()

            #########################
            # END: OBJ Surface Data #
            #########################


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())