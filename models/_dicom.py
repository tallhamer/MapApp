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

class DicomPlanContext(qtc.QObject):
    structures_loaded = qtc.Signal(list)
    current_structure_changed = qtc.Signal(vtk.vtkActor)

    def __init__(self, plan_id, isocenter, orientation, beams, ref_frame=None):
        super().__init__()
        self._plan_id = plan_id
        self._frame_of_reference_uid = ref_frame
        self._isocenter = isocenter
        self._patient_orientation = orientation
        self._beams = beams

        self._raw_structure_points = {}  # structure id: raw contour points (used with DICOM RT FIles)
        self._structures = {}  # structure id: vtk_actor
        self._current_structure = None  # vtk_actor

    @property
    def plan_id(self):
        return self._plan_id

    @property
    def frame_of_reference_uid(self):
        return self._frame_of_reference_uid

    @property
    def isocenter(self):
        return self._isocenter

    @property
    def patient_orientation(self):
        return self._patient_orientation

    @property
    def beams(self):
        return self._beams

    @property
    def structures(self):
        return [key for key in self._structures.keys()]

    @property
    def current_structure(self):
        return self._current_structure

    def update_current_structure(self, structure_id):
        if self._structures[structure_id] is not None:
            print("Using cashed mesh")
            self._current_structure = self._structures[structure_id]
            self.current_structure_changed.emit(self.current_structure)
        else:
            print("Generating DICOM surface using marching cubes.")
            mesh = self._pcloud_to_mesh(self._raw_structure_points[structure_id], voxel_size=3, iso_level_percentile=3)
            print('DICOM Surface complete')
            self._structures[structure_id] = self._generate_visual_mesh(mesh)
            self._current_structure = self._structures[structure_id]
            self.current_structure_changed.emit(self.current_structure)

    def load_structures_from_dicom_rt_file(self, file_path):
        ds = pydicom.dcmread(file_path)
        if ds.file_meta.MediaStorageSOPClassUID == RTStructureSetStorage:
            if ds.FrameOfReferenceUID == self.frame_of_reference_uid:
                print('Reading in DICOM structures from DICOM file')
                self._get_structure_point_clouds(ds)
            else:
                raise DicomFileValidationError(f"{file_path} dose not match the loaded DICOM RT Plan.")
        else:
            raise DicomFileValidationError(f"{file_path} is not a valid DICOM RT Structure Set file.")

    def _get_structure_point_clouds(self, ds):
        # Generate ROI Look Up Table using the ROI Number as the key
        roi_lut = {}
        for structure in ds.StructureSetROISequence:
            # print(f'{structure.ROIName} ({structure.ROIName.lower()})',
            #       structure.ROINumber
            #       )
            roi_lut[structure.ROINumber] = structure.ROIName.lower()

        # Grab the Body structure points
        contours = []
        for roi in ds.ROIContourSequence:
            # if (roi.ReferencedROINumber in roi_lut) and \
            #         roi_lut[roi.ReferencedROINumber] == 'body':
            #     # print('Found Body')
            contours = []
            if hasattr(roi, "ContourSequence"):
                # print(roi_lut[roi.ReferencedROINumber])
                for contour in roi.ContourSequence:
                    contours.append([[float(contour.ContourData[i]),
                                      float(contour.ContourData[i + 1]),
                                      float(contour.ContourData[i + 2])
                                      ] for i in range(0,
                                                       len(contour.ContourData),
                                                       3
                                                       )
                                     ]
                                    )

                dcm_points = np.array([point for contour in contours for point in contour])

                dcm_pcloud = o3d.geometry.PointCloud()
                dcm_pcloud.points = o3d.utility.Vector3dVector(dcm_points)
                dcm_pcloud.estimate_normals()

                self._raw_structure_points[roi_lut[roi.ReferencedROINumber]] = dcm_pcloud
                self._structures[roi_lut[roi.ReferencedROINumber]] = None

        self.structures_loaded.emit(self.structures)

    def _pcloud_to_mesh(self, pcd, voxel_size=3, iso_level_percentile=5):
        # Convet Open3D point cloud to numpy array
        points = np.asarray(pcd.points)

        # Compute the bounds of the point cloud
        mins = pcd.get_min_bound()
        maxs = pcd.get_max_bound()

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

    def _generate_visual_mesh(self, mesh):
        # Create a polydata object and add the points
        polydata = vtk.vtkPolyData()
        polydata.points = numpy_support.numpy_to_vtk(mesh.vertices)

        # Create a vertex cell array to hold the triagles
        triangles = vtk.vtkCellArray()
        for i in range(len(mesh.triangles)):
            triangles.InsertNextCell(3, mesh.triangles[i])
        polydata.polys = triangles

        # Create a mapper and actor
        mapper = vtk.vtkPolyDataMapper()
        polydata >> mapper

        # Create the scene actor that represents the point cloud
        actor = vtk.vtkActor(mapper=mapper)
        actor.GetProperty().SetColor(0, 1, 0)
        actor.property.opacity = 1

        return actor

