import json
import datetime as dt
import numpy as np
from skimage import measure
from scipy.spatial import cKDTree

import pydicom
from pydicom.dataset import Dataset, FileDataset
from pydicom.uid import ExplicitVRLittleEndian, CTImageStorage, RTPlanStorage, RTStructureSetStorage

# from pynetdicom.sop_class import RTPlanStorage, RTStructureSetStorage

import open3d as o3d

import vtk
from vtkmodules.util import numpy_support

from models.settings import AppSettings

import PySide6.QtCore as qtc
import pyqtgraph as pg

import logging
logger = logging.getLogger('MapApp')

class DicomFileValidationError(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)

class DicomPlanContext(qtc.QObject):
    plan_id_changed = qtc.Signal(str)
    frame_of_reference_uid_changed = qtc.Signal(str)
    isocenter_changed = qtc.Signal(list)
    patient_orientation_changed = qtc.Signal(str)
    beams_changed = qtc.Signal(list)
    redraw_beams = qtc.Signal(tuple)
    structures_updated = qtc.Signal(list)
    current_structure_changed = qtc.Signal(vtk.vtkActor)
    invalid_file_loaded = qtc.Signal(str)

    def __init__(self, plan_id='', ref_frame='', isocenter=[], orientation='', beams=[]):
        print('DicomPlanContext.__init__')
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

    @plan_id.setter
    def plan_id(self, value):
        print('DicomPlanContext.plan_id.setter')
        self._plan_id = str(value)
        self.plan_id_changed.emit(self._plan_id)

    @property
    def frame_of_reference_uid(self):
        return self._frame_of_reference_uid

    @frame_of_reference_uid.setter
    def frame_of_reference_uid(self, value):
        print('DicomPlanContext.frame_of_reference_uid.setter')
        self._frame_of_reference_uid = str(value)
        self.frame_of_reference_uid_changed.emit(self._frame_of_reference_uid)

    @property
    def isocenter(self):
        return self._isocenter

    @isocenter.setter
    def isocenter(self, iter):
        print('DicomPlanContext.isocenter.setter')
        self._isocenter = [float(i) for i in iter]
        self.isocenter_changed.emit(self._isocenter)

    @property
    def patient_orientation(self):
        return self._patient_orientation

    @patient_orientation.setter
    def patient_orientation(self, value):
        print('DicomPlanContext.patient_orientation.setter')
        self._patient_orientation = str(value)
        self.patient_orientation_changed.emit(self._patient_orientation)

    @property
    def beams(self):
        return self._beams

    @beams.setter
    def beams(self, iter):
        print('DicomPlanContext.beams.setter')
        self._beams = iter
        self.beams_changed.emit(self._beams)

    @property
    def structures(self):
        return [key for key in self._structures.keys()]

    @property
    def current_structure(self):
        return self._current_structure

    def update_values(self, plan_ctx):
        print('DicomPlanContext.update_values')
        if isinstance(plan_ctx, DicomPlanContext):
            self.plan_id = plan_ctx.plan_id
            self.frame_of_reference_uid = plan_ctx.frame_of_reference_uid
            self.isocenter = plan_ctx.isocenter
            self.patient_orientation = plan_ctx.patient_orientation
            self.beams = plan_ctx.beams

            self._raw_structure_points = plan_ctx._raw_structure_points
            self._structures = plan_ctx._structures
            self.structures_updated.emit(self.structures)
            self._current_structure = None

    def update_current_structure(self, structure_id):
        print('DicomPlanContext.update_current_structure')
        if structure_id in self._structures:
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
        else:
            self._current_structure = None

    def load_structures_from_dicom_rt_file(self, file_path):
        print('DicomPlanContext.load_structures_from_dicom_rt_file')
        ds = pydicom.dcmread(file_path)
        if ds.file_meta.MediaStorageSOPClassUID == RTStructureSetStorage:
            if ds.FrameOfReferenceUID == self.frame_of_reference_uid:
                print('Reading in DICOM structures from DICOM file')
                self._get_structure_point_clouds(ds)
            else:
                self.invalid_file_loaded.emit(f"{file_path} dose not match the loaded DICOM RT Plan.")
                raise DicomFileValidationError(f"{file_path} dose not match the loaded DICOM RT Plan.")
        else:
            self.invalid_file_loaded.emit(f"{file_path} is not a valid DICOM RT Structure Set file.")
            raise DicomFileValidationError(f"{file_path} is not a valid DICOM RT Structure Set file.")

    def validate_beams(self, map_data):
        print('DicomPlanContext.validate_beams')
        with open(r'.\settings.json', 'r') as settings:
            settings_data = json.load(settings)
            settings = AppSettings(**settings_data)

            arc_check_resolution = settings.dicom.arc_check_resolution

        collision_map, x_ticks, y_ticks = map_data

        # construct couch index positions for resampled map
        c0 = np.arange(270, 360, 1)
        c1 = np.arange(0, 91, 1)
        couch_values = np.hstack((c0, c1))
        i_idx = np.arange(len(couch_values))

        # construct gantry index positions for resampled map
        g0 = np.arange(180, 360, 1)
        g1 = np.arange(0, 180, 1)
        gantry_values = np.hstack((g0, g1))
        j_idx = np.arange(len(gantry_values))

        x_map = dict([(str(couch_values[x]), int(i_idx[x])) for x in range(len(i_idx))])
        y_map = dict([(str(gantry_values[y]), int(j_idx[y])) for y in range(len(j_idx))])

        arc_plots = []
        static_plots = []

        for beam in self.beams:
            print(beam)
            _status, _num, _id, _name, _couch, _gantry_start, _gantry_stop, _gantry_rot_direction, _type = beam

            if _gantry_rot_direction == 'NONE':

                g_start_idx = y_map[str(round(float(_gantry_start)))]
                c_pos_idx = x_map[_couch]
                is_ok = np.all(collision_map.image[g_start_idx, c_pos_idx])
                beam[0] = True if is_ok else False

                static_beam = pg.ScatterPlotItem(x=[c_pos_idx], y=[g_start_idx], symbol='o')
                if _type == 'SETUP':
                    static_beam.setPen(pg.mkPen(color='cyan', width=5))
                else:
                    static_beam.setPen(pg.mkPen(color='g', width=5))

                static_plots.append(static_beam)

            else:
                g_start_idx = y_map[str(round(float(_gantry_start)))]
                g_stop_idx = y_map[str(round(float(_gantry_stop)))]
                c_pos_idx = x_map[_couch]
                if _gantry_rot_direction == 'CC':
                    if g_start_idx == 0 and g_stop_idx == 0:

                        is_ok = np.all(collision_map.image[::,c_pos_idx])
                        beam[0] = True if is_ok else False

                        print(collision_map.image[::, c_pos_idx])
                        print(is_ok)

                        beam_plot = pg.PlotCurveItem(x=[c_pos_idx, c_pos_idx], y=[0, len(j_idx)-1])
                        beam_plot.setPen(pg.mkPen(color='y', width=4))
                        arc_plots.append(beam_plot)

                    elif g_start_idx == 0 and g_stop_idx > 0:
                        is_ok_180 = np.all(collision_map.image[0, c_pos_idx])
                        print(g_start_idx, g_stop_idx, c_pos_idx)
                        print(collision_map.image[0, c_pos_idx])
                        print(is_ok_180)
                        g_start_idx = len(j_idx) - 1

                        is_ok_rest = np.all(
                            collision_map.image[g_start_idx:g_stop_idx:-arc_check_resolution, c_pos_idx])

                        is_ok = is_ok_180 and is_ok_rest
                        beam[0] = True if is_ok else False

                        print(g_start_idx, g_stop_idx, c_pos_idx, -arc_check_resolution)
                        print(collision_map.image[g_start_idx:g_stop_idx:-arc_check_resolution, c_pos_idx])
                        print(is_ok)

                        beam_plot = pg.PlotCurveItem(x=[c_pos_idx, c_pos_idx], y=[g_start_idx, g_stop_idx])
                        beam_plot.setPen(pg.mkPen(color='y', width=4))
                        arc_plots.append(beam_plot)

                    else:
                        is_ok = np.all(collision_map.image[g_start_idx:g_stop_idx:-arc_check_resolution, c_pos_idx])
                        beam[0] = True if is_ok else False

                        print(g_start_idx, g_stop_idx, c_pos_idx, -arc_check_resolution)
                        print(collision_map.image[g_start_idx:g_stop_idx:-arc_check_resolution, c_pos_idx])
                        print(is_ok)

                        beam_plot = pg.PlotCurveItem(x=[c_pos_idx, c_pos_idx], y=[g_start_idx, g_stop_idx])
                        beam_plot.setPen(pg.mkPen(color='y', width=4))
                        arc_plots.append(beam_plot)

                else:
                    if g_start_idx == 0 and g_stop_idx == 0:
                        is_ok = np.all(collision_map.image[::,c_pos_idx])
                        beam[0] = True if is_ok else False

                        print(g_start_idx, g_stop_idx, c_pos_idx)
                        print(collision_map.image[::,c_pos_idx])
                        print(is_ok)

                        beam_plot = pg.PlotCurveItem(x=[c_pos_idx, c_pos_idx], y=[0, len(j_idx) - 1])
                        beam_plot.setPen(pg.mkPen(color='y', width=4))
                        arc_plots.append(beam_plot)

                    elif g_start_idx >= 0 and g_stop_idx > 0:
                        is_ok = np.all(collision_map.image[g_start_idx:g_stop_idx:arc_check_resolution, c_pos_idx])
                        beam[0] = True if is_ok else False

                        print(g_start_idx, g_stop_idx, c_pos_idx, arc_check_resolution)
                        print(collision_map.image[g_start_idx:g_stop_idx:arc_check_resolution, c_pos_idx])
                        print(is_ok)

                        beam_plot = pg.PlotCurveItem(x=[c_pos_idx, c_pos_idx], y=[g_start_idx, g_stop_idx])
                        beam_plot.setPen(pg.mkPen(color='y', width=4))
                        arc_plots.append(beam_plot)

        self.beams_changed.emit(self._beams)
        self.redraw_beams.emit((arc_plots, static_plots))

    def _get_structure_point_clouds(self, ds):
        print('DicomPlanContext._get_structure_point_clouds')
        # Generate ROI Look Up Table using the ROI Number as the key
        roi_lut = {}
        for structure in ds.StructureSetROISequence:
            roi_lut[structure.ROINumber] = structure.ROIName.lower()

        # Grab the Body structure points
        for roi in ds.ROIContourSequence:
            contours = []
            if hasattr(roi, "ContourSequence"):
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

        self.structures_updated.emit(self.structures)

    def _pcloud_to_mesh(self, pcd, voxel_size=3, iso_level_percentile=5):
        print('DicomPlanContext._pcloud_to_mesh')
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
        print('DicomPlanContext._generate_visual_mesh')
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
    courses_updated = qtc.Signal(list)
    plans_updated = qtc.Signal(list)
    current_plan_changed = qtc.Signal(DicomPlanContext)
    invalid_file_loaded = qtc.Signal(str)
    patient_context_cleared = qtc.Signal()


    def __init__(self):
        print('PatientContext.__init__')
        super().__init__()

        self._patient_id = ''                    # str
        self._first_name = ''                    # str
        self._last_name = ''                      # str
        self._courses = {}                          # {str: {str: PlanContext}}
        self._current_course = ''                 # str
        self._plans = {}                            # PlanContext.plan_id: PlanContext
        self._current_plan = DicomPlanContext()     # PlanContext

    @property
    def patient_id(self):
        return self._patient_id

    @patient_id.setter
    def patient_id(self, value):
        print('PatientContext.patient_id.setter')
        self._patient_id = str(value)
        self.patient_id_changed.emit(self._patient_id)

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        print('PatientContext.first_name.setter')
        self._first_name = str(value)
        self.patient_first_name_changed.emit(self._first_name)

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        print('PatientContext.last_name.setter')
        self._last_name = str(value)
        self.patient_last_name_changed.emit(self._last_name)

    @property
    def courses(self):
        return [key for key in self._courses.keys()]

    @property
    def current_course(self):
        return self._current_course

    @property
    def plans(self):
        return [key for key in self._plans.keys()]

    @property
    def current_plan(self):
        return self._current_plan

    def clear(self):
        print('PatientContext.clear')
        self.patient_id = ''
        self.first_name = ''
        self.last_name = ''
        self._courses = {}
        self.courses_updated.emit(self.courses)
        self._current_course = ''  # str
        self._plans = {}
        self.plans_updated.emit(self.plans)
        self._current_plan.update_values(DicomPlanContext())
        self.patient_context_cleared.emit()

    def update_current_course(self, course_id):
        print('PatientContext.update_current_course')
        if course_id in self._courses:
            self._current_course = course_id
            self._plans = self._courses[course_id]
            self.plans_updated.emit(self.plans)
        else:
            pass

    def update_current_plan(self, plan_id):
        print('PatientContext.update_current_plan')
        if plan_id in self._plans:
            self._current_plan.update_values(self._plans[plan_id])
            self.current_plan_changed.emit(self._current_plan)

    def load_context_from_dicom_rt_file(self, file_path):
        print('PatientContext.load_context_from_dicom_rt_file')
        ds = pydicom.dcmread(file_path)

        if ds.file_meta.MediaStorageSOPClassUID == RTPlanStorage:
            # Patient Data
            self.patient_id = ds.PatientID

            name = str(ds.PatientName).split('^')
            if len(name) == 1:
                self.first_name, = name
            elif len(name) == 2:
                self.last_name, self._first_name = name
            elif len(name) == 3:
                self.last_name = name[0]
                self.first_name = name[1]
            else:
                self.first_name = ds.PatientID

            # Plan Data
            plan = DicomPlanContext()
            plan.plan_id = ds.SeriesDescription
            plan.frame_of_reference_uid = ds.FrameOfReferenceUID

            # Get Orientation from PatientSetupSequence
            _orientation = None
            for i in range(len(ds.PatientSetupSequence)):
                orientation = ds.PatientSetupSequence[i].PatientPosition

                if (_orientation is None) or (i == 0):
                    _orientation = orientation
                elif _orientation != orientation:
                    print("There are multiple patient orientations reported in the DICOM Plan")
                else:
                    pass
            plan.patient_orientation = _orientation

            # Get beams and isocenter
            _isocenter = None
            _beams = []
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

            plan.isocenter = _isocenter
            plan.beams = _beams
            plans = {plan.plan_id: plan}

            self._courses['F1'] = plans
            self.courses_updated.emit(self.courses)
            self.update_current_course('F1')
            self.update_current_plan(plan.plan_id)
        else:
            self.invalid_file_loaded.emit(f"{file_path} is not a valid DICOM RT Plan file.")
            raise DicomFileValidationError(f"{file_path} is not a valid DICOM RT Plan file.")

