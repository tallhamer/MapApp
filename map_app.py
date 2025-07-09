import os
import sys
import base64
import logging
import binascii
from pathlib import Path
import datetime as dt

import pydicom
from pydicom.dataset import Dataset, FileMetaDataset
from pydicom.uid import ExplicitVRLittleEndian, CTImageStorage

import numpy as np
from scipy.ndimage import gaussian_filter

import vtk
from vtkmodules.util.numpy_support import  vtk_to_numpy

import PySide6.QtCore as qtc
import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg
import pyqtgraph as pg

from ui.main_window import Ui_MainWindow
from ui.dlg_orient import OrientDialog
from ui.dlg_settings import SettingsDialog
from ui.dlg_maprt_patient import MapRTPatientDialog
from ui.dlg_dicom_files import DicomFileDialog
from ui.dlg_surface_export import SurfaceExportDialog
from models.maprt import MapRTAPIManager, MapRTContext
from models.dicom import PatientContext, DicomPlanContext, DicomFileValidationError
from models.settings import app_settings

import resource_rc

class MainWindow(qtw.QMainWindow, Ui_MainWindow):
    def __init__(self):
        self.logger = logging.getLogger('MapApp.map_app.MainWindow')

        self.logger.debug("Initializing the attributes of main application")
        super().__init__()

        self.setupUi(self)

        self.setWindowTitle("Map App")

        #TODO: Only turn on for DEMO purposes
        self.w_le_patinet_id.setEchoMode(qtw.QLineEdit.Password)

        self.w_tw_patient_settings.setCurrentIndex(0)
        self.w_tw_visualizations.setCurrentIndex(1)

        self.dicom_file_mode = False
        self.maprt_file_mode = False

        self._setup_patient_context()

        self._setup_api_manager()

        self._setup_maprt_context()
        self._setup_collision_map_plot()
        self._setup_3d_visualization()

        self._construct_menu_actions()

        self._construct_status_bar_widgets()

    ####################################################################################
    # Setup                                                                            #
    ####################################################################################

    def _setup_patient_context(self):
        self.logger.debug("Setup master PatientContext object")

        #TODO: For demo purposes hide the MRN. Remove this later.
        # self.w_le_patinet_id.setEchoMode(qtw.QLineEdit.EchoMode.Password)

        self.w_pb_esapi_search.clicked.connect(self.ESAPI_STUB)

        # Setup the global PatientContext and PlanContext objects
        self.patient_ctx = PatientContext()

        # PatientContext specific Signals
        self.patient_ctx.patient_id_changed.connect(self.w_le_patinet_id.setText)
        self.patient_ctx.patient_first_name_changed.connect(self.w_l_patient_first_name.setText)
        self.patient_ctx.patient_last_name_changed.connect(self.w_l_patient_last_name.setText)
        self.patient_ctx.courses_updated.connect(self.ui_update_courses)
        self.patient_ctx.plans_updated.connect(self.ui_update_plans)
        self.patient_ctx.patient_context_cleared.connect(self.ui_clear_ui_components)

        # PatientContext.current_plan (PlanContext) specific Signals
        self.patient_ctx.current_plan.isocenter_changed.connect(self.ui_update_isocenter_label)
        self.patient_ctx.current_plan.beams_changed.connect(self.ui_update_beam_table)
        self.patient_ctx.current_plan.redraw_beams.connect(self.ui_update_beam_plots)
        self.patient_ctx.current_plan.structures_updated.connect(self.ui_update_structures)
        self.patient_ctx.current_plan.current_structure_changed.connect(self.update_3D_dicom_visualization)

        # ui to PatientContext or PlanContext method connections
        self.w_cb_body_structure.currentTextChanged.connect(self.patient_ctx.current_plan.update_current_structure)

    def _setup_api_manager(self):
        self.logger.debug("Setup master MapRT API Manager")

        # Setup the global MapRT API connection manager
        token = binascii.unhexlify(base64.b64decode(app_settings.maprt.api_token.encode('utf-8'))).decode('utf-8')
        self.maprt_api = MapRTAPIManager(app_settings.maprt.api_url,
                                         token,
                                         app_settings.maprt.api_user_agent
                                         )

        # Connect the ui signals to the MapRTAPIManager objects methods
        self.w_pb_fetch_api_data.clicked.connect(self.fetch_api_data)
        self.w_pb_get_map.clicked.connect(self.get_maprt_collision_maps)

    def _setup_maprt_context(self):
        self.logger.debug("Setup master MapRT Context object")
        # Setup the global MapRTContext object
        self.maprt_ctx = MapRTContext(self.maprt_api)

        # Connect the MapRTContext specific Signals to the ui
        self.maprt_ctx.api_status_changed.connect(self.w_l_api_status.setText)
        self.maprt_ctx.treatment_rooms_updated.connect(self.ui_update_maprt_treatment_rooms)
        self.maprt_ctx.patient_surfaces_updated.connect(self.ui_update_maprt_surfaces)
        self.maprt_ctx.collision_maps_updated.connect(self.ui_update_maprt_collision_maps)
        self.maprt_ctx.current_surface_changed.connect(self.ui_update_maprt_3D_surface_visualization)
        self.maprt_ctx.current_map_data_changed.connect(self.ui_update_collision_map_graphics_view)
        self.maprt_ctx.current_map_data_changed.connect(self.patient_ctx.current_plan.validate_beams)
        self.maprt_ctx.api_connection_error.connect(self.ui_notify_connection_error)

        # Connect the ui signals to the MapRTContext objects methods
        self.w_dsb_api_couch_buffer.valueChanged.connect(self.maprt_ctx.update_couch_buffer)
        self.w_dsb_api_patient_buffer.valueChanged.connect(self.maprt_ctx.update_patient_buffer)
        self.w_cb_current_map.currentTextChanged.connect(self.maprt_ctx.update_current_map_data)
        self.w_cb_surface_for_map.currentTextChanged.connect(self.maprt_ctx.update_surface)
        self.w_cb_treatment_room.currentTextChanged.connect(self.maprt_ctx.update_room)

        # Connect PatientContext to MapRTContext
        self.patient_ctx.current_plan_changed.connect(self.maprt_ctx.update_plan_context)
        self.patient_ctx.patient_context_cleared.connect(self.maprt_ctx.clear)

    def _setup_collision_map_plot(self):
        self.logger.debug("Setup MapRT collision map plotter")
        self.collision_map = None
        self.plotted_beams = None

        # Create a pyqtgraph plot
        self.collision_map_plot_widget = pg.PlotWidget()

        # Grab a reference for the ViewBox to use later when adding the collision_map array and tracking the mouse
        self.collision_map_view_box = self.collision_map_plot_widget.getViewBox()
        self.collision_map_view_box.setMouseEnabled(x=False, y=False)

        # Create crosshair lines that track the mouse while inthe view
        self.collision_map_v_line = pg.InfiniteLine(angle=90, movable=False)
        self.collision_map_v_line.setZValue(10)
        self.collision_map_h_line = pg.InfiniteLine(angle=0, movable=False)
        self.collision_map_v_line.setZValue(11)
        self.collision_map_view_box.addItem(self.collision_map_v_line, ignoreBounds=True)
        self.collision_map_view_box.addItem(self.collision_map_h_line, ignoreBounds=True)

        # Set the axis properties
        self.collision_map_plot_widget.showAxes(True)
        self.collision_map_plot_widget.invertY(True)

        # Set the global color scheme for the plot (match MapRT for now)
        self.collision_map_lut = np.array([[175, 15, 15], [41, 48, 66]], dtype=np.uint8)

        # Connect the Signals
        self.collision_map_view_box.scene().sigMouseMoved.connect(self.collision_map_mouse_moved)

        # Add plot to ui
        layout = qtw.QHBoxLayout(self.w_w_collision_map)
        layout.addWidget(self.collision_map_plot_widget)

    def _setup_3d_visualization(self):
        self.logger.debug("Setup VTK 3D visualization window")
        self.maprt_actor = None
        self.maprt_laser_actors = ()
        self.dicom_actor = None
        self.dicom_laser_actors = ()

        # 3D Scene Widget Setup
        self.vtk_renderer = vtk.vtkRenderer()
        self.vtk_render_window = self.vtk_widget.GetRenderWindow()
        self.vtk_render_window.AddRenderer(self.vtk_renderer)
        self.vtk_interactor = self.vtk_widget.GetRenderWindow().GetInteractor()
        self.vtk_interactor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())

        # Setup 3D scene color controls
        self.w_pb_background_color.clicked.connect(self.vtk_render_window_background_color_changed)
        self.w_fr_background_color.setStyleSheet(f"background-color: rgb({0}, {0}, {0});")
        self.w_fr_background_color.show()

        # Setup DICOM actor color controls
        self.w_pb_dcm_color.clicked.connect(self.dicom_surface_color_changed)
        self.w_fr_dcm_color.setStyleSheet(f"background-color: rgb({0}, {127}, {0});")
        self.w_fr_dcm_color.show()
        self.w_hs_dcm_opacity.valueChanged.connect(self.dicom_surface_opacity_changed)

        # Setup MapRT obj actor color controls
        self.w_pb_obj_color.clicked.connect(self.maprt_surface_color_changed)
        self.w_fr_obj_color.setStyleSheet(f"background-color: rgb({127}, {127}, {127});")
        self.w_fr_obj_color.show()
        self.w_hs_obj_opacity.valueChanged.connect(self.maprt_surface_opacity_changed)

        # Setup laser actor color controls
        self.w_pb_laser_color.clicked.connect(self.laser_color_changed)
        self.w_fr_laser_color.setStyleSheet(f"background-color: rgb({255}, {0}, {0});")
        self.w_fr_laser_color.show()
        self.w_hs_laser_opacity.valueChanged.connect(self.laser_opacity_changed)

        self.w_dsb_surface_shift_x.valueChanged.connect(self.ui_update_maprt_3D_surface_visualization)
        self.w_dsb_surface_shift_y.valueChanged.connect(self.ui_update_maprt_3D_surface_visualization)
        self.w_dsb_surface_shift_z.valueChanged.connect(self.ui_update_maprt_3D_surface_visualization)

        self.w_ch_axis_widget.checkStateChanged.connect(self.ui_visualize_axis_widget)
        self.w_ch_orientation_widget.checkStateChanged.connect(self.ui_visualize_cam_orientation_widget)

        # Connect view manipulation radiobuttons
        self.w_rb_plusX.toggled.connect(self.set_camera_to_plus_x)
        self.w_rb_minusX.toggled.connect(self.set_camera_to_minus_x)
        self.w_rb_plusY.toggled.connect(self.set_camera_to_plus_y)
        self.w_rb_minusY.toggled.connect(self.set_camera_to_minus_y)
        self.w_rb_plusZ.toggled.connect(self.set_camera_to_plus_z)
        self.w_rb_minusZ.toggled.connect(self.set_camera_to_minus_z)

        # Create axes actor
        axes_actor = vtk.vtkAxesActor()

        # Create axis orientation marker widget
        self.axis_widget = vtk.vtkOrientationMarkerWidget()
        self.axis_widget.SetOutlineColor(0.9300, 0.5700, 0.1300)
        self.axis_widget.SetOrientationMarker(axes_actor)
        self.axis_widget.SetInteractor(self.vtk_interactor)
        self.axis_widget.SetViewport(0.0, 0.0, 0.2, 0.2)  # Set size and position
        self.axis_widget.EnabledOn()
        self.axis_widget.InteractiveOff()

        # Create orientation manipulation widget
        self.cam_orient_manipulator = vtk.vtkCameraOrientationWidget(parent_renderer=self.vtk_renderer,
                                                                interactor=self.vtk_interactor)
        # Enable the widget.
        self.cam_orient_manipulator.EnabledOn()

        self.vtk_interactor.Initialize()
        self.vtk_widget.show()

    def _construct_menu_actions(self):
        self.logger.debug("Construct Main Menu Bar")
        menu_bar = self.menuBar()
        menu_file = menu_bar.addMenu("&File")

        action_clear_current_patient = qtg.QAction("&Clear Current Patient", self)
        action_clear_current_patient.triggered.connect(self.patient_ctx.clear)
        menu_file.addAction(action_clear_current_patient)

        menu_file.addSeparator()

        menu_open = menu_file.addMenu("&Open")

        action_open_dicom = qtg.QAction("&DICOM RT Files", self)
        action_open_dicom.triggered.connect(self.ui_open_dicom_files)
        menu_open.addAction(action_open_dicom)

        action_open_surface = qtg.QAction("Surface File", self)
        action_open_surface.triggered.connect(self.ui_select_maprt_surface_file)
        menu_open.addAction(action_open_surface)

        menu_save = menu_file.addMenu("&Save")

        action_3d_scene_to_image = qtg.QAction("&Render Window Image", self)
        action_3d_scene_to_image.triggered.connect(self.save_3d_image)
        menu_save.addAction(action_3d_scene_to_image)

        menu_export = menu_file.addMenu("&Export")

        action_export_surface_to_dicom = qtg.QAction("&MapRT Surface to DICOM", self)
        action_export_surface_to_dicom.triggered.connect(self.export_surface_to_dicom)
        menu_export.addAction(action_export_surface_to_dicom)

        menu_file.addSeparator()

        action_exit = qtg.QAction("E&xit", self)
        action_exit.triggered.connect(self.close)
        menu_file.addAction(action_exit)

        menu_options = menu_bar.addMenu("&Options")

        action_settings = qtg.QAction("&Settings", self)
        action_settings.triggered.connect(self.show_settings_dialog)
        menu_options.addAction(action_settings)

    def _construct_status_bar_widgets(self):
        self.logger.debug("Construct MainWindow Status Bar")
        self.status_bar = qtw.QStatusBar()
        self.setStatusBar(self.status_bar)
        self.statusBar().showMessage("Ready")

        self.progress_bar = qtw.QProgressBar()
        self.progress_bar.setAlignment(qtc.Qt.AlignmentFlag.AlignRight)
        self.progress_bar.setFixedWidth(200)
        self.status_bar.addPermanentWidget(self.progress_bar)
        self.progress_bar.setRange(0, 100)
        # self.progress_bar.setValue(50)

        # Connect models so that they can communicate with the MainWindow
        self.patient_ctx.status_bar_coms.connect(self.status_bar.showMessage)
        self.patient_ctx.status_bar_clear.connect(self.status_bar.clearMessage)
        self.patient_ctx.progress_coms.connect(self.progress_bar.setValue)

        self.patient_ctx.current_plan.status_bar_coms.connect(self.status_bar.showMessage)
        self.patient_ctx.current_plan.status_bar_clear.connect(self.status_bar.clearMessage)
        self.patient_ctx.current_plan.progress_coms.connect(self.progress_bar.setValue)

        self.maprt_api.status_bar_coms.connect(self.status_bar.showMessage)
        self.maprt_api.status_bar_clear.connect(self.status_bar.clearMessage)
        self.maprt_api.progress_coms.connect(self.progress_bar.setValue)

        self.maprt_ctx.status_bar_coms.connect(self.status_bar.showMessage)
        self.maprt_ctx.status_bar_clear.connect(self.status_bar.clearMessage)
        self.maprt_ctx.progress_coms.connect(self.progress_bar.setValue)



        status_bar_coms = qtc.Signal(str)
        progress_coms = qtc.Signal(int)

    ####################################################################################
    # PatientContext Connections and Methods                                           #
    ####################################################################################

    def ESAPI_STUB(self):
        self.logger.debug("MainWindow.ESAPI_STUB")

    def ui_open_dicom_files(self):
        self.logger.debug("Open DICOM RT files from MainWindow")
        dcm_diag = DicomFileDialog()
        if dcm_diag.exec():
            plan_path = dcm_diag.w_le_dicom_plan_path.text()
            self.logger.debug(f'Attempting to load Patient and plan information from file "{plan_path}"')
            if plan_path != '':
                try:
                    self.patient_ctx.clear()
                    self.ui_set_dicom_file_mode(True)
                    self.patient_ctx.load_context_from_dicom_rt_file(plan_path)
                    self.logger.info("DICOM RT Plan file successfully loaded")

                    struct_path = dcm_diag.w_le_dicom_structure_path.text()
                    self.logger.debug(f'Attempting to load structure information from file "{struct_path}"')
                    if struct_path != '':
                        self.patient_ctx.current_plan.load_structures_from_dicom_rt_file(struct_path)
                    self.logger.info("DICOM RT Structure Set file successfully loaded")

                except DicomFileValidationError as e:
                    self.logger.error(str(e))
                    self.patient_ctx.clear()
                    self.ui_set_dicom_file_mode(False)
                    self.ui_show_info_message(str(e))

                except Exception as e:
                    self.logger.error(str(e))
                    self.patient_ctx.clear()
                    self.ui_set_dicom_file_mode(False)
                    self.ui_show_info_message(str(e))
            else:
                self.logger.info("No DICOM RT Plan file selected. You must have a DICOM RT Plan at minimum.")
                self.ui_show_info_message("No DICOM RT Plan file selected. You must have a DICOM RT Plan at minimum.")

    def ui_update_courses(self, courses):
        self.logger.debug("Updating courses in MainWindow")
        if self.w_cb_course_id.count() == 0:
            self.w_cb_course_id.addItems(courses)
        else:
            current_selection = self.w_cb_course_id.currentText()
            if current_selection in courses:
                with qtc.QSignalBlocker(self.w_cb_course_id):
                    self.w_cb_course_id.clear()
                    self.w_cb_course_id.addItems(courses)
                    self.w_cb_course_id.setCurrentText(current_selection)
            else:
                self.w_cb_course_id.clear()
                self.w_cb_course_id.addItems(courses)

    def ui_update_plans(self, plans):
        self.logger.debug("Updating plans in MainWindow")
        if self.w_cb_plan_id.count() == 0:
            self.w_cb_plan_id.addItems(plans)
        else:
            current_selection = self.w_cb_plan_id.currentText()
            if current_selection in plans:
                with qtc.QSignalBlocker(self.w_cb_plan_id):
                    self.w_cb_plan_id.clear()
                    self.w_cb_plan_id.addItems(plans)
                    self.w_cb_plan_id.setCurrentText(current_selection)
            else:
                self.w_cb_plan_id.clear()
                self.w_cb_plan_id.addItems(plans)

    def ui_update_isocenter_label(self, iso):
        self.logger.debug("Updating isocenter label in MainWindow")
        if len(iso) == 3:
            x, y, z = iso
            x_str = f"<span style='color: #00aaff;'><b>X:</b></span> {x}"
            y_str = f"<span style='color: #00aaff;'><b>Y:</b></span> {y}"
            z_str = f"<span style='color: #00aaff;'><b>Z:</b></span> {z}"
            self.w_l_plan_isocenter.setText(f"<pre>{x_str} {y_str} {z_str}</pre>")
        else:
            x_str = f"<span style='color: #00aaff;'><b>X:</b></span> --"
            y_str = f"<span style='color: #00aaff;'><b>Y:</b></span> --"
            z_str = f"<span style='color: #00aaff;'><b>Z:</b></span> --"
            self.w_l_plan_isocenter.setText(f"{x_str} {y_str} {z_str}")

    def ui_update_beam_table(self, beams):
        self.logger.debug("Updating beam table in MainWindow")
        good_icon = qtg.QIcon(":/icons/good.png")
        bad_icon = qtg.QIcon(":/icons/bad.png")
        if not beams == []: # Need this for refreshes and clearing

            self.w_tw_beams.clear()
            self.w_tw_beams.setRowCount(0)
            self.w_tw_beams.setColumnCount(0)

            self.w_tw_beams.setRowCount(len(beams))
            self.w_tw_beams.setColumnCount(len(beams[0]))
            self.w_tw_beams.setHorizontalHeaderLabels(["",
                                                       "Num",
                                                       "ID",
                                                       "Name",
                                                       "Couch",
                                                       "Gantry Start",
                                                       "Gantry Stop",
                                                       "Rotation",
                                                       "Type"
                                                       ]
                                                      )

            for row_index, row_data in enumerate(beams):
                for col_index, cell_data in enumerate(row_data):
                    if col_index == 0 and cell_data is True:
                        item = qtw.QTableWidgetItem()
                        item.setTextAlignment(qtc.Qt.AlignmentFlag.AlignCenter)
                        item.setIcon(good_icon)
                        self.w_tw_beams.setItem(row_index, col_index, item)
                    elif col_index == 0 and cell_data is False:
                        item = qtw.QTableWidgetItem()
                        item.setTextAlignment(qtc.Qt.AlignmentFlag.AlignCenter)
                        item.setIcon(bad_icon)
                        self.w_tw_beams.setItem(row_index, col_index, item)
                    else:
                        item = qtw.QTableWidgetItem(cell_data)
                        item.setTextAlignment(qtc.Qt.AlignmentFlag.AlignCenter)
                        self.w_tw_beams.setItem(row_index, col_index, item)

            self.w_tw_beams.resizeColumnsToContents()
            self.w_tw_beams.setSortingEnabled(True)
        else:
            self.w_tw_beams.clear()
            self.w_tw_beams.setRowCount(0)
            self.w_tw_beams.setColumnCount(0)

    def ui_update_structures(self, structures):
        self.logger.debug("Updating structures in MainWindow")
        if self.w_cb_body_structure.count() == 0:
            self.w_cb_body_structure.addItems(structures)
        else:
            current_selection = self.w_cb_plan_id.currentText()
            if current_selection in structures:
                with qtc.QSignalBlocker(self.w_cb_plan_id):
                    self.w_cb_body_structure.clear()
                    self.w_cb_body_structure.addItems(structures)
                    self.w_cb_body_structure.setCurrentText(current_selection)
            else:
                self.w_cb_body_structure.clear()
                self.w_cb_body_structure.addItems(structures)

    def update_3D_dicom_visualization(self, model):
        self.logger.debug("Updating the 3D visualization for the DICOM surface in MainWindow")
        if self.dicom_actor is None:
            print("In new dicom actor code")
            self.dicom_actor = self.patient_ctx.current_plan.current_structure

            R, G, B, A = self._get_current_color(self.w_fr_dcm_color)
            print(R, G, B, A)
            # self.dicom_actor.GetProperty().SetColor(R / 255.0, G / 255.0, B / 255.0)
            self.dicom_actor.property.color = (R / 255.0, G / 255.0, B / 255.0)
            self.dicom_actor.property.opacity = self.w_hs_dcm_opacity.value() / 100.0

            self.dicom_laser_actors = self._get_laser_marks(self.dicom_actor.GetMapper().GetInput())

            laser_R, laser_G, laser_B, laser_A = self._get_current_color(self.w_fr_laser_color)
            for laser_actor in self.dicom_laser_actors:
                laser_actor.GetProperty().SetColor(laser_R / 255.0, laser_G / 255.0, laser_B / 255.0)
                laser_actor.property.opacity = (self.w_hs_laser_opacity.value() / 100.0) * \
                                               (self.w_hs_dcm_opacity.value() / 100.0)

            self.vtk_renderer.AddActor(self.dicom_actor)
            for laser_actor in self.dicom_laser_actors:
                self.vtk_renderer.AddActor(laser_actor)
            self.vtk_renderer.ResetCamera()

        else:
            self.vtk_renderer.RemoveActor(self.dicom_actor)
            for laser_actor in self.dicom_laser_actors:
                self.vtk_renderer.RemoveActor(laser_actor)

            self.dicom_actor = self.patient_ctx.current_plan.current_structure

            R, G, B, A = self._get_current_color(self.w_fr_dcm_color)
            self.dicom_actor.GetProperty().SetColor(R / 255.0, G / 255.0, B / 255.0)
            self.dicom_actor.property.opacity = self.w_hs_dcm_opacity.value() / 100.0

            self.dicom_laser_actors = self._get_laser_marks(self.dicom_actor.GetMapper().GetInput())

            laser_R, laser_G, laser_B, laser_A = self._get_current_color(self.w_fr_laser_color)
            for laser_actor in self.dicom_laser_actors:
                laser_actor.GetProperty().SetColor(laser_R / 255.0, laser_G / 255.0, laser_B / 255.0)
                laser_actor.property.opacity = (self.w_hs_laser_opacity.value() / 100.0) * \
                                               (self.w_hs_dcm_opacity.value() / 100.0)

            self.vtk_renderer.AddActor(self.dicom_actor)
            for laser_actor in self.dicom_laser_actors:
                self.vtk_renderer.AddActor(laser_actor)


        self.vtk_render_window.Render()

    def dicom_surface_color_changed(self):
        self.logger.debug("DICOM surface color changed in MainWindow")
        _R, _G, _B, _A = self._get_current_color(self.w_fr_dcm_color)
        color = qtw.QColorDialog.getColor(qtg.QColor(_R, _G, _B) , self, "Select Color")

        if color.isValid():
            R, G, B, A = color.getRgb()
            self.w_fr_dcm_color.setStyleSheet(f"background-color: rgb({R}, {G}, {B});")
            self.w_fr_dcm_color.show()

            if self.dicom_actor is not None:
                self.dicom_actor.GetProperty().SetColor(R / 255.0, G / 255.0, B / 255.0)
                self.vtk_render_window.Render()

    def dicom_surface_opacity_changed(self):
        # self.logger.debug("DICOM surface opacity changed in MainWindow")
        self.w_l_dcm_opacity.setText(str(self.w_hs_dcm_opacity.value()))
        if self.dicom_actor is not None:
            self.dicom_actor.property.opacity = self.w_hs_dcm_opacity.value() / 100.0

            for laser_actor in self.dicom_laser_actors:
                laser_actor.property.opacity = (self.w_hs_laser_opacity.value() / 100.0) * \
                                               (self.w_hs_dcm_opacity.value() / 100.0)
            self.vtk_render_window.Render()

    def ui_clear_dicom_3d_scene(self):
        self.logger.debug("Clearing DICOM components from 3D scene in MainWindow")
        if self.dicom_actor is not None:
            self.vtk_renderer.RemoveActor(self.dicom_actor)
            for laser_actor in self.dicom_laser_actors:
                self.vtk_renderer.RemoveActor(laser_actor)
            self.vtk_render_window.Render()
            self.dicom_actor = None
            self.dicom_laser_actors = ()

    ####################################################################################
    # MapRTContext Connections and Methods                                             #
    ####################################################################################

    def fetch_api_data(self):
        self.logger.debug("Pulling data from MapRT API Manager in MainWindow")

        if self.patient_ctx.patient_id == '':
            self.logger.info("No patient context found requesting basic patient information from user")
            dialog = MapRTPatientDialog()
            if dialog.exec():
                self.logger.info("Constructing Preview Context for Patient, Course and Plan")
                self.patient_ctx.patient_id = dialog.w_le_patient_id.text()
                self.patient_ctx.first_name = 'Preview'
                self.patient_ctx.last_name = 'MapRT Patient'

                plan = DicomPlanContext()
                plan.plan_id = 'Preview Plan'
                plan.frame_of_reference_uid = 'Preview'
                plan.patient_orientation = dialog.w_cb_patient_orientation.currentText()
                plan.isocenter = np.zeros(3)
                plan.beams = []
                plans = {plan.plan_id: plan}

                self.patient_ctx._courses['P1'] = plans
                self.patient_ctx.courses_updated.emit(self.patient_ctx.courses)
                self.patient_ctx.update_current_course('P1')
                self.patient_ctx.update_current_plan(plan.plan_id)

                self.logger.info("Attempting to gather MapRT information from API Manager base on user input")
                self.maprt_api.get_status()
                self.maprt_api.get_treatment_rooms()
                self.maprt_api.get_patient_surfaces(self.patient_ctx.patient_id)
                self.w_pb_get_map.setEnabled(True)
        else:
            self.logger.info("Attempting to gather MapRT information from API Manager based on active patient context")
            self.maprt_api.get_status()
            self.maprt_api.get_treatment_rooms()
            self.maprt_api.get_patient_surfaces(self.patient_ctx.patient_id)
            self.w_pb_get_map.setEnabled(True)

    def get_maprt_collision_maps(self):
        self.logger.debug("Requesting collision map data from MapRT API Manager in MainWindow")
        self.maprt_api.get_map(self.maprt_ctx,
                               x_shift=self.w_dsb_surface_shift_x.value(),
                               y_shift=self.w_dsb_surface_shift_y.value(),
                               z_shift=self.w_dsb_surface_shift_z.value()
                               )

    def ui_update_maprt_treatment_rooms(self, rooms):
        self.logger.debug("Updating MapRT treatment room selections in MainWindow")
        if self.w_cb_treatment_room.count() == 0:
            self.w_cb_treatment_room.addItems(rooms)
        else:
            current_selection = self.w_cb_treatment_room.currentText()
            if current_selection in rooms:
                with qtc.QSignalBlocker(self.w_cb_treatment_room):
                    self.w_cb_treatment_room.clear()
                    self.w_cb_treatment_room.addItems(rooms)
                    self.w_cb_treatment_room.setCurrentText(current_selection)
            else:
                self.w_cb_treatment_room.clear()
                self.w_cb_treatment_room.addItems(rooms)

    def ui_update_maprt_surfaces(self, surfaces):
        self.logger.debug("Updating MapRT surface selections in MainWindow")
        if self.w_cb_surface_for_map.count() == 0:
            self.w_cb_surface_for_map.addItems(surfaces)
        else:
            current_selection = self.w_cb_surface_for_map.currentText()
            if current_selection in surfaces:
                with qtc.QSignalBlocker(self.w_cb_surface_for_map):
                    self.w_cb_surface_for_map.clear()
                    self.w_cb_surface_for_map.addItems(surfaces)
                    self.w_cb_surface_for_map.setCurrentText(current_selection)
            else:
                self.w_cb_surface_for_map.clear()
                self.w_cb_surface_for_map.addItems(surfaces)

    def ui_update_maprt_collision_maps(self, maps):
        self.logger.debug("Updating MapRT collision map selections in MainWindow")

        if self.w_cb_current_map.count() == 0:
            self.w_cb_current_map.addItems(maps)
        else:

            self.w_cb_current_map.blockSignals(True)
            self.w_cb_current_map.clear()
            self.w_cb_current_map.blockSignals(False)
            self.w_cb_current_map.addItems(maps)
            self.w_cb_current_map.setCurrentText(self.maprt_ctx.current_map_label)

    def ui_update_maprt_3D_surface_visualization(self, surface):
        self.logger.debug("Updating MapRT 3D surface visualization in MainWindow")
        if self.maprt_actor is None:

            if self.maprt_ctx.current_surface is not None:
                self.maprt_transform = vtk.vtkTransform()
                self.maprt_transform.PostMultiply()
                self.maprt_transform.Translate(self.w_dsb_surface_shift_x.value() * 10,
                                               self.w_dsb_surface_shift_y.value() * 10,
                                               self.w_dsb_surface_shift_z.value() * 10
                                               )

                # Create a transform filter
                self.maprt_transform_filter = vtk.vtkTransformFilter()
                self.maprt_transform_filter.SetInputData(self.maprt_ctx.current_surface.vtk_polydata)
                self.maprt_transform_filter.SetTransform(self.maprt_transform)
                self.maprt_transform_filter.Update()

                self.maprt_surface_mapper = vtk.vtkPolyDataMapper()
                self.maprt_surface_mapper.SetInputData(self.maprt_transform_filter.GetOutput())

                self.maprt_actor = vtk.vtkActor(mapper=self.maprt_surface_mapper)

                R, G, B, A = self._get_current_color(self.w_fr_obj_color)
                self.maprt_actor.GetProperty().SetColor(R / 255.0, G / 255.0, B / 255.0)
                self.maprt_actor.property.opacity = self.w_hs_obj_opacity.value() / 100.0

                self.maprt_laser_actors = self._get_laser_marks(self.maprt_transform_filter.GetOutput())

                laser_R, laser_G, laser_B, laser_A = self._get_current_color(self.w_fr_laser_color)
                for laser_actor in self.maprt_laser_actors:
                    laser_actor.GetProperty().SetColor(laser_R / 255.0, laser_G / 255.0, laser_B / 255.0)
                    laser_actor.property.opacity = (self.w_hs_laser_opacity.value() / 100.0) * \
                                                   (self.w_hs_obj_opacity.value() / 100.0)

                self.vtk_renderer.AddActor(self.maprt_actor)
                for laser_actor in self.maprt_laser_actors:
                    self.vtk_renderer.AddActor(laser_actor)
                self.vtk_renderer.ResetCamera()

        else:
            if self.maprt_ctx.current_surface is not None:
                self.vtk_renderer.RemoveActor(self.maprt_actor)
                for laser_actor in self.maprt_laser_actors:
                    self.vtk_renderer.RemoveActor(laser_actor)

                self.maprt_transform = vtk.vtkTransform()
                self.maprt_transform.PostMultiply()
                self.maprt_transform.Translate(self.w_dsb_surface_shift_x.value() * 10,
                                               self.w_dsb_surface_shift_y.value() * 10,
                                               self.w_dsb_surface_shift_z.value() * 10
                                               )

                # Create a transform filter
                self.maprt_transform_filter = vtk.vtkTransformFilter()
                self.maprt_transform_filter.SetInputData(self.maprt_ctx.current_surface.vtk_polydata)
                self.maprt_transform_filter.SetTransform(self.maprt_transform)
                self.maprt_transform_filter.Update()

                self.maprt_surface_mapper = vtk.vtkPolyDataMapper()
                self.maprt_surface_mapper.SetInputData(self.maprt_transform_filter.GetOutput())

                self.maprt_actor = vtk.vtkActor(mapper=self.maprt_surface_mapper)

                R, G, B, A = self._get_current_color(self.w_fr_obj_color)
                self.maprt_actor.GetProperty().SetColor(R / 255.0, G / 255.0, B / 255.0)
                self.maprt_actor.property.opacity = self.w_hs_obj_opacity.value() / 100.0

                self.maprt_laser_actors = self._get_laser_marks(self.maprt_transform_filter.GetOutput())

                laser_R, laser_G, laser_B, laser_A = self._get_current_color(self.w_fr_laser_color)
                for laser_actor in self.maprt_laser_actors:
                    laser_actor.GetProperty().SetColor(laser_R / 255.0, laser_G / 255.0, laser_B / 255.0)
                    laser_actor.property.opacity = (self.w_hs_laser_opacity.value() / 100.0) * \
                                                   (self.w_hs_obj_opacity.value() / 100.0)

                self.vtk_renderer.AddActor(self.maprt_actor)
                for laser_actor in self.maprt_laser_actors:
                    self.vtk_renderer.AddActor(laser_actor)

        self.vtk_render_window.Render()

    def ui_update_collision_map_graphics_view(self, current_map_data):
        self.logger.debug("Updating MapRT collision map visualization in MainWindow")
        if self.collision_map is not None:
            self.collision_map_plot_widget.removeItem(self.collision_map)

        self.collision_map, x_ticks, y_ticks = current_map_data
        self.collision_map.setZValue(0)
        self.collision_map.setLookupTable(self.collision_map_lut)

        bottom_axis = self.collision_map_plot_widget.getAxis('bottom')
        bottom_axis.setTicks(x_ticks)

        left_axis = self.collision_map_plot_widget.getAxis('left')
        left_axis.setTicks(y_ticks)

        self.collision_map_plot_widget.addItem(self.collision_map)
        self.w_cb_current_map.setCurrentText(self.maprt_ctx.current_map_label)

    def ui_update_beam_plots(self, beam_plot_items):
        self.logger.debug("Updating beam plots on MapRT collision map visualization in MainWindow")
        arcs, static_beams = beam_plot_items

        if self.plotted_beams is not None:
            for beam in self.plotted_beams:
                self.collision_map_plot_widget.removeItem(beam)

        plotted_beams = []
        for arc in arcs:
            arc.setZValue(25)
            self.collision_map_plot_widget.addItem(arc)
            plotted_beams.append(arc)
        for static_beam in static_beams:
            static_beam.setZValue(25)
            self.collision_map_plot_widget.addItem(static_beam)
            plotted_beams.append(static_beam)
        self.plotted_beams = plotted_beams

    def ui_notify_connection_error(self, message):
        self.logger.critical("User notified of MapRT API connection error in MainWindow")
        qtw.QMessageBox.critical(self, "MapRT API Error", message, qtw.QMessageBox.Ok)

    def ui_select_maprt_surface_file(self):
        self.logger.debug("User request to select .obj file for visualization in MainWindow")
        file_path, _ = qtw.QFileDialog.getOpenFileName(self,
                                                      "Select MapRT .obj Surface File",
                                                      ".",
                                                      "OBJ Files (*.obj)"
                                                      )
        if file_path:
            get_map_state = self.w_pb_get_map.isEnabled()

            try:
                self.logger.info("Setting application to MapRT file mode")
                self.ui_set_maprt_file_mode(True)

                if self.patient_ctx.patient_id == '':
                    self.logger.info("No active Patient Context found requesting basic patient information from user")
                    dialog = MapRTPatientDialog()
                    if dialog.exec():
                        self.logger.info("Setting up Preview Context for Patient, Course and Plan")
                        self.patient_ctx.patient_id = dialog.w_le_patient_id.text()
                        self.patient_ctx.first_name = 'Preview'
                        self.patient_ctx.last_name = 'MapRT Patient'

                        plan = DicomPlanContext()
                        plan.plan_id = 'Preview Plan'
                        plan.frame_of_reference_uid = 'Preview'
                        plan.patient_orientation = dialog.w_cb_patient_orientation.currentText()
                        plan.isocenter = np.zeros(3)
                        plan.beams = []
                        plans = {plan.plan_id: plan}

                        self.patient_ctx._courses['P1'] = plans
                        self.patient_ctx.courses_updated.emit(self.patient_ctx.courses)
                        self.patient_ctx.update_current_course('P1')
                        self.patient_ctx.update_current_plan(plan.plan_id)

                        self.logger.info("Loading surface file for visualization")
                        self.maprt_ctx.load_surface_file(file_path, self.patient_ctx.current_plan.patient_orientation)

                else:
                    self.logger.info("Patient Context found requesting basic patient orientation information from user")
                    dialog = OrientDialog()
                    if dialog.exec() == qtw.QDialog.DialogCode.Accepted:
                        _orientation = dialog.w_cb_obj_surface_orientation.currentText()
                        if _orientation == "Current Plan" and self.patient_ctx.current_plan is not None:
                            self.maprt_ctx.load_surface_file(file_path, self.patient_ctx.current_plan.patient_orientation)

                        else:
                            self.maprt_ctx.load_surface_file(file_path, _orientation)

            except Exception as e:
                self.logger.error(str(e))
                self.ui_set_maprt_file_mode(False)
                self.w_pb_get_map.setEnabled(get_map_state)
                self.ui_show_info_message(str(e))

    def collision_map_mouse_moved(self, event):
        # self.logger.debug("Mouse motion detected over MapRT collision map in MainWindow")
        pos = event  # using signal proxy turns original event into tuple
        if self.collision_map_view_box.sceneBoundingRect().contains(pos):
            mouse_point = self.collision_map_view_box.mapSceneToView(pos)
            self.collision_map_v_line.setPos(mouse_point.x())
            self.collision_map_v_line.setZValue(100)
            self.collision_map_h_line.setPos(mouse_point.y())
            self.collision_map_h_line.setZValue(101)
            # self.text_item.setText(f"x={mouse_point.x():.2f}, y={mouse_point.y():.2f}")
            # print(f"x={mouse_point.x():.2f}, y={mouse_point.y():.2f}")

    def maprt_surface_color_changed(self):
        self.logger.debug("MapRT surface color changed in MainWindow")
        _R, _G, _B, _A = self._get_current_color(self.w_fr_obj_color)
        color = qtw.QColorDialog.getColor(qtg.QColor(_R, _G, _B), self, "Select Color")

        if color.isValid():
            R, G, B, A = color.getRgb()
            self.w_fr_obj_color.setStyleSheet(f"background-color: rgb({R}, {G}, {B});")
            self.w_fr_obj_color.show()

            if self.maprt_actor is not None:
                self.maprt_actor.GetProperty().SetColor(R / 255.0, G / 255.0, B / 255.0)
                self.vtk_render_window.Render()

    def maprt_surface_opacity_changed(self):
        # self.logger.debug("MapRT surface opacity changed in MainWindow")
        self.w_l_obj_opacity.setText(str(self.w_hs_obj_opacity.value()))
        if self.maprt_actor is not None:
            self.maprt_actor.property.opacity = self.w_hs_obj_opacity.value() / 100.0
            for laser_actor in self.maprt_laser_actors:
                laser_actor.property.opacity = (self.w_hs_laser_opacity.value() / 100.0) * \
                                               (self.w_hs_obj_opacity.value() / 100.0)
            self.vtk_render_window.Render()
        else:
            pass

    def export_surface_to_dicom(self):
        self.logger.debug("Exporting MapRT surface to DICOM in MainWindow")
        #TODO: Add Exception handling to this function

        export_dialog = SurfaceExportDialog(self)
        if export_dialog.exec():
            polydata = export_dialog.clipper.GetOutput()
            points = vtk_to_numpy(polydata.GetPoints().GetData())
            voxel_size = export_dialog.w_dsb_voxel_size.value()

            # TODO: Make this a configuration widget in the UI
            pixel_value = 2000

            # Grab the bounding coordinates for the surface in DICOM orientation
            x_min, x_max, y_min, y_max, z_min, z_max = polydata.GetBounds()
            bounds_min = np.array([x_min, y_min, z_min])
            bounds_max = np.array([x_max, y_max, z_max])

            # Calculate grid dimensions
            dimensions = np.ceil((bounds_max - bounds_min) / voxel_size).astype(int)

            # Construct the Pixel to Coordinate transform matrix
            pixel_to_coord = np.eye(4, dtype=np.float64)
            pixel_to_coord *= voxel_size
            pixel_to_coord[0,-1] = x_min
            pixel_to_coord[1,-1] = y_min
            pixel_to_coord[2,-1] = z_min
            pixel_to_coord[3, -1] = 1

            # Take the inverse to get the Coordinate to Pixel index transform used to find the grid values
            coord_to_pixel = np.linalg.inv(pixel_to_coord)

            # Initialize an empty NumPy array with the calculated dimensions
            pixel_data = np.zeros(dimensions[::-1], dtype=np.uint16)

            # Convert the point coords to pixel indexes
            affine_coords = np.vstack((points.T, np.ones(len(points))))
            pixel_idxs = np.floor(coord_to_pixel @ affine_coords).astype(int)
            i, j, k, _ = pixel_idxs

            # Use the pixel indexes to set all occupied pixels in the grid to the pixel value
            if export_dialog.w_ch_fill_down.isChecked():
                for idx in range(len(i)):
                    pixel_data[k[idx], j[idx]::, i[idx]] = pixel_value
            else:
                pixel_data[(k, j, i)] = pixel_value


            if export_dialog.w_ch_smooth.isChecked():
                sigma = export_dialog.w_dsb_sigma.value()
                smoothed_pixel_data = gaussian_filter(pixel_data, sigma=sigma)
            else:
                smoothed_pixel_data = pixel_data

            # dicom_path = None
            # with open(r'resources/settings.json', 'r') as settings:
            #     settings_data = json.load(settings)
            #     self.settings = AppSettings(**settings_data)
            #
            #     dicom_path = Path(self.settings.dicom.dicom_data_directory)

            dicom_path = Path(app_settings.dicom.dicom_data_directory)
            save_path = dicom_path / f"{self.patient_ctx.patient_id}-{voxel_size}"
            save_path.mkdir(parents=True, exist_ok=True)

            dt_object = dt.datetime.now()
            study = pydicom.uid.generate_uid()
            series = pydicom.uid.generate_uid()
            frame_of_ref = pydicom.uid.generate_uid()
            for i, image in enumerate(smoothed_pixel_data):
            # for i, image in enumerate(pixel_data):

                instance = pydicom.uid.generate_uid()

                file_meta = FileMetaDataset()
                file_meta.FileMetaInformationGroupLength = 192
                file_meta.FileMetaInformationVersion = b'\x00\x01'
                file_meta.MediaStorageSOPClassUID = CTImageStorage
                file_meta.MediaStorageSOPInstanceUID = pydicom.uid.generate_uid()
                file_meta.TransferSyntaxUID = ExplicitVRLittleEndian

                # Main data elements
                ds = Dataset()
                ds.file_meta = file_meta
                ds.is_implicit_VR = True
                ds.is_little_endian = True

                ds.PatientName = f"{self.patient_ctx.last_name}^{self.patient_ctx.first_name}"
                ds.PatientID = f"{self.patient_ctx.patient_id}-{voxel_size}"
                ds.PatientBirthDate = dt_object.strftime("%Y%m%d")
                ds.PatientSex = 'M'
                ds.PatientPosition = self.patient_ctx.current_plan.patient_orientation

                ds.SpecificCharacterSet = 'ISO_IR 192'
                ds.ImageType = ['ORIGINAL', 'PRIMARY', 'AXIAL']
                ds.InstanceCreationDate = dt_object.strftime("%Y%m%d")
                ds.InstanceCreationTime = dt_object.strftime("%H%M%S")
                ds.SOPClassUID = CTImageStorage
                ds.SOPInstanceUID = instance
                ds.StudyInstanceUID = study
                ds.SeriesInstanceUID = series
                ds.StudyID = '42'
                ds.SeriesNumber = '1'
                ds.AcquisitionNumber = '1'
                ds.InstanceNumber = str(i + 1)
                ds.StudyDate = dt_object.strftime("%Y%m%d")
                ds.SeriesDate = dt_object.strftime("%Y%m%d")
                ds.AcquisitionDate = dt_object.strftime("%Y%m%d")
                ds.ContentDate = dt_object.strftime("%Y%m%d")
                ds.StudyTime = dt_object.strftime("%H%M%S.%f")
                ds.SeriesTime = dt_object.strftime("%H%M%S.%f")
                ds.AcquisitionTime = dt_object.strftime("%H%M%S.%f")
                ds.ContentTime = dt_object.strftime("%H%M%S.%f")
                ds.AccessionNumber = ''
                ds.Modality = 'CT'
                ds.Manufacturer = 'Map App'
                ds.ReferringPhysicianName = ''
                ds.StationName = 'Map App'
                ds.StudyDescription = 'Synthetic Surface CT'
                ds.PhysiciansOfRecord = 'Physician'
                ds.OperatorsName = 'DICOM Service'
                ds.ManufacturerModelName = 'Patient Verification'

                ds.ImagePositionPatient = [x_min, y_min, z_min + (i * voxel_size)]
                ds.ImageOrientationPatient = [1, 0, 0, 0, 1, 0]
                ds.FrameOfReferenceUID = frame_of_ref
                ds.PositionReferenceIndicator = ''
                ds.ImageComments = f'Voxel Size {voxel_size}'
                ds.SamplesPerPixel = 1
                ds.PhotometricInterpretation = 'MONOCHROME2'
                ds.Rows = image.shape[0]
                ds.Columns = image.shape[1]
                ds.PixelSpacing = [voxel_size, voxel_size]
                ds.SliceThickness = f"{voxel_size}"
                ds.KVP = '120.0'
                ds.BitsAllocated = 16
                ds.BitsStored = 16
                ds.HighBit = 15
                ds.PixelRepresentation = 0
                ds.WindowCenter = '500'
                ds.WindowWidth = '1000'
                ds.RescaleIntercept = '0'
                ds.RescaleSlope = '1.0'
                ds.RescaleType = 'HU'

                ds.PixelData = image.tobytes()

                # Save the DICOM file
                ds.save_as(f'{str(save_path)}\\CT.{instance}.dcm', write_like_original=False)
        else:
            print("export canceled")

    def ui_clear_maprt_3d_scene(self):
        self.logger.debug("Clearing MapRT components from 3D visual scene in MainWindow")
        if self.maprt_actor is not None:
            self.vtk_renderer.RemoveActor(self.maprt_actor)
            for laser_actor in self.maprt_laser_actors:
                self.vtk_renderer.RemoveActor(laser_actor)
            self.vtk_render_window.Render()
            self.maprt_actor = None
            self.maprt_laser_actors = ()

            # You are clearing the UI so block the signals so that downstream method calls are avoided
            self.w_dsb_surface_shift_x.blockSignals(True)
            self.w_dsb_surface_shift_x.setValue(0)
            self.w_dsb_surface_shift_x.blockSignals(False)

            self.w_dsb_surface_shift_y.blockSignals(True)
            self.w_dsb_surface_shift_y.setValue(0)
            self.w_dsb_surface_shift_y.blockSignals(False)

            self.w_dsb_surface_shift_z.blockSignals(True)
            self.w_dsb_surface_shift_z.setValue(0)
            self.w_dsb_surface_shift_z.blockSignals(False)

    def ui_clear_collision_map_plot(self):
        self.logger.debug("Clearing MapRT collision map information in MainWindow")
        if self.collision_map is not None:
            self.collision_map_plot_widget.removeItem(self.collision_map)
            self.collision_map = None

        if self.plotted_beams is not None:
            for beam in self.plotted_beams:
                self.collision_map_plot_widget.removeItem(beam)

            self.plotted_beams = None

    ####################################################################################
    # ui manipulation methods                                                          #
    ####################################################################################

    def show_settings_dialog(self):
        self.logger.debug("Showing application settings dialog in MainWindow")
        settings_dialog = SettingsDialog()

        if settings_dialog.exec():
            print("writing settings")

            app_settings.dicom.dicom_data_directory = settings_dialog.w_le_dicom_directory.text()
            app_settings.dicom.arc_check_resolution = settings_dialog.w_sb_arc_check_resolution.value()
            app_settings.dicom.surface_recon_method = settings_dialog.w_cb_recon_method.currentText()
            app_settings.dicom.pixel_spacing_x = settings_dialog.w_dsb_pixel_spacing_x.value()
            app_settings.dicom.pixel_spacing_y = settings_dialog.w_dsb_pixel_spacing_y.value()
            app_settings.dicom.contours_to_keep = settings_dialog.w_cb_contours_to_keep.currentText()

            app_settings.maprt.api_url = settings_dialog.w_le_api_url.text()
            hidden_token = base64.b64encode(binascii.hexlify(settings_dialog.w_le_api_token.text().encode('utf-8'))).decode('utf-8')
            app_settings.maprt.api_token = hidden_token
            app_settings.maprt.api_user_agent = settings_dialog.w_le_api_user_agent.text()

            print()

            with open('settings.json', 'w') as settings:
                settings.write(app_settings.model_dump_json(indent=4))
        else:
            print("ignoring settings changes")

    def ui_show_info_message(self, message):
        self.logger.debug(f"'{message}' message sent to user in MainWindow")
        qtw.QMessageBox.information(self, "Information", message, qtw.QMessageBox.Ok)

    def ui_set_dicom_file_mode(self, value=False):
        self.logger.debug(f"Updating UI for DICOM file mode = {value} in MainWindow")
        self.dicom_file_mode = value
        self.w_pb_esapi_search.setEnabled(not self.dicom_file_mode)
        self.w_le_patinet_id.setEnabled(not self.dicom_file_mode)
        self.w_cb_course_id.setEnabled(not self.dicom_file_mode)
        self.w_cb_plan_id.setEnabled(not self.dicom_file_mode)

    def ui_set_maprt_file_mode(self, value=False):
        self.logger.debug(f"Updating UI for MapRT file mode = {value} in MainWindow")
        self.maprt_file_mode = value
        self.w_pb_fetch_api_data.setEnabled(not self.maprt_file_mode)
        self.w_cb_treatment_room.setEnabled(not self.maprt_file_mode)
        self.w_dsb_api_couch_buffer.setEnabled(not self.maprt_file_mode)
        self.w_dsb_api_patient_buffer.setEnabled(not self.maprt_file_mode)
        self.w_pb_get_map.setEnabled(not self.maprt_file_mode)

    def ui_clear_ui_components(self):
        self.logger.debug("Clearing all UI components in MainWindow")
        self.ui_clear_dicom_3d_scene()
        self.ui_clear_maprt_3d_scene()
        self.ui_clear_collision_map_plot()
        self.ui_set_dicom_file_mode(value=False)
        self.ui_set_maprt_file_mode(value=False)
        self.w_pb_get_map.setEnabled(False)

    def ui_visualize_axis_widget(self):
        self.logger.debug("Toggling axis indicator widget visibility in MainWindow")
        if self.w_ch_axis_widget.isChecked():
            self.axis_widget.EnabledOn()
        else:
            self.axis_widget.EnabledOff()

        self.vtk_render_window.Render()

    def ui_visualize_cam_orientation_widget(self):
        self.logger.debug("Toggling camera orientation widget visibility in MainWindow")
        if self.w_ch_orientation_widget.isChecked():
            self.cam_orient_manipulator.EnabledOn()
        else:
            self.cam_orient_manipulator.EnabledOff()

        self.vtk_render_window.Render()

    def _get_laser_marks(self, polydata):
        self.logger.debug("Constructing laser actors for visualization in MainWindow")
        X, Y, Z = self.patient_ctx.current_plan.isocenter

        # Create laser planes
        xy_plane = vtk.vtkPlane()
        xy_plane.SetOrigin(0, 0, Z)
        xy_plane.SetNormal(0, 0, 1)

        # Create a planes
        yz_plane = vtk.vtkPlane()
        yz_plane.SetOrigin(X, 0, 0)
        yz_plane.SetNormal(1, 0, 0)

        # Create a planes
        zx_plane = vtk.vtkPlane()
        zx_plane.SetOrigin(0, Y, 0)
        zx_plane.SetNormal(0, 1, 0)

        # Create laser cutters
        xy_cutter = vtk.vtkCutter()
        xy_cutter.SetCutFunction(xy_plane)
        xy_cutter.SetInputData(polydata)
        xy_cutter.Update()

        yz_cutter = vtk.vtkCutter()
        yz_cutter.SetCutFunction(yz_plane)
        yz_cutter.SetInputData(polydata)
        yz_cutter.Update()

        zx_cutter = vtk.vtkCutter()
        zx_cutter.SetCutFunction(zx_plane)
        zx_cutter.SetInputData(polydata)
        zx_cutter.Update()

        # Create sphere geometry
        sphereSource = vtk.vtkSphereSource()
        sphereSource.radius = 1.5
        sphereSource.phi_resolution = 5
        sphereSource.theta_resolution = 5

        # Mapp the Sphere Glyph to the points
        xy_glyphFilter = vtk.vtkGlyph3D()
        xy_glyphFilter.SetInputData(xy_cutter.GetOutput())
        xy_glyphFilter.SetSourceConnection(sphereSource.GetOutputPort())
        xy_glyphFilter.SetScaling(False)  # Disable scaling of glyphs
        xy_glyphFilter.Update()

        yz_glyphFilter = vtk.vtkGlyph3D()
        yz_glyphFilter.SetInputData(yz_cutter.GetOutput())
        yz_glyphFilter.SetSourceConnection(sphereSource.GetOutputPort())
        yz_glyphFilter.SetScaling(False)  # Disable scaling of glyphs
        yz_glyphFilter.Update()

        zx_glyphFilter = vtk.vtkGlyph3D()
        zx_glyphFilter.SetInputData(zx_cutter.GetOutput())
        zx_glyphFilter.SetSourceConnection(sphereSource.GetOutputPort())
        zx_glyphFilter.SetScaling(False)  # Disable scaling of glyphs
        zx_glyphFilter.Update()

        # Create a mapper and actor for the cut surface
        xy_cut_mapper = vtk.vtkPolyDataMapper()
        xy_cut_mapper.SetInputData(xy_glyphFilter.GetOutput())
        xy_cut_mapper.ScalarVisibilityOff()
        xy_cut_actor = vtk.vtkActor()
        xy_cut_actor.SetMapper(xy_cut_mapper)
        xy_cut_actor.GetProperty().SetColor(1, 0, 0)  # Red color for the cut surface

        yz_cut_mapper = vtk.vtkPolyDataMapper()
        yz_cut_mapper.SetInputData(yz_glyphFilter.GetOutput())
        yz_cut_mapper.ScalarVisibilityOff()
        yz_cut_actor = vtk.vtkActor()
        yz_cut_actor.SetMapper(yz_cut_mapper)
        yz_cut_actor.GetProperty().SetColor(1, 0, 0)  # Red color for the cut surface

        zx_cut_mapper = vtk.vtkPolyDataMapper()
        zx_cut_mapper.SetInputData(zx_glyphFilter.GetOutput())
        zx_cut_mapper.ScalarVisibilityOff()
        zx_cut_actor = vtk.vtkActor()
        zx_cut_actor.SetMapper(zx_cut_mapper)
        zx_cut_actor.GetProperty().SetColor(1, 0, 0)  # Red color for the cut surface

        return (xy_cut_actor, yz_cut_actor, zx_cut_actor)

    def _get_current_color(self, frame):
        self.logger.debug("Returning current color for supplied example frame in MainWindow")
        palette = frame.palette()
        background_color = palette.color(qtg.QPalette.ColorRole.Window)
        return background_color.getRgb()

    def _get_viewing_bounds(self):
        self.logger.debug("Determining max bounds for 3D viewing in MainWindow")
        _x_min, _x_max, _y_min, _y_max, _z_min, _z_max = [], [], [], [], [], []

        actors = self.vtk_renderer.GetActors()
        actors.InitTraversal()
        current_actor = actors.GetNextActor()
        while current_actor is not None:
            poly = current_actor.GetMapper().GetInput()

            x_min, x_max, y_min, y_max, z_min, z_max = poly.bounds
            _x_min.append(x_min)
            _x_max.append(x_max)
            _y_min.append(y_min)
            _y_max.append(y_max)
            _z_min.append(z_min)
            _z_max.append(z_max)

            current_actor = actors.GetNextActor()

        return (min(_x_min), max(_x_max), min(_y_min), max(_y_max), min(_z_min), max(_z_max))

    def laser_color_changed(self):
        self.logger.debug("Laser color changed in MainWindow")
        _R, _G, _B, _A = self._get_current_color(self.w_fr_laser_color)
        color = qtw.QColorDialog.getColor(qtg.QColor(_R, _G, _B), self, "Select Color")

        if color.isValid():
            R, G, B, A = color.getRgb()
            self.w_fr_laser_color.setStyleSheet(f"background-color: rgb({R}, {G}, {B});")
            self.w_fr_laser_color.show()

            if self.dicom_actor is not None:
                for laser_actor in self.dicom_laser_actors:
                    laser_actor.GetProperty().SetColor(R / 255.0, G / 255.0, B / 255.0)

            if self.maprt_actor is not None:
                for laser_actor in self.maprt_laser_actors:
                    laser_actor.GetProperty().SetColor(R / 255.0, G / 255.0, B / 255.0)

            self.vtk_render_window.Render()

    def laser_opacity_changed(self):
        # self.logger.debug("Laser opacity changed in MainWindow")
        self.w_l_laser_opacity.setText(str(self.w_hs_laser_opacity.value()))
        if self.maprt_actor is not None:
            for laser_actor in self.maprt_laser_actors:
                laser_actor.property.opacity = (self.w_hs_laser_opacity.value() / 100.0) * \
                                               (self.w_hs_obj_opacity.value() / 100.0)
            self.vtk_render_window.Render()

        if self.dicom_actor is not None:
            for laser_actor in self.dicom_laser_actors:
                laser_actor.property.opacity = (self.w_hs_laser_opacity.value() / 100.0) * \
                                               (self.w_hs_dcm_opacity.value() / 100.0)
            self.vtk_render_window.Render()

    def vtk_render_window_background_color_changed(self):
        self.logger.debug("Background color for 3D visual scene changed in MainWindow")
        _R, _G, _B, _A = self._get_current_color(self.w_fr_background_color)
        color = qtw.QColorDialog.getColor(qtg.QColor(_R, _G, _B), self, "Select Color")

        if color.isValid():
            R, G, B, A = color.getRgb()
            self.w_fr_background_color.setStyleSheet(f"background-color: rgb({R}, {G}, {B});")
            self.w_fr_background_color.show()

            self.vtk_renderer.SetBackground(R/255.0, G/255.0, B/255.0)
            self.vtk_render_window.Render()

    def save_3d_image(self):
        self.logger.debug("User requested 3D visual scene be saved as static image in MainWindow")
        filename, _ = qtw.QFileDialog.getSaveFileName(self,
                                                      "Save Render Window as Image",
                                                      ".",
                                                      "PNG Image (*.png);;BitMap Image (*.bmp)"
                                                      )
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

    def set_camera_to_plus_x(self):
        self.logger.debug("Camera position for 3D visual scene set to view from +X in MainWindow")
        if self.w_rb_plusX.isChecked():
            camera = self.vtk_renderer.GetActiveCamera()
            x_min, x_max, y_min, y_max, z_min, z_max = self._get_viewing_bounds()
            center = [(x_min + x_max) / 2.0, (y_min + y_max) / 2.0, (z_min + z_max) / 2.0]

            x_length = x_max - x_min
            y_length = y_max - y_min
            z_length = z_max - z_min
            max_length = max(x_length, y_length, z_length)

            camera.SetPosition(x_max + max_length, center[1], center[2])
            camera.SetFocalPoint(center[0], center[1], center[2])
            camera.SetViewUp(0, -1, 0)
            camera.SetParallelProjection(True)
            self.vtk_renderer.ResetCameraClippingRange()
            self.vtk_renderer.ResetCamera()
            self.vtk_render_window.Render()

    def set_camera_to_minus_x(self):
        self.logger.debug("Camera position for 3D visual scene set to view from -X in MainWindow")
        if self.w_rb_minusX.isChecked():
            camera = self.vtk_renderer.GetActiveCamera()
            x_min, x_max, y_min, y_max, z_min, z_max = self._get_viewing_bounds()
            center = [(x_min + x_max) / 2.0, (y_min + y_max) / 2.0, (z_min + z_max) / 2.0]

            x_length = x_max - x_min
            y_length = y_max - y_min
            z_length = z_max - z_min
            max_length = max(x_length, y_length, z_length)

            camera.SetPosition(x_min - max_length, center[1], center[2])
            camera.SetFocalPoint(center[0], center[1], center[2])
            camera.SetViewUp(0, -1, 0)
            camera.SetParallelProjection(True)
            self.vtk_renderer.ResetCameraClippingRange()
            self.vtk_renderer.ResetCamera()
            self.vtk_render_window.Render()

    def set_camera_to_plus_y(self):
        self.logger.debug("Camera position for 3D visual scene set to view from +Y in MainWindow")
        if self.w_rb_plusY.isChecked():
            camera = self.vtk_renderer.GetActiveCamera()
            x_min, x_max, y_min, y_max, z_min, z_max = self._get_viewing_bounds()
            center = [(x_min + x_max) / 2.0, (y_min + y_max) / 2.0, (z_min + z_max) / 2.0]

            x_length = x_max - x_min
            y_length = y_max - y_min
            z_length = z_max - z_min
            max_length = max(x_length, y_length, z_length)

            camera.SetPosition(center[0], y_max + max_length, center[2])
            camera.SetFocalPoint(center[0], center[1], center[2])
            camera.SetViewUp(0, 0, 1)
            camera.SetParallelProjection(True)
            self.vtk_renderer.ResetCameraClippingRange()
            self.vtk_renderer.ResetCamera()
            self.vtk_render_window.Render()

    def set_camera_to_minus_y(self):
        self.logger.debug("Camera position for 3D visual scene set to view from -Y in MainWindow")
        if self.w_rb_minusY.isChecked():
            camera = self.vtk_renderer.GetActiveCamera()
            x_min, x_max, y_min, y_max, z_min, z_max = self._get_viewing_bounds()
            center = [(x_min + x_max) / 2.0, (y_min + y_max) / 2.0, (z_min + z_max) / 2.0]

            x_length = x_max - x_min
            y_length = y_max - y_min
            z_length = z_max - z_min
            max_length = max(x_length, y_length, z_length)

            camera.SetPosition(center[0], y_min - max_length, center[2])
            camera.SetFocalPoint(center[0], center[1], center[2])
            camera.SetViewUp(0, 0, 1)
            camera.SetParallelProjection(True)
            self.vtk_renderer.ResetCameraClippingRange()
            self.vtk_renderer.ResetCamera()
            self.vtk_render_window.Render()

    def set_camera_to_plus_z(self):
        self.logger.debug("Camera position for 3D visual scene set to view from +Z in MainWindow")
        if self.w_rb_plusZ.isChecked():
            camera = self.vtk_renderer.GetActiveCamera()
            x_min, x_max, y_min, y_max, z_min, z_max = self._get_viewing_bounds()
            center = [(x_min + x_max) / 2.0, (y_min + y_max) / 2.0, (z_min + z_max) / 2.0]

            x_length = x_max - x_min
            y_length = y_max - y_min
            z_length = z_max - z_min
            max_length = max(x_length, y_length, z_length)

            camera.SetPosition(center[0], center[1], z_max + max_length)
            camera.SetFocalPoint(center[0], center[1], center[2])
            camera.SetViewUp(0, -1, 0)
            camera.SetParallelProjection(True)
            self.vtk_renderer.ResetCameraClippingRange()
            self.vtk_renderer.ResetCamera()
            self.vtk_render_window.Render()

    def set_camera_to_minus_z(self):
        self.logger.debug("Camera position for 3D visual scene set to view from -Z in MainWindow")
        if self.w_rb_minusZ.isChecked():
            camera = self.vtk_renderer.GetActiveCamera()
            x_min, x_max, y_min, y_max, z_min, z_max = self._get_viewing_bounds()
            center = [(x_min + x_max) / 2.0, (y_min + y_max) / 2.0, (z_min + z_max) / 2.0]

            x_length = x_max - x_min
            y_length = y_max - y_min
            z_length = z_max - z_min
            max_length = max(x_length, y_length, z_length)

            camera.SetPosition(center[0], center[1], z_min - max_length)
            camera.SetFocalPoint(center[0], center[1], center[2])
            camera.SetViewUp(0, -1, 0)
            camera.SetParallelProjection(True)
            self.vtk_renderer.ResetCameraClippingRange()
            self.vtk_renderer.ResetCamera()
            self.vtk_render_window.Render()


        pass

if __name__ == '__main__':
    if not os.path.exists(r'.\logs'):
        os.mkdir(r'.\logs', 777)

    logger = logging.getLogger('MapApp')
    logger.setLevel(logging.DEBUG)

    # create file handler which logs even debug messages
    log_file_name = f".\\logs\\{dt.datetime.now().strftime("%Y%m%d")}.log"
    fh = logging.FileHandler(log_file_name)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(levelname)s - %(asctime)s - [%(process)d] - %(name)s.%(funcName)s - [%(lineno)d] -  %(message)s')

    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    logger.info("Starting the MapApp Application")

    # from qt_material import apply_stylesheet

    app = qtw.QApplication(sys.argv)
    main_window = MainWindow()

    # apply_stylesheet(app, theme='dark_blue.xml')

    main_window.show()
    sys.exit(app.exec())