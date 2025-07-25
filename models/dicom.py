import json
import logging

import numpy as np
from skimage.draw import polygon

import pydicom
from pydicom.uid import RTPlanStorage, RTStructureSetStorage

import vtk
from vtkmodules.util.numpy_support import numpy_to_vtk

from models.settings import app_settings

import PySide6.QtCore as qtc
import pyqtgraph as pg

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
    status_bar_coms = qtc.Signal(str)
    status_bar_clear = qtc.Signal()
    progress_coms = qtc.Signal(int)

    def __init__(self, plan_id='', ref_frame='', isocenter=[], orientation='', beams=[]):
        self.logger = logging.getLogger('MapApp.models.dicom.DicomPlanContext')
        self.logger.debug("Initializing DicomPlanContext objects attributes")
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
        self.logger.debug(f"Setting DicomPlanContext plan_id using '{value}'")
        self._plan_id = str(value)
        self.plan_id_changed.emit(self._plan_id)

    @property
    def frame_of_reference_uid(self):
        return self._frame_of_reference_uid

    @frame_of_reference_uid.setter
    def frame_of_reference_uid(self, value):
        self.logger.debug(f"Setting DicomPlanContext frame_of_reference_uid using '{value}'")
        self._frame_of_reference_uid = str(value)
        self.frame_of_reference_uid_changed.emit(self._frame_of_reference_uid)

    @property
    def isocenter(self):
        return self._isocenter

    @isocenter.setter
    def isocenter(self, iter):
        self.logger.debug(f"Setting DicomPlanContext isocenter using {iter}")
        self._isocenter = [float(i) for i in iter]
        self.isocenter_changed.emit(self._isocenter)

    @property
    def patient_orientation(self):
        return self._patient_orientation

    @patient_orientation.setter
    def patient_orientation(self, value):
        self.logger.debug(f"Setting DicomPlanContext patient_orientation using '{value}'")
        self._patient_orientation = str(value)
        self.patient_orientation_changed.emit(self._patient_orientation)

    @property
    def beams(self):
        return self._beams

    @beams.setter
    def beams(self, iter):
        self.logger.debug(f"Setting DicomPlanContext beams using {iter}")
        self._beams = iter
        self.beams_changed.emit(self._beams)

    @property
    def structures(self):
        return [key for key in self._structures.keys()]

    @property
    def current_structure(self):
        return self._current_structure

    def update_values(self, plan_ctx):
        self.logger.debug(f"Updating DicomPlanContext using another DicomPlanContext object")
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
        self.logger.debug(f"Updating the current structure using it's 'id' in the DicomPlanContext")
        if structure_id in self._structures:
            if self._structures[structure_id] is not None:
                self.logger.info(f"Structure with id = '{structure_id}' found in the DicomPlanContext using cached structure")
                self._current_structure = self._structures[structure_id]
                self.current_structure_changed.emit(self.current_structure)
            else:
                self.logger.info(f"Structure with id = '{structure_id}' not found in the DicomPlanContext - Generating new DICOM surface using marching cubes")
                # mesh = self._pcloud_to_mesh(self._raw_structure_points[structure_id], voxel_size=3, iso_level_percentile=3)
                mesh = self._pcloud_to_mesh(self._raw_structure_points[structure_id])
                self.logger.info(f"Structure with id = '{structure_id}' surface generation completed")
                self.logger.info(f"Structure with id = '{structure_id}' surface added to the DicomPlanContext")
                self._structures[structure_id] = self._generate_visual_mesh(mesh)
                self._current_structure = self._structures[structure_id]
                self.current_structure_changed.emit(self.current_structure)
        else:
            self.logger.info(f"No structure with the id '{structure_id}' found in the DicomPlanContext")
            self._current_structure = None

    def load_structures_from_dicom_rt_file(self, file_path):
        self.logger.debug(f"Loading DICOM RT structures from file into the DicomPlanContext")
        ds = pydicom.dcmread(file_path)

        if ds.file_meta.MediaStorageSOPClassUID == RTStructureSetStorage:
            if ds.FrameOfReferenceUID == self.frame_of_reference_uid:
                self.logger.debug('Reading in DICOM structures from DICOM file')
                self._get_structure_point_clouds(ds)
            else:
                # This is logged in the main app
                self.invalid_file_loaded.emit(f"{file_path} dose not match the loaded DICOM RT Plan.")
                raise DicomFileValidationError(f"{file_path} dose not match the loaded DICOM RT Plan.")
        else:
            # This is logged in the main app
            self.status_bar_clear.emit()
            self.progress_coms.emit(0)
            self.invalid_file_loaded.emit(f"{file_path} is not a valid DICOM RT Structure Set file.")
            raise DicomFileValidationError(f"{file_path} is not a valid DICOM RT Structure Set file.")

    def validate_beams(self, map_data):
        self.logger.debug(f"Validating all beams in the DicomPlanContext using MapRT collision map")

        arc_check_resolution = app_settings.dicom.arc_check_resolution
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
            _status, _num, _id, _name, _couch, _gantry_start, _gantry_stop, _gantry_rot_direction, _type = beam

            if _gantry_rot_direction == 'NONE':

                g_start_idx = y_map[str(round(float(_gantry_start)))]
                c_pos_idx = x_map[str(round(float(_couch)))]
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

                        beam_plot = pg.PlotCurveItem(x=[c_pos_idx, c_pos_idx], y=[0, len(j_idx)-1])
                        beam_plot.setPen(pg.mkPen(color='y', width=4))
                        arc_plots.append(beam_plot)

                    elif g_start_idx == 0 and g_stop_idx > 0:
                        is_ok_180 = np.all(collision_map.image[0, c_pos_idx])
                        g_start_idx = len(j_idx) - 1

                        is_ok_rest = np.all(
                            collision_map.image[g_start_idx:g_stop_idx:-arc_check_resolution, c_pos_idx])

                        is_ok = is_ok_180 and is_ok_rest
                        beam[0] = True if is_ok else False

                        beam_plot = pg.PlotCurveItem(x=[c_pos_idx, c_pos_idx], y=[g_start_idx, g_stop_idx])
                        beam_plot.setPen(pg.mkPen(color='y', width=4))
                        arc_plots.append(beam_plot)

                    else:
                        is_ok = np.all(collision_map.image[g_start_idx:g_stop_idx:-arc_check_resolution, c_pos_idx])
                        beam[0] = True if is_ok else False

                        beam_plot = pg.PlotCurveItem(x=[c_pos_idx, c_pos_idx], y=[g_start_idx, g_stop_idx])
                        beam_plot.setPen(pg.mkPen(color='y', width=4))
                        arc_plots.append(beam_plot)

                else:
                    if g_start_idx == 0 and g_stop_idx == 0:
                        is_ok = np.all(collision_map.image[::,c_pos_idx])
                        beam[0] = True if is_ok else False

                        beam_plot = pg.PlotCurveItem(x=[c_pos_idx, c_pos_idx], y=[0, len(j_idx) - 1])
                        beam_plot.setPen(pg.mkPen(color='y', width=4))
                        arc_plots.append(beam_plot)

                    elif g_start_idx >= 0 and g_stop_idx > 0:
                        is_ok = np.all(collision_map.image[g_start_idx:g_stop_idx:arc_check_resolution, c_pos_idx])
                        beam[0] = True if is_ok else False

                        beam_plot = pg.PlotCurveItem(x=[c_pos_idx, c_pos_idx], y=[g_start_idx, g_stop_idx])
                        beam_plot.setPen(pg.mkPen(color='y', width=4))
                        arc_plots.append(beam_plot)

        self.beams_changed.emit(self._beams)
        self.redraw_beams.emit((arc_plots, static_plots))

    def _get_contour_orientation(self, points):
        """
            Determines if a sequence of 3D coplanar points forming a closed loop is clockwise or counter-clockwise.

            Args:
                points: A list of tuples or lists, where each inner element represents
                        a point (x, y). The points should be ordered sequentially
                        along the perimeter of the loop.

            Returns:
                "CCW" if the points are ordered counter-clockwise.
                "CW" if the points are ordered clockwise.
                "CL" if the points are effectively collinear (signed area is close to zero).
        """
        n = len(points)
        if n < 3:
            raise Exception("Not a polygon (requires at least 3 points)")

        signed_area = 0.0
        for i in range(n):
            x1, y1, z1 = points[i]
            x2, y2, z2 = points[(i + 1) % n]  # Connects last point to first
            signed_area += (x1 * y2 - x2 * y1)

        # A small tolerance for floating-point comparisons
        if signed_area > 1e-9:
            return "CCW"
        elif signed_area < -1e-9:
            return "CW"
        else:
            return "CL"  # Or effectively collinear/degenerate

    def _get_structure_point_clouds(self, ds):
        self.logger.debug(f"Generating point clouds from DICOM structure points in DicomPlanContext")

        contours_to_keep = app_settings.dicom.contours_to_keep

        self.status_bar_coms.emit("Loading DICOM RT Structures from file")
        progress_inc = int(100 / len(ds.StructureSetROISequence))
        progress = 0

        # Generate ROI Look Up Table using the ROI Number as the key
        roi_lut = {}
        for structure in ds.StructureSetROISequence:
            roi_lut[structure.ROINumber] = structure.ROIName.lower()

        # Grab the Body structure points
        for roi in ds.ROIContourSequence:
            progress += progress_inc
            self.progress_coms.emit(progress)
            contours = []
            if hasattr(roi, "ContourSequence"):
                for contour in roi.ContourSequence:
                    if contour.ContourGeometricType != 'CLOSED_PLANAR':
                        continue

                    points = np.array(contour.ContourData).reshape((-1, 3))
                    z = float(round(points[0][2], 2))
                    points[:, 2] = z

                    if (contours_to_keep == 'ALL') or (self._get_contour_orientation(points) == contours_to_keep):
                        contours.append(points)

                self._raw_structure_points[roi_lut[roi.ReferencedROINumber]] = contours
                self._structures[roi_lut[roi.ReferencedROINumber]] = None

        self.progress_coms.emit(100)
        self.progress_coms.emit(0)
        self.status_bar_clear.emit()
        self.structures_updated.emit(self.structures)

    def _numpy3d_to_vtk_image(self, _3darray, origin, spacing):
        self.logger.debug(f"Generating vtkImageData from 3D numpy array")
        """
        Convert binary 3D NumPy volume to VTK surface mesh using Marching Cubes.
        """
        # Convert NumPy array to VTK array
        # flat_data_array = volume.ravel(order='F')  # For VTK's column-major order
        flat_data_array = _3darray.ravel()  # For VTK's column-major order
        vtk_data_array = numpy_to_vtk(num_array=flat_data_array, deep=True, array_type=vtk.VTK_FLOAT)

        # Create vtkImageData
        image_data = vtk.vtkImageData()
        image_data.SetDimensions(_3darray.shape[2], _3darray.shape[1], _3darray.shape[0])  # (x, y, z)
        image_data.SetSpacing(spacing)
        image_data.SetOrigin(origin[0], origin[1], origin[2])  # Optionally set origin

        # Attach data
        image_data.GetPointData().SetScalars(vtk_data_array)

        return image_data

    def _zero_crossing_isosurface(self, structure_contours):
        self.logger.debug(f"Extracting zero-crossing isosurface to generate surface mesh from structure point cloud in DicomPlanContext")
        structure_points = np.vstack(structure_contours)

        # Construct VTK PolyData object from structure points
        polydata = vtk.vtkPolyData()
        polydata.points = numpy_to_vtk(structure_points)

        # Grab the bounding coordinates for the contour points in DICOM orientation
        x_min, x_max, y_min, y_max, z_min, z_max = polydata.GetBounds()
        bounds_min = np.array([x_min, y_min, z_min])
        bounds_max = np.array([x_max, y_max, z_max])

        # Compute the extents of the point cloud data
        extents = bounds_max - bounds_min

        sample_size = int(polydata.GetNumberOfPoints() * 0.00005)
        if sample_size < 10:
            sample_size = 10

        # Do we need to estimate normals?
        distance = vtk.vtkSignedDistance()

        #  --- Compute Signed distance 3D Image ---
        #
        # The vtkSignedDistance class uses the following key methods:
        #
        # SetInputData(vtkPolyData)	- Input point cloud (must be vtkPolyData)
        # SetRadius(float)	- Influence radius for distance computation
        # SetBounds((xmin, xmax, ymin, ymax, zmin, zmax)) - Spatial domain for output grid
        # SetDimensions(nx, ny, nz) - Output grid resolution
        # SetAdjustBounds(True/False) - Automatically pad bounds slightly
        # SetBoundaryModeToClosestSurface() - Choose how signed distance is computed at the edges
        # SetPoints(vtkPoints) - Use if setting raw points instead of polydata
        # SetNormals(vtkDataArray) - Optionally provide oriented normals

        dimensions = 255
        radius = (max(extents[:-1]) / dimensions) * 3.0  # ~4 voxels

        distance.SetRadius(radius)
        distance.SetDimensions(dimensions, dimensions, dimensions)
        distance.SetBounds(x_min - extents[0] * 0.1, x_max + extents[0] * 0.1,
                           y_min - extents[1] * 0.1, y_max + extents[1] * 0.1,
                           z_min - extents[2] * 0.1, z_max + extents[2] * 0.1)

        #  --- Estimate Normals for the Signed Distance---
        #
        # vtk.vtkPCANormalEstimation()
        #
        # SetInputData(vtkPolyData)	–	Input point cloud or mesh (vtkPolyData)
        # SetSampleSize(int) - Number of nearest neighbors to use for PCA (typically 10–50)
        # SetNormalOrientationToGraphTraversal() – Default. Tries to orient normals consistently using a spanning tree
        # SetNormalOrientationToNone() – Disables automatic orientation (normals may be inconsistent)
        # SetNormalOrientationToPoint(), SetOrientationPoint(x, y, z) - Orients all normals to face toward or away from a fixed point
        # FlipNormalsOn() / FlipNormalsOff() - Invert the computed normals
        # GetOutput() - Returns vtkPolyData	new point cloud with Normals array in GetPointData()

        normals = None
        if polydata.point_data.normals:
            distance.SetInputData(polydata)
        else:
            normals = vtk.vtkPCANormalEstimation()
            normals.SetInputData(polydata)
            normals.SetSampleSize(sample_size)
            normals.FlipNormalsOn()
            normals.SetNormalOrientationToGraphTraversal()
            normals >> distance

        #  --- Construct the surface ---
        #
        # vtkExtractSurface Parameters
        #
        # SetInputData(vtkPolyData)	– Input point cloud with normals
        # SetRadius(float) - Radius to search for neighboring points; influences surface smoothness/detail
        # SetSampleSpacing(float) - Grid resolution (spacing); lower values → higher detail, more compute
        # SetSmoothingIterations(int) - Number of Laplacian smoothing passes after surface is generated
        # SetHoleFilling(bool) - Fill small topological holes in the output mesh
        # SetNormalWeighting(bool) - Use normals to guide the surface orientation (improves quality if normals are reliable)
        # SetOutputNormals(bool) - Whether to compute and output normals on the resulting mesh
        # GetOutput() - Returns the reconstructed surface (vtkPolyData)

        surface = vtk.vtkExtractSurface()
        surface.SetRadius(radius * 0.99)
        surface.SetHoleFilling(True)
        distance >> surface
        surface.Update()

        return surface.GetOutput()

    def _marching_cubes_isosurface(self, structure_contours):
        self.logger.debug(f"Using marching cubes to generate surface mesh from structure point cloud in DicomPlanContext")

        x_spacing = app_settings.dicom.pixel_spacing_x
        y_spacing = app_settings.dicom.pixel_spacing_y

        structure_points = np.vstack(structure_contours)

        z_diffs = structure_points[::, -1][1:] - structure_points[::, -1][0:-1]
        z_spacing = np.round(z_diffs[np.where(z_diffs != 0)], 2)
        if np.all((z_spacing - z_spacing[0]) == 0):
            z_spacing = z_spacing[0]

        voxel_size = np.array([x_spacing, y_spacing, z_spacing])

        # Construct VTK PolyData object from structure points
        polydata = vtk.vtkPolyData()
        polydata.points = numpy_to_vtk(structure_points)

        # Grab the bounding coordinates for the contour points in DICOM orientation
        x_min, x_max, y_min, y_max, z_min, z_max = polydata.GetBounds()
        bounds_min = np.array([x_min, y_min, z_min]) - (2.0 * voxel_size)
        bounds_max = np.array([x_max, y_max, z_max]) + (2.0 * voxel_size)

        # COmpute the extents of the point cloud data
        extents = bounds_max - bounds_min

        # Calculate grid dimensions
        dimensions = np.ceil((bounds_max - bounds_min) / voxel_size).astype(int)

        # Construct the Pixel to Coordinate transform matrix
        pixel_to_coord = np.eye(4, dtype=np.float64)
        pixel_to_coord[0:3, 0:3] *= voxel_size.reshape((-1, 3))
        pixel_to_coord[0, -1] = bounds_min[0]
        pixel_to_coord[1, -1] = bounds_min[1]
        pixel_to_coord[2, -1] = bounds_min[2]
        pixel_to_coord[3, -1] = 1

        # Take the inverse to get the Coordinate to Pixel index transform used to find the grid values
        coord_to_pixel = np.linalg.inv(pixel_to_coord)

        # Initialize an empty NumPy array with the calculated dimensions
        pixel_data = np.zeros(dimensions[::-1], dtype=np.uint16)

        for contour in structure_contours:
            # Convert the point coords to pixel indexes
            affine_coords = np.vstack((contour.T, np.ones(len(contour))))
            pixel_idxs = np.floor(coord_to_pixel @ affine_coords).astype(int)
            i, j, k, _ = pixel_idxs

            rv, cv = polygon(j, i)

            pixel_data[k[0], rv, cv] = 1

        image_data = self._numpy3d_to_vtk_image(pixel_data, bounds_min, voxel_size)

        # Extract surface
        mc = vtk.vtkMarchingCubes()
        mc.SetInputData(image_data)
        mc.SetValue(0, 1)
        mc.Update()

        return mc.GetOutput()

    def _contour_isosurface(self, structure_contours):
        self.logger.debug(f"Using contour filter to generate isosurface mesh from structure point cloud in DicomPlanContext")

        x_spacing = app_settings.dicom.pixel_spacing_x
        y_spacing = app_settings.dicom.pixel_spacing_y

        structure_points = np.vstack(structure_contours)

        z_diffs = structure_points[::, -1][1:] - structure_points[::, -1][0:-1]
        z_spacing = np.round(z_diffs[np.where(z_diffs != 0)], 2)
        if np.all((z_spacing - z_spacing[0]) == 0):
            z_spacing = z_spacing[0]

        voxel_size = np.array([x_spacing, y_spacing, z_spacing])

        # Construct VTK PolyData object from structure points
        polydata = vtk.vtkPolyData()
        polydata.points = numpy_to_vtk(structure_points)

        # Grab the bounding coordinates for the contour points in DICOM orientation
        x_min, x_max, y_min, y_max, z_min, z_max = polydata.GetBounds()
        bounds_min = np.array([x_min, y_min, z_min]) - (2.0 * voxel_size)
        bounds_max = np.array([x_max, y_max, z_max]) + (2.0 * voxel_size)

        # COmpute the extents of the point cloud data
        extents = bounds_max - bounds_min

        # Calculate grid dimensions
        dimensions = np.ceil((bounds_max - bounds_min) / voxel_size).astype(int)

        # Construct the Pixel to Coordinate transform matrix
        pixel_to_coord = np.eye(4, dtype=np.float64)
        pixel_to_coord[0:3, 0:3] *= voxel_size.reshape((-1, 3))
        pixel_to_coord[0, -1] = bounds_min[0]
        pixel_to_coord[1, -1] = bounds_min[1]
        pixel_to_coord[2, -1] = bounds_min[2]
        pixel_to_coord[3, -1] = 1

        # Take the inverse to get the Coordinate to Pixel index transform used to find the grid values
        coord_to_pixel = np.linalg.inv(pixel_to_coord)

        # Initialize an empty NumPy array with the calculated dimensions
        pixel_data = np.zeros(dimensions[::-1], dtype=np.uint16)

        for contour in structure_contours:
            # Convert the point coords to pixel indexes
            affine_coords = np.vstack((contour.T, np.ones(len(contour))))
            pixel_idxs = np.floor(coord_to_pixel @ affine_coords).astype(int)
            i, j, k, _ = pixel_idxs

            rv, cv = polygon(j, i)

            pixel_data[k[0], rv, cv] = 1

        image_data = self._numpy3d_to_vtk_image(pixel_data, bounds_min, voxel_size)

        # Extract surface
        cf = vtk.vtkContourFilter()
        cf.SetInputData(image_data)
        cf.SetValue(0, 1)  # isovalue
        cf.Update()

        return cf.GetOutput()

    # def _pcloud_to_mesh(self, pcd, voxel_size=3, iso_level_percentile=5):
    def _pcloud_to_mesh(self, contours):
        self.logger.debug(f"Determining surface reconstruction method for point cloud in DicomPlanContext")

        recon_methods = {'Zero-Crossing': self._zero_crossing_isosurface,
                         'Marching Cubes': self._marching_cubes_isosurface,
                         'Contour Isosurface': self._contour_isosurface
                         }

        surface_recon_method = app_settings.dicom.surface_recon_method

        recon = recon_methods[surface_recon_method]
        mesh = recon(contours)
        return mesh

    def _generate_visual_mesh(self, mesh):
        self.logger.debug(f'Generating final surface mesh for visualization in DicomPlanContext')

        # Create a mapper and actor
        mapper = vtk.vtkPolyDataMapper()
        mapper.ScalarVisibilityOff()
        # polydata >> mapper
        mesh >> mapper

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
    status_bar_coms = qtc.Signal(str)
    status_bar_clear = qtc.Signal()
    progress_coms = qtc.Signal(int)

    def __init__(self):
        self.logger = logging.getLogger('MapApp.models.dicom.PatientContext')
        self.logger.debug(f'Initializing attributes for PatientContext object')
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
        self.logger.debug(f"Setting patient_id to '{value}' in PatientContext")
        self._patient_id = str(value)
        self.patient_id_changed.emit(self._patient_id)

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        self.logger.debug(f"Setting first_name to '{value}' in PatientContext")
        self._first_name = str(value)
        self.patient_first_name_changed.emit(self._first_name)

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        self.logger.debug(f"Setting last_name to '{value}' in PatientContext")
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
        self.logger.debug(f'Clearing attributes in PatientContext')
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
        self.logger.debug(f"Setting current_course to '{course_id}' in PatientContext")
        if course_id in self._courses:
            self._current_course = course_id
            self.logger.debug(f"Updating available plans for course id = '{course_id}' in PatientContext")
            self._plans = self._courses[course_id]
            self.plans_updated.emit(self.plans)
        else:
            pass

    def update_current_plan(self, plan_id):
        self.logger.debug(f"Setting current_plan to '{plan_id}' in PatientContext")
        if plan_id in self._plans:
            self._current_plan.update_values(self._plans[plan_id])
            self.current_plan_changed.emit(self._current_plan)

    def load_context_from_dicom_rt_file(self, file_path):
        self.logger.debug(f"Loading DICOM RT plan from file into the PatientContext")
        ds = pydicom.dcmread(file_path)

        # Update Progress
        progress = 0
        progress += 5 # 5
        self.progress_coms.emit(progress)

        self.logger.info(f"Checking for proper DICOM RT file format in PatientContext")
        self.status_bar_coms.emit("Generating new DicomPlanContext for DICOM RT Plan file")
        if ds.file_meta.MediaStorageSOPClassUID == RTPlanStorage:
            # Patient Data
            self.patient_id = ds.PatientID

            # Update Progress
            progress += 5  # 10
            self.progress_coms.emit(progress)

            name = str(ds.PatientName).split('^')
            print(name)
            if len(name) == 1:
                self.first_name, = name
            elif len(name) == 2:
                self.last_name, self.first_name = name
            elif len(name) == 3:
                self.last_name, self.first_name, _ = name
            else:
                self.first_name = ds.PatientID

            # Update Progress
            progress += 10 # 20
            self.progress_coms.emit(progress)

            # Plan Data
            self.logger.info(f"Generating new DicomPlanContext for DICOM RT plan file in PatientContext")
            plan = DicomPlanContext()
            plan.plan_id = ds.SeriesDescription
            plan.frame_of_reference_uid = ds.FrameOfReferenceUID

            # Update Progress
            progress += 5  # 25
            self.progress_coms.emit(progress)

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

            # Update Progress
            progress += 5  # 30
            self.progress_coms.emit(progress)

            # Get beams and isocenter
            _isocenter = None

            self.logger.info(f"Constructing Beams list from DICOM RT plan file in PatientContext")
            progress_inc = int((100 - progress) / len(ds.BeamSequence))
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

                if _type not in ('TRMT_PORTFILM', 'OPEN_PORTFILM'):
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

                # Update Progress
                progress += progress_inc
                self.progress_coms.emit(progress)

            plan.isocenter = _isocenter
            plan.beams = _beams
            plans = {plan.plan_id: plan}

            self._courses['F1'] = plans
            self.courses_updated.emit(self.courses)
            self.update_current_course('F1')
            self.update_current_plan(plan.plan_id)

            # Update Progress
            self.progress_coms.emit(100)
            self.progress_coms.emit(0)
            self.status_bar_clear.emit()
        else:
            # Logged in main application

            # Update Progress
            self.progress_coms.emit(0)
            self.status_bar_clear.emit()

            self.invalid_file_loaded.emit(f"{file_path} is not a valid DICOM RT Plan file.")
            raise DicomFileValidationError(f"{file_path} is not a valid DICOM RT Plan file.")

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