class PatientContext(qtc.QObject):
    patient_id_changed = qtc.Signal(str)
    patient_first_name_changed = qtc.Signal(str)
    patient_last_name_changed = qtc.Signal(str)
    plans_updated = qtc.Signal(dict)
    current_plan_changed = qtc.Signal(DicomPlanContext)

    def __init__(self):
        super().__init__()

        self._patient_id = None         # str
        self._first_name = None         # str
        self._last_name = None          # str
        self._plans = {}                # PlanContext.plan_id: PlanContext
        self._current_plan = None       # PlanContext

    @property
    def patient_id(self):
        return self._patient_id

    @patient_id.setter
    def patient_id(self, value):
        self._patient_id = str(value)
        self.patient_id_changed.emit(self._patient_id)

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        self._first_name = str(value)
        self.patient_first_name_changed.emit(self._first_name)

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        self._last_name = str(value)
        self.patient_last_name_changed.emit(self._last_name)

    @property
    def plans(self):
        return self._plans

    @property
    def current_plan(self):
        return self._current_plan

    def update_current_plan(self, plan_id):
        if plan_id in self._plans:
            self._current_plan = self._plans[plan_id]
            self.current_plan_changed.emit(self._current_plan)
        else:
            pass

    def load_context_from_dicom_rt_file(self, file_path):
        ds = pydicom.dcmread(file_path)
        if ds.file_meta.MediaStorageSOPClassUID == RTPlanStorage:
            # Patient Data
            self._patient_id = ds.PatientID

            name = str(ds.PatientName).split('^')
            if len(name) == 1:
                self._first_name, = name
            elif len(name) == 2:
                self._last_name, self._first_name = name
            elif len(name) == 3:
                self._last_name = name[0]
                self._first_name = name[1]
            else:
                self._first_name = ds.PatientID

            # Plan Data
            _plan_id = ds.SeriesDescription
            _frame_of_reference_uid = ds.FrameOfReferenceUID
            _isocenter = None
            _orientation = None
            _beams = []

            # Get Orientation from PatientSetupSequence
            for i in range(len(ds.PatientSetupSequence)):
                orientation = ds.PatientSetupSequence[i].PatientPosition

                if (_orientation is None) or (i == 0):
                    _orientation = orientation
                elif _orientation != orientation:
                    print("There are multiple patient orientations reported in the DICOM Plan")
                else:
                    pass

            # Get beams and isocenter
            for beam in ds.BeamSequence:
                _status = ''
                _num = str(beam.BeamNumber)
                _id = str(beam.BeamName)

                vms_name = beam.get((0x3243, 0x1009), None)
                _name = '' if vms_name is None else vms_name.value.decode('utf-8')

                _type = beam.TreatmentDeliveryType

                first_cp = beam.ControlPointSequence[0]

                _isocenter = np.array(first_cp.IsocenterPosition, dtype=float).round(2)
                _gantry_start = _gantry_stop = str(first_cp.GantryAngle)
                _gantry_rot_direction = str(first_cp.GantryRotationDirection)
                _couch = str(first_cp.PatientSupportAngle)

                last_cp = beam.ControlPointSequence[-1]
                if hasattr(last_cp, 'GantryAngle'):
                    _gantry_stop = str(last_cp.GantryAngle)

                _beams.append([_status,
                               _num,
                               _id,
                               _name,
                               _couch,
                               _gantry_start,
                               _gantry_stop,
                               _gantry_rot_direction,
                               _type
                               ]
                              )
            plan = DicomPlanContext(_plan_id,
                                    _isocenter.tolist(),
                                    _orientation,
                                    _beams,
                                    ref_frame=_frame_of_reference_uid
                                    )

            self._plans[plan.plan_id] = plan
        else:
            raise DicomFileValidationError(f"{file_path} is not a valid DICOM RT Plan file.")


