import pydicom
from pydicom import dcmread
from pynetdicom.sop_class import RTPlanStorage, RTStructureSetStorage

import numpy as np
import open3d as o3d
from skimage import measure
from scipy.spatial import cKDTree

import vtk
from vtkmodules.util import numpy_support

import PySide6.QtCore as qtc

class DicomFileValidationError(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)

class DicomRTPlan(qtc.QObject):

    file_path_changed = qtc.Signal(str)
    invalid_file_loaded = qtc.Signal(str)
    plan_model_updated = qtc.Signal()

    def __init__(self):
        super().__init__()
        self._parent = None
        self._filepath = None

        self._patient_id = None
        self._patient_first_name = None
        self._patient_last_name = None
        self._patient_orientation = None
        self._plan_id = None
        self._frame_of_reference_uid = None
        self._beams = []

        self._structure_set = DicomRTStructureSet()
        self._body = None

    @property
    def filepath(self):
        return self._filepath

    @filepath.setter
    def filepath(self, new_path):
        if new_path != self._filepath:
            self.update_filepath(new_path)

    @property
    def patient_id(self):
        return self._patient_id

    @property
    def patient_first_name(self):
        return self._patient_first_name

    @property
    def patient_last_name(self):
        return self._patient_last_name

    @property
    def patient_orientation(self):
        return self._patient_orientation

    @property
    def plan_id(self):
        return self._plan_id

    @property
    def frame_of_reference_uid(self):
        return self._frame_of_reference_uid

    @property
    def structure_set(self):
        return self._structure_set

    @property
    def beams(self):
        return self._beams

    qtc.Slot(str)
    def update_filepath(self, new_path):
        print("In DicomRTPlan model update_path Slot")
        self.ds = dataset = pydicom.dcmread(new_path)

        if dataset.file_meta.MediaStorageSOPClassUID == RTPlanStorage:
            self._filepath = new_path
            self.file_path_changed.emit(self.filepath)

            self._patient_id = dataset.PatientID

            name = str(dataset.PatientName).split('^')
            if len(name) == 1:
                self._patient_first_name, = name
            elif len(name) == 2:
                self._patient_last_name, self._patient_first_name = name
            elif len(name) == 3:
                self._patient_last_name = name[0]
                self._patient_first_name = name[1]
            else:
                self._patient_first_name = dataset.PatientID

            for i in range(len(dataset.PatientSetupSequence)):
                orientation = dataset.PatientSetupSequence[i].PatientPosition

                if (self._patient_orientation is None) or (i == 0):
                    self._patient_orientation = orientation
                elif self._patient_orientation != orientation:
                    print("There are multiple patient orientations reported in the DICOM Plan")
                else:
                    pass

            self._plan_id = dataset.SeriesDescription
            self._frame_of_reference_uid = dataset.FrameOfReferenceUID

            for beam in dataset.BeamSequence:
                _status = ''
                _num = str(beam.BeamNumber)
                _id = str(beam.BeamName)

                vms_name = beam.get((0x3243, 0x1009), None)
                _name = '' if vms_name is None else vms_name.value.decode('utf-8')

                _type = beam.TreatmentDeliveryType

                first_cp = beam.ControlPointSequence[0]
                last_cp = beam.ControlPointSequence[-1]

                _gantry_start = _gantry_stop = str(first_cp.GantryAngle)

                if hasattr(last_cp, 'GantryAngle'):
                    _gantry_stop = str(last_cp.GantryAngle)

                _gantry_rot_direction = str(first_cp.GantryRotationDirection)

                _couch = str(first_cp.PatientSupportAngle)

                self.beams.append([_status,
                                   _num,
                                   _id,
                                   _name,
                                   _type,
                                   _gantry_start,
                                   _gantry_stop,
                                   _gantry_rot_direction,
                                   _couch]
                                  )

                # print(f'Beam Number: {_num}')
                # print(f'Beam ID: {_id}')
                # print(f'Beam Name: {_name}')
                # print(f'Beam Type: {_type}')
                # print(f'\tNumber of Control Points: {len(beam.ControlPointSequence)}')
                # print(f'\tGantry Start Angle: {_gantry_start}')
                # print(f'\tGantry Stop Angle: {_gantry_stop}')
                # print(f'\tGantry Rotation Direction: {_gantry_rot_direction}')
                # print(f'\tCouch: {_couch}')

            self.plan_model_updated.emit()
        else:
            self.invalid_file_loaded.emit(f"{new_path} is not a valid DICOM RT Plan file.")
            raise DicomFileValidationError("Not a valid DICOM RT Plan file.")

class DicomRTStructureSet(qtc.QObject):

    file_path_changed = qtc.Signal(str)
    invalid_file_loaded = qtc.Signal(str)
    vtkActorUpdated = qtc.Signal()

    def __init__(self):
        super().__init__()
        self._filepath = None
        self._dataset = None

        self._patinet_id = None

    @property
    def filepath(self):
        return self._filepath

    @filepath.setter
    def filepath(self, new_path):
        if new_path != self._filepath:
            self.update_filepath(new_path)

    @property
    def dataset(self):
        return self._dataset

    def _get_body_point_cloud(self):
        # Read DICOM Structure Set
        self._dataset = pydicom.dcmread(self.filepath)

        # Generate ROI Look Up Table using the ROI Number as the key
        roi_lut = {}
        for structure in self._dataset.StructureSetROISequence:
            # print(f'{structure.ROIName} ({structure.ROIName.lower()})',
            #       structure.ROINumber
            #       )
            roi_lut[structure.ROINumber] = structure.ROIName.lower()

        # Grab the Body structure points
        body_contours = []
        for roi in self._dataset.ROIContourSequence:
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
    def update_filepath(self, new_path):
        self._dataset = dcmread(new_path)

        if self._dataset.file_meta.MediaStorageSOPClassUID == RTStructureSetStorage:
            self._filepath = new_path
            self.file_path_changed.emit(self.filepath)

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
        else:
            self.invalid_file_loaded.emit(f"{new_path} is not a valid DICOM RT Structure Set file.")

class DicomRTBroker(qtc.QObject):

    def __init__(self):
        super().__init__()
        self.dicom_plan = DicomRTPlan()
        self.dicom_structures = DicomRTStructureSet()
