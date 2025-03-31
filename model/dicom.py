import pydicom
import numpy as np
import open3d as o3d
from skimage import measure
from scipy.spatial import cKDTree

import vtk
from vtkmodules.util import numpy_support

import PySide6.QtCore as qtc

class DicomRTPlanFile(qtc.QObject):

    filePathChanged = qtc.Signal(str)

    def __init__(self):
        super().__init__()
        self._filepath = None
        self.patient_orientation = None

    @property
    def filepath(self):
        return self._filepath

    @filepath.setter
    def filepath(self, new_path):
        self._filepath = new_path
        self.filePathChanged.emit(new_path)

    qtc.Slot(str)
    def update_path(self, new_path):
        print("In DicomRTPlan model update_path Slot")
        self._filepath = new_path
        ds = pydicom.dcmread(new_path)

        if hasattr(ds, "PatientSetupSequence"):
            for i in range(len(ds.PatientSetupSequence)):
                orientation = ds.PatientSetupSequence[i].PatientPosition

                if (self.patient_orientation is None) or (i == 0):
                    self.patient_orientation = orientation
                elif self.patient_orientation != orientation:
                    print("There are multiple patient orientations reported in the DICOM Plan")
                else:
                    pass
        else:
            print("Not a valid DICOM RT Plan file.")

class DicomRTStructureSetFile(qtc.QObject):

    filePathChanged = qtc.Signal(str)
    vtkActorUpdated = qtc.Signal()

    def __init__(self):
        super().__init__()
        self._filepath = None
        self.patient_orientation = None

    @property
    def filepath(self):
        return self._filepath

    @filepath.setter
    def filepath(self, new_path):
        self._filepath = new_path
        self.filePathChanged.emit(new_path)

    def _get_body_point_cloud(self):
        # Read DICOM Structure Set
        ds = pydicom.dcmread(self.filepath)

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

        dcm_pcloud = o3d.geometry.PointCloud()
        dcm_pcloud.points = o3d.utility.Vector3dVector(dcm_points)
        dcm_pcloud.estimate_normals()

        return dcm_pcloud

    def _pcloud_to_mesh(self, pcd, voxel_size=3, iso_level_percentile=5):
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

    qtc.Slot(str)
    def update_path(self, new_path):
        print("In DicomFileSyncModel update_path Slot")
        self._filepath = new_path

        print('Reading in DICOM "Body" structure from DICOM file')
        dcm_pcloud = self._get_body_point_cloud()

        print("Generating DICOM surface using marchine cubes.")
        dcm_mesh = self._pcloud_to_mesh(dcm_pcloud, voxel_size=3, iso_level_percentile=3)
        print('DICOM Surface complete')

        # Create a polydata object and add the points
        self.dcm_polydata = vtk.vtkPolyData()
        self.dcm_polydata.points = numpy_support.numpy_to_vtk(dcm_mesh.vertices)

        # Create a vertex cell array to hold the triagles
        dcm_triangles = vtk.vtkCellArray()
        for i in range(len(dcm_mesh.triangles)):
            dcm_triangles.InsertNextCell(3, dcm_mesh.triangles[i])
        self.dcm_polydata.polys = dcm_triangles

        # Create a mapper and actor
        dcm_mesh_mapper = vtk.vtkPolyDataMapper()
        self.dcm_polydata >> dcm_mesh_mapper


        # Create the scene actor that represents the point cloud
        self.dcm_body_actor = vtk.vtkActor(mapper=dcm_mesh_mapper)
        self.dcm_body_actor.GetProperty().SetColor(0, 1, 0)
        self.dcm_body_actor.property.opacity = 1

        self.vtkActorUpdated.emit()

class DicomFileStackModel(qtc.QObject):

    plan_file_changed = qtc.Signal(str)
    patient_orientation_changed = qtc.Signal(str)
    structure_file_changed = qtc.Signal(str)
    vtk_actor_updated = qtc.Signal()

    def __init__(self):
        super().__init__()
        self._plan_file = None
        self.patient_orientation = None
        self.plan_file_changed.connect(self.update_plan_file)

        self._structure_file = None
        self.structure_file_changed.connect(self.update_structure_file)

    @property
    def plan_file(self):
        return self._plan_file

    @plan_file.setter
    def plan_file(self, new_path):
        self.plan_file_changed.emit(new_path)

    @property
    def structure_file(self):
        return self._structure_file

    @structure_file.setter
    def structure_file(self, new_path):
        self.structure_file_changed.emit(new_path)

    qtc.Slot(str)
    def update_plan_file(self, new_path):
        print("In DicomFileSyncModel update_plan_file Slot")
        self._plan_file = new_path
        ds = pydicom.dcmread(self.plan_file)

        if hasattr(ds, "PatientSetupSequence"):
            for i in range(len(ds.PatientSetupSequence)):
                orientation = ds.PatientSetupSequence[i].PatientPosition

                if (self.patient_orientation is None) or (i == 0):
                    self.patient_orientation = orientation
                    self.patient_orientation_changed.emit(orientation)
                elif self.patient_orientation != orientation:
                    print("There are multiple patient orientations reported in the DICOM Plan")
                else:
                    pass
        else:
            print("Not a valid DICOM RT Plan file.")

    def _get_body_point_cloud(self):
        # Read DICOM Structure Set
        ds = pydicom.dcmread(self.structure_file)

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

        dcm_pcloud = o3d.geometry.PointCloud()
        dcm_pcloud.points = o3d.utility.Vector3dVector(dcm_points)
        dcm_pcloud.estimate_normals()

        return dcm_pcloud

    def _pcloud_to_mesh(self, pcd, voxel_size=3, iso_level_percentile=5):
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

    qtc.Slot(str)
    def update_structure_file(self, new_path):
        print("In DicomFileSyncModel update_structure_file Slot")
        self._structure_file = new_path

        print('Reading in DICOM "Body" structure from DICOM file')
        dcm_pcloud = self._get_body_point_cloud()

        print("Generating DICOM surface using marchine cubes.")
        dcm_mesh = self._pcloud_to_mesh(dcm_pcloud, voxel_size=3, iso_level_percentile=3)
        print('DICOM Surface complete')

        # Create a polydata object and add the points
        self.dcm_polydata = vtk.vtkPolyData()
        self.dcm_polydata.points = numpy_support.numpy_to_vtk(dcm_mesh.vertices)

        # Create a vertex cell array to hold the triagles
        dcm_triangles = vtk.vtkCellArray()
        for i in range(len(dcm_mesh.triangles)):
            dcm_triangles.InsertNextCell(3, dcm_mesh.triangles[i])
        self.dcm_polydata.polys = dcm_triangles

        # Create a mapper and actor
        dcm_mesh_mapper = vtk.vtkPolyDataMapper()
        self.dcm_polydata >> dcm_mesh_mapper


        # Create the scene actor that represents the point cloud
        self.dcm_body_actor = vtk.vtkActor(mapper=dcm_mesh_mapper)
        self.dcm_body_actor.GetProperty().SetColor(0, 1, 0)
        self.dcm_body_actor.property.opacity = 1

        self.vtk_actor_updated.emit()