class DicomRTPlan(qtc.QObject):

    file_path_changed = qtc.Signal(str)
    invalid_file_loaded = qtc.Signal(str)
    plan_model_updated = qtc.Signal(qtc.QObject)

    def __init__(self):
        super().__init__()
        self._filepath = None

        self._patient_id = None
        self._patient_first_name = None
        self._patient_last_name = None
        self._patient_orientation = None
        self._plan_id = None
        self._isocenter = None
        self._frame_of_reference_uid = None
        self._beams = []

        self._structure_set = DicomRTStructureSet(self)

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
    def isocenter(self):
        return self._isocenter

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

                self._isocenter = np.array(first_cp.IsocenterPosition, dtype=float).round(2)
                _gantry_start = _gantry_stop = str(first_cp.GantryAngle)
                _gantry_rot_direction = str(first_cp.GantryRotationDirection)
                _couch = str(first_cp.PatientSupportAngle)

                last_cp = beam.ControlPointSequence[-1]
                if hasattr(last_cp, 'GantryAngle'):
                    _gantry_stop = str(last_cp.GantryAngle)

                self.beams.append([_status,
                                   _num,
                                   _id,
                                   _name,
                                   _couch,
                                   _gantry_start,
                                   _gantry_stop,
                                   _gantry_rot_direction,
                                   _type
                                   ]
                                  )

            self.plan_model_updated.emit(self)
        else:
            self.invalid_file_loaded.emit(f"{new_path} is not a valid DICOM RT Plan file.")
            raise DicomFileValidationError("Not a valid DICOM RT Plan file.")