def convert_3d_surface_to_ct_data(patient_ctx, actor):
    dt_object = dt.datetime.now()

    # Create a new DICOM dataset
    file_meta = Dataset()
    file_meta.MediaStorageSOPClassUID = CTImageStorage
    file_meta.MediaStorageSOPInstanceUID = pydicom.uid.generate_uid()
    file_meta.TransferSyntaxUID = ExplicitVRLittleEndian

    ds = FileDataset('dummy.dcm', {}, file_meta=file_meta, preamble=b"\0" * 128)

    # Add the required attributes for a CT image
    ds.Modality = 'CT'
    ds.ContentDate = dt_object.strftime("%Y%m%d")
    ds.ContentTime = dt_object.strftime()
    ds.StudyInstanceUID = pydicom.uid.generate_uid()
    ds.SeriesInstanceUID = pydicom.uid.generate_uid()
    ds.SOPInstanceUID = pydicom.uid.generate_uid()
    ds.SOPClassUID = CTImageStorage
    ds.PatientName = f"{patient_ctx.last_name}^{patient_ctx.first_name}"
    ds.PatientID = patient_ctx.patient_id
    ds.StudyID = '1'
    ds.SeriesNumber = '1'
    ds.InstanceNumber = '1'
    ds.ImagePositionPatient = [0, 0, 0]
    ds.ImageOrientationPatient = [1, 0, 0, 0, 1, 0]
    ds.PixelSpacing = [1, 1]
    ds.SliceThickness = 1
    ds.KVP = 120
    ds.XRayTubeCurrent = 100
    ds.Rows = 512
    ds.Columns = 512
    ds.BitsAllocated = 16
    ds.BitsStored = 16
    ds.HighBit = 15
    ds.PixelRepresentation = 0
    ds.RescaleIntercept = -1024
    ds.RescaleSlope = 1

    # Create dummy pixel data (replace with actual CT data)
    pixel_data = np.random.randint(-1024, 3071, size=(512, 512), dtype=np.int16)
    ds.PixelData = pixel_data.tobytes()

    # Save the DICOM file
    ds.save_as('ct_slice.dcm', write_like_original=False)


if __name__ == '__main__':

    def print_struct(struct):
        print(struct)

    plan_file = r"C:\tmp\map app data\ESAPI_Testing\RP.1.2.246.352.71.5.206203234488.43856.20250402093313.dcm"
    ss_file = r"C:\tmp\map app data\ESAPI_Testing\RS.1.2.246.352.71.4.206203234488.21666.20250402094226.dcm"

    pt = PatientContext()
    pt.load_context_from_dicom_rt_file(plan_file)

    print(pt.patient_id)
    print(pt.first_name)
    print(pt.last_name)
    print(pt.courses)
    print(pt.plans)
    pt.update_current_course('F1')
    print(pt.plans)
    pt.update_current_plan('FieldTypes')
    print(pt.current_plan)
    plan = pt.current_plan
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