class DicomRTStructureSet(qtc.QObject):

    file_path_changed = qtc.Signal(str)
    invalid_file_loaded = qtc.Signal(str)
    structures_loaded = qtc.Signal(qtc.QObject)
    # structure_model_updated = qtc.Signal()
    vtk_actor_updated = qtc.Signal(qtc.QObject)

    def __init__(self, parent):
        super().__init__()
        self._parent = parent
        self._filepath = None
        self._dataset = None

        self._patinet_id = None
        self._structure_points = {}
        self._structure_meshes = {}
        self._frame_of_reference_uid = None

    @property
    def filepath(self):
        return self._filepath

    @filepath.setter
    def filepath(self, new_path):
        if new_path != self._filepath:
            self.update_filepath(new_path)

    @property
    def structures(self):
        return self._structure_points.keys()

    def _get_structure_point_clouds(self):
        # Read DICOM Structure Set
        self.ds = dataset = pydicom.dcmread(self.filepath)

        # Generate ROI Look Up Table using the ROI Number as the key
        roi_lut = {}
        for structure in dataset.StructureSetROISequence:
            # print(f'{structure.ROIName} ({structure.ROIName.lower()})',
            #       structure.ROINumber
            #       )
            roi_lut[structure.ROINumber] = structure.ROIName.lower()

        # Grab the Body structure points
        contours = []
        for roi in dataset.ROIContourSequence:
            # if (roi.ReferencedROINumber in roi_lut) and \
            #         roi_lut[roi.ReferencedROINumber] == 'body':
            #     # print('Found Body')
            contours = []
            if hasattr(roi, "ContourSequence"):
                print(roi_lut[roi.ReferencedROINumber])
                for contour in roi.ContourSequence:
                    contours.append([[float(contour.ContourData[i]),
                                      float(contour.ContourData[i + 1]),
                                      float(contour.ContourData[i + 2])
                                      ] for i in range(0,
                                                       len(contour.ContourData),
                                                       3
                                                       )
                                     ]
                                    )

                dcm_points = np.array([point for contour in contours for point in contour])

                dcm_pcloud = o3d.geometry.PointCloud()
                dcm_pcloud.points = o3d.utility.Vector3dVector(dcm_points)
                dcm_pcloud.estimate_normals()

                self._structure_points[roi_lut[roi.ReferencedROINumber]] = dcm_pcloud

        print(self.structures)
        self.structures_loaded.emit(self)

    def _pcloud_to_mesh(self, pcd, voxel_size=3, iso_level_percentile=5):
        # Convet Open3D point cloud to numpy array
        points = np.asarray(pcd.points)

        # Compute the bounds of the point cloud
        mins = pcd.get_min_bound()
        maxs = pcd.get_max_bound()

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

    def get_body_mesh(self, structure):
        if structure in self._structure_meshes:
            print("Using cashed mesh")
            self._generate_visual_mesh(self._structure_meshes[structure])
        else:
            print("Generating DICOM surface using marching cubes.")
            mesh = self._pcloud_to_mesh(self._structure_points[structure], voxel_size=3, iso_level_percentile=3)
            print('DICOM Surface complete')
            self._structure_meshes[structure] = mesh
            self._generate_visual_mesh(mesh)

    def _generate_visual_mesh(self, dcm_mesh):
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

        self.vtk_actor_updated.emit(self)

    # qtc.Slot(str)
    def update_filepath(self, new_path):
        dataset = dcmread(new_path)

        if dataset.file_meta.MediaStorageSOPClassUID == RTStructureSetStorage:
            if dataset.FrameOfReferenceUID == self._parent.frame_of_reference_uid:
                self._filepath = new_path
                self.file_path_changed.emit(self.filepath)

                print('Reading in DICOM structures from DICOM file')
                self._get_structure_point_clouds()
            else:
                self.invalid_file_loaded.emit(f"{new_path} dose not match the loaded DICOM RT Plan.")
        else:
            self.invalid_file_loaded.emit(f"{new_path} is not a valid DICOM RT Structure Set file.")


if __name__ == '__main__':

    def print_struct(struct):
        print(struct)

    plan_file = r"C:\__python__\Projects\MapApp\data\ESAPI_Testing\RP.1.2.246.352.71.5.206203234488.43856.20250402093313.dcm"
    ss_file = r"C:\__python__\Projects\MapApp\data\ESAPI_Testing\RS.1.2.246.352.71.4.206203234488.21666.20250402094226.dcm"

    pt = PatientContext()
    pt.load_context_from_dicom_rt_file(plan_file)

    print(pt.patient_id)
    print(pt.first_name)
    print(pt.last_name)
    print(pt.plans)
    for plan_id, plan in pt.plans.items():
        plan.current_structure_changed.connect(print_struct)
        print(plan.plan_id)
        print(plan.frame_of_reference_uid)
        print(plan.isocenter)
        print(plan.patient_orientation)
        for beam in plan.beams:
            print(beam)
        plan.load_structures_from_dicom_rt_file(ss_file)
        print(plan.structures)
        plan.update_current_structure('body')
        plan.update_current_structure('ptv')
        plan.update_current_structure('body')
    print(pt.current_plan)