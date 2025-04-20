import sys
import json
import base64
import binascii
import numpy as np

import vtk

import PySide6.QtCore as qtc
import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg
import pyqtgraph as pg

# from ui.test_window import Ui_MainWindow
from ui.main_window import Ui_MainWindow
from diag_orient import OrientDialog
from diag_settings import SettingsDialog
from models.maprt import MapRTAPIManager, MapRTContext
from models.dicom import PatientContext, DicomFileValidationError
from models.settings import AppSettings

import resource_rc

class MainWindow(qtw.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        print('MainWindow.__init__')
        self.setupUi(self)

        self._load_application_settings()

        self.setWindowTitle("Map App")
        self._construct_menu_actions()
        self.w_tw_patient_settings.setCurrentIndex(0)
        self.w_tw_visualizations.setCurrentIndex(1)


        self._setup_patient_context()

        # "https://maprtpkr.adventhealth.com:5000"
        # "82212e3b-7edb-40e4-b346-c4fe806a1a0b"
        # "VisionRT.Integration.Saturn/1.2.8"

        # Setup the global MapRT API connection manager
        self.maprt_api = MapRTAPIManager(self.maprt_api_url,
                                         self.maprt_api_token,
                                         self.maprt_api_user_agent
                                         )
        self._connect_api_manager_to_ui()

        self._setup_maprt_context()

        # # Connect PatientContext to MapRTContext
        # self.patient_ctx.current_plan_changed.connect(self.maprt_ctx.update_plan_context)

        self._setup_collision_map_plot()

        # VTK rendering setup
        # self.maprt_actor = None
        # self.maprt_laser_actors = None
        # self.dicom_actor = None
        # self.dicom_laser_actors = None

        self._setup_3d_visualization()

    ####################################################################################
    # Setup                                                                            #
    ####################################################################################
    def testing(self):
        print('MainWindow.testing')

    def _load_application_settings(self):
        print('MainWindow._load_application_settings')
        with open(r'.\settings.json', 'r') as settings:
            settings_data = json.load(settings)
            self.settings = AppSettings(**settings_data)

            self.dicom_data_directory = self.settings.dicom.dicom_data_directory
            self.arc_check_resolution = self.settings.dicom.arc_check_resolution

            self.maprt_api_url = self.settings.maprt.api_url
            self.maprt_api_token = binascii.unhexlify(base64.b64decode(self.settings.maprt.api_token.encode('utf-8'))).decode('utf-8')
            self.maprt_api_user_agent = self.settings.maprt.api_user_agent

    def _setup_patient_context(self):
        print('MainWindow._setup_patient_context')
        # Setup the global PatientContext and PlanContext objects
        self.patient_ctx = PatientContext()

        self.w_pb_esapi_search.clicked.connect(self.testing)

        # PatientContext specific Signals
        self.patient_ctx.patient_id_changed.connect(self.w_le_patinet_id.setText)
        self.patient_ctx.patient_first_name_changed.connect(self.w_l_patient_first_name.setText)
        self.patient_ctx.patient_last_name_changed.connect(self.w_l_patient_last_name.setText)
        self.patient_ctx.courses_updated.connect(self.ui_update_courses)
        self.patient_ctx.plans_updated.connect(self.ui_update_plans)
        self.patient_ctx.plans_updated.connect(self.ui_enable_load_structure_button)
        self.patient_ctx.invalid_file_loaded.connect(self.ui_show_info_message)

        # PatientContext.current_plan (PlanContext) specific Signals
        self.patient_ctx.current_plan.isocenter_changed.connect(self.ui_update_isocenter_label)
        self.patient_ctx.current_plan.invalid_file_loaded.connect(self.ui_show_info_message)
        self.patient_ctx.current_plan.beams_changed.connect(self.ui_update_beam_table)
        self.patient_ctx.current_plan.redraw_beams.connect(self.ui_update_beam_plots)
        self.patient_ctx.current_plan.structures_updated.connect(self.ui_update_structures)
        self.patient_ctx.current_plan.current_structure_changed.connect(self.update_dicom_visualization)

        # ui to PatientContext or PlanContext method connections
        self.w_cb_body_structure.currentTextChanged.connect(self.patient_ctx.current_plan.update_current_structure)

        # Set ui to ui connections for DICOM RT file mode
        self.w_pb_dcm_plan_file.clicked.connect(self.ui_select_dicom_rt_plan_file)
        self.w_pb_dcm_struct_file.clicked.connect(self.ui_select_dicom_rt_structure_file)
        self.w_gb_dicomrt_files.setVisible(self.w_ch_use_dicomrt.isChecked())
        self.w_ch_use_dicomrt.checkStateChanged.connect(self.show_dicomrt_file_input_widgets)

    def _connect_api_manager_to_ui(self):
        print('MainWindow._connect_api_manager_to_ui')
        # Connect the ui signals to the MapRTAPIManager objects methods
        self.w_pb_fetch_api_data.clicked.connect(self.fetch_api_data)
        self.w_pb_get_map.clicked.connect(self.get_maprt_collision_maps)

    def _setup_maprt_context(self):
        print('MainWindow._setup_maprt_context')
        # Setup the global MapRTContext object
        self.maprt_ctx = MapRTContext(self.maprt_api)

        # Connect the MapRTContext specific Signals to the ui
        self.maprt_ctx.api_status_changed.connect(self.w_l_api_status.setText)
        self.maprt_ctx.treatment_rooms_updated.connect(self.ui_update_maprt_treatment_rooms)
        self.maprt_ctx.patient_surfaces_updated.connect(self.ui_update_maprt_surfaces)
        self.maprt_ctx.collision_maps_updated.connect(self.ui_update_maprt_collision_maps)
        self.maprt_ctx.current_surface_changed.connect(self.ui_update_map_surface_visualization)
        self.maprt_ctx.current_map_data_changed.connect(self.ui_update_collision_map_graphics_view)
        self.maprt_ctx.api_connection_error.connect(self.ui_notify_connection_error)

        self.maprt_ctx.current_map_data_changed.connect(self.patient_ctx.current_plan.validate_beams)

        # Connect the ui signals to the MapRTContext objects methods
        self.w_dsb_api_couch_buffer.valueChanged.connect(self.maprt_ctx.update_couch_buffer)
        self.w_dsb_api_patient_buffer.valueChanged.connect(self.maprt_ctx.update_patient_buffer)
        self.w_cb_current_map.currentTextChanged.connect(self.maprt_ctx.update_current_map_data)
        self.w_pb_obj_file.clicked.connect(self.ui_select_maprt_surface_file)
        self.w_cb_surface_for_map.currentTextChanged.connect(self.maprt_ctx.update_surface)
        self.w_cb_treatment_room.currentTextChanged.connect(self.maprt_ctx.update_room)

        # Connect PatientContext to MapRTContext
        self.patient_ctx.current_plan_changed.connect(self.maprt_ctx.update_plan_context)

    def _setup_collision_map_plot(self):
        print('MainWindow._setup_collision_map_plot')
        self.collision_map = None

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
        print('MainWindow._setup_3d_visualization')
        self.maprt_actor = None
        self.maprt_laser_actors = None
        self.dicom_actor = None
        self.dicom_laser_actors = None

        # 3D Scene Widget Setup
        self.vtk_renderer = vtk.vtkRenderer()
        self.vtk_render_window = self.vtk_widget.GetRenderWindow()
        self.vtk_render_window.AddRenderer(self.vtk_renderer)
        self.vtk_interactor = self.vtk_widget.GetRenderWindow().GetInteractor()
        # self.vtk_interactor.render_window = self.vtk_render_window
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

        # Setup MapRT obj actor color controls
        self.w_pb_laser_color.clicked.connect(self.laser_color_changed)
        self.w_fr_laser_color.setStyleSheet(f"background-color: rgb({255}, {0}, {0});")
        self.w_fr_laser_color.show()
        self.w_hs_laser_opacity.valueChanged.connect(self.laser_opacity_changed)

        # Connect image save button
        self.w_pb_save_image.clicked.connect(self.save_3d_image)

        # Connect view manipulation radiobuttons
        self.w_rb_plusX.toggled.connect(self.set_camera_to_plus_x)
        self.w_rb_minusX.toggled.connect(self.set_camera_to_minus_x)
        self.w_rb_plusY.toggled.connect(self.set_camera_to_plus_y)
        self.w_rb_minusY.toggled.connect(self.set_camera_to_minus_y)
        self.w_rb_plusZ.toggled.connect(self.set_camera_to_plus_z)
        self.w_rb_minusZ.toggled.connect(self.set_camera_to_minus_z)

        # Create axes actor
        axes_actor = vtk.vtkAxesActor()

        # Create orientation marker widget
        self.orientation_widget = vtk.vtkOrientationMarkerWidget()
        self.orientation_widget.SetOutlineColor(0.9300, 0.5700, 0.1300)
        self.orientation_widget.SetOrientationMarker(axes_actor)
        self.orientation_widget.SetInteractor(self.vtk_interactor)
        self.orientation_widget.SetViewport(0.0, 0.0, 0.2, 0.2)  # Set size and position
        self.orientation_widget.EnabledOn()
        self.orientation_widget.InteractiveOff()
        self.orientation_widget.On()

        self.cam_orient_manipulator = vtk.vtkCameraOrientationWidget(parent_renderer=self.vtk_renderer,
                                                                interactor=self.vtk_interactor)
        # Enable the widget.
        self.cam_orient_manipulator.On()

        self.vtk_interactor.Initialize()
        self.vtk_widget.show()

    def _construct_menu_actions(self):
        print('MainWindow._construct_menu_actions')
        menu_bar = self.menuBar()
        menu_file = menu_bar.addMenu("&File")

        action_exit = qtg.QAction("E&xit", self)
        action_exit.triggered.connect(self.close)
        menu_file.addAction(action_exit)

        menu_options = menu_bar.addMenu("&Options")

        action_settings = qtg.QAction("&Settings", self)
        action_settings.triggered.connect(self.show_settings_dialog)
        menu_options.addAction(action_settings)

    ####################################################################################
    # PatientContext Connections and Methods                                           #
    ####################################################################################

    def ui_update_courses(self, courses):
        print('MainWindow.ui_update_courses')
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
        print('MainWindow.ui_update_plans')
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
        print('MainWindow.ui_update_isocenter_label')
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
        print('MainWindow.ui_update_beam_table')
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
        print('MainWindow.ui_update_structures')
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

    def show_dicomrt_file_input_widgets(self):
        print('MainWindow.show_dicomrt_file_input_widgets')
        self.patient_ctx.clear()
        self.ui_clear_patient_context_widgets()
        self.ui_clear_dicom_3d_scene()

    def ui_select_dicom_rt_plan_file(self):
        print('MainWindow.ui_select_dicom_rt_plan_file')
        file_path, _ = qtw.QFileDialog.getOpenFileName(self,
                                                      "Select DICOM Structureset File",
                                                      self.dicom_data_directory,
                                                      "DICOM Files (*.dcm)"
                                                      )
        if file_path:
            try:
                self.patient_ctx.load_context_from_dicom_rt_file(file_path)
                self.w_le_dcm_plan_file.setText(file_path)

            except DicomFileValidationError as e:
                self.dicomrt_plan_model = None
                print(e)

    def ui_enable_load_structure_button(self):
        print('MainWindow.ui_enable_load_structure_button')
        self.w_pb_dcm_struct_file.setEnabled(True)

    def ui_select_dicom_rt_structure_file(self):
        print('MainWindow.ui_select_dicom_rt_structure_file')
        file_path, _ = qtw.QFileDialog.getOpenFileName(self,
                                                       "Select DICOM Structureset File",
                                                       self.dicom_data_directory,
                                                       "DICOM Files (*.dcm)"
                                                       )
        if file_path:
            try:
                self.patient_ctx.current_plan.load_structures_from_dicom_rt_file(file_path)
                # self.dicomrt_plan_model.invalid_file_loaded.connect(self.show_info_message)
                # self.dicomrt_plan_model.file_path_changed.connect(self.w_le_dcm_plan_file.setText)
                # self.dicomrt_plan_model.plan_model_updated.connect(self.update_patient_context_from_dicom)
                #
                # self.dicomrt_plan_model.structure_set.invalid_file_loaded.connect(self.show_info_message)
                # self.dicomrt_plan_model.structure_set.file_path_changed.connect(self.w_le_dcm_struct_file.setText)
                # self.dicomrt_plan_model.structure_set.vtk_actor_updated.connect(self.update_dcm_visualization)
                # self.dicomrt_plan_model.structure_set.structures_loaded.connect(self.update_structure_selections)
                # self.w_cb_body_structure.currentTextChanged.connect(self.update_dcm_body_structure)

                self.w_le_dcm_struct_file.setText(file_path)
            except DicomFileValidationError as e:
                self.dicomrt_plan_model = None
                print(e)

    def update_dicom_visualization(self, model):
        print('MainWindow.update_dicom_visualization')
        if self.dicom_actor is None:
            self.dicom_actor = self.patient_ctx.current_plan.current_structure

            R, G, B, A = self._get_current_color(self.w_fr_dcm_color)
            self.dicom_actor.GetProperty().SetColor(R / 255.0, G / 255.0, B / 255.0)
            self.dicom_actor.property.opacity = self.w_hs_dcm_opacity.value() / 100.0

            self.dicom_laser_actors = self._get_laser_marks(self.dicom_actor.GetMapper().GetInput())

            laser_R, laser_G, laser_B, laser_A = self._get_current_color(self.w_fr_laser_color)
            for laser_actor in self.dicom_laser_actors:
                laser_actor.GetProperty().SetColor(laser_R / 255.0, laser_G / 255.0, laser_B / 255.0)
                laser_actor.property.opacity = self.w_hs_laser_opacity.value() / 100.0

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
                laser_actor.property.opacity = self.w_hs_laser_opacity.value() / 100.0

            self.vtk_renderer.AddActor(self.dicom_actor)
            for laser_actor in self.dicom_laser_actors:
                self.vtk_renderer.AddActor(laser_actor)
            self.vtk_renderer.ResetCamera()

        self.vtk_render_window.Render()

    def dicom_surface_color_changed(self):
        print('MainWindow.dicom_surface_color_changed')
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
        print('MainWindow.dicom_surface_opacity_changed')
        self.w_l_dcm_opacity.setText(str(self.w_hs_dcm_opacity.value()))
        if self.dicom_actor is not None:
            self.dicom_actor.property.opacity = self.w_hs_dcm_opacity.value() / 100.0
            self.vtk_render_window.Render()
        else:
            pass

    def ui_clear_patient_context_widgets(self):
        print('MainWindow.ui_clear_patient_context_widgets')
        self.w_le_dcm_plan_file.clear()
        self.w_le_dcm_struct_file.clear()
        self.w_pb_dcm_struct_file.setEnabled(False)
        self.w_pb_esapi_search.setEnabled(not self.w_ch_use_dicomrt.isChecked())
        self.w_le_patinet_id.setEnabled(not self.w_ch_use_dicomrt.isChecked())
        self.w_cb_course_id.setEnabled(not self.w_ch_use_dicomrt.isChecked())
        self.w_cb_plan_id.setEnabled(not self.w_ch_use_dicomrt.isChecked())
        self.w_gb_dicomrt_files.setVisible(self.w_ch_use_dicomrt.isChecked())

    def ui_clear_dicom_3d_scene(self):
        print('MainWindow.ui_clear_dicom_3d_scene')
        if self.dicom_actor is not None:
            self.vtk_renderer.RemoveActor(self.dicom_actor)
            for laser_actor in self.dicom_laser_actors:
                self.vtk_renderer.RemoveActor(laser_actor)
            self.vtk_render_window.Render()
            self.dicom_actor = None
            self.dicom_laser_actors = None

    ####################################################################################
    # MapRTContext Connections and Methods                                             #
    ####################################################################################

    def fetch_api_data(self):
        print('MainWindow.fetch_api_data')
        self.maprt_api.get_status()
        self.maprt_api.get_treatment_rooms()
        self.maprt_api.get_patient_surfaces(self.patient_ctx.patient_id)
        self.w_pb_get_map.setEnabled(True)

    def get_maprt_collision_maps(self):
        print('MainWindow.get_maprt_collision_maps')
        self.maprt_api.get_map(self.maprt_ctx)

    def ui_update_maprt_treatment_rooms(self, rooms):
        print('MainWindow.ui_update_maprt_treatment_rooms')
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
        print('MainWindow.ui_update_maprt_surfaces')
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
        print('MainWindow.ui_update_maprt_collision_maps')
        if self.w_cb_current_map.count() == 0:
            self.w_cb_current_map.addItems(maps)
        else:
            self.w_cb_current_map.blockSignals(True)
            self.w_cb_current_map.clear()
            self.w_cb_current_map.blockSignals(False)
            self.w_cb_current_map.addItems(maps)
            self.w_cb_current_map.setCurrentText(self.maprt_ctx.current_map_label)

    def ui_update_map_surface_visualization(self, surface):
        print('MainWindow.ui_update_map_surface_visualization')
        if self.maprt_actor is None:

            self.maprt_surface_mapper = vtk.vtkPolyDataMapper()
            self.maprt_ctx.current_surface.vtk_polydata >> self.maprt_surface_mapper

            self.maprt_actor = vtk.vtkActor(mapper=self.maprt_surface_mapper)

            self.maprt_transform = vtk.vtkTransform()
            self.maprt_actor.SetUserTransform(self.maprt_transform)

            R, G, B, A = self._get_current_color(self.w_fr_obj_color)
            self.maprt_actor.GetProperty().SetColor(R / 255.0, G / 255.0, B / 255.0)
            self.maprt_actor.property.opacity = self.w_hs_obj_opacity.value() / 100.0

            self.maprt_laser_actors = self._get_laser_marks(self.maprt_actor.GetMapper().GetInput())

            laser_R, laser_G, laser_B, laser_A = self._get_current_color(self.w_fr_laser_color)
            for laser_actor in self.maprt_laser_actors:
                laser_actor.GetProperty().SetColor(laser_R / 255.0, laser_G / 255.0, laser_B / 255.0)
                laser_actor.property.opacity = self.w_hs_laser_opacity.value() / 100.0

            self.vtk_renderer.AddActor(self.maprt_actor)
            for laser_actor in self.maprt_laser_actors:
                self.vtk_renderer.AddActor(laser_actor)
            self.vtk_renderer.ResetCamera()
        else:
            self.vtk_renderer.RemoveActor(self.maprt_actor)
            for laser_actor in self.maprt_laser_actors:
                self.vtk_renderer.RemoveActor(laser_actor)

            self.maprt_surface_mapper = vtk.vtkPolyDataMapper()
            self.maprt_ctx.current_surface.vtk_polydata >> self.maprt_surface_mapper

            self.maprt_actor = vtk.vtkActor(mapper=self.maprt_surface_mapper)

            self.maprt_transform = vtk.vtkTransform()
            self.maprt_actor.SetUserTransform(self.maprt_transform)

            R, G, B, A = self._get_current_color(self.w_fr_obj_color)
            self.maprt_actor.GetProperty().SetColor(R / 255.0, G / 255.0, B / 255.0)
            self.maprt_actor.property.opacity = self.w_hs_obj_opacity.value() / 100.0

            self.maprt_laser_actors = self._get_laser_marks(self.maprt_actor.GetMapper().GetInput())

            laser_R, laser_G, laser_B, laser_A = self._get_current_color(self.w_fr_laser_color)
            for laser_actor in self.maprt_laser_actors:
                laser_actor.GetProperty().SetColor(laser_R / 255.0, laser_G / 255.0, laser_B / 255.0)
                laser_actor.property.opacity = self.w_hs_laser_opacity.value() / 100.0

            self.vtk_renderer.AddActor(self.maprt_actor)
            for laser_actor in self.maprt_laser_actors:
                self.vtk_renderer.AddActor(laser_actor)
            self.vtk_renderer.ResetCamera()

        self.vtk_render_window.Render()

    def ui_update_collision_map_graphics_view(self, current_map_data):
        print('MainWindow.ui_update_collision_map_graphics_view')
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
        print('MainWindow.ui_update_beam_plots')
        arcs, static_beams = beam_plot_items
        for arc in arcs:
            arc.setZValue(25)
            self.collision_map_plot_widget.addItem(arc)
        for static_beam in static_beams:
            static_beam.setZValue(25)
            self.collision_map_plot_widget.addItem(static_beam)

    def ui_notify_connection_error(self, message):
        print('MainWindow.ui_notify_connection_error')
        qtw.QMessageBox.critical(self, "MapRT API Error", message, qtw.QMessageBox.Ok)

    def ui_select_maprt_surface_file(self):
        print('MainWindow.ui_select_maprt_surface_file')
        file_path, _ = qtw.QFileDialog.getOpenFileName(self,
                                                      "Select MapRT .obj Surface File",
                                                      ".",
                                                      "OBJ Files (*.obj)"
                                                      )
        if file_path:
            dialog = OrientDialog()
            if dialog.exec() == qtw.QDialog.DialogCode.Accepted:
                _orientation = dialog.w_cb_obj_surface_orientation.currentText()
                if _orientation == "Current Plan" and self.patient_ctx.current_plan is not None:
                    self.maprt_ctx.load_surface_file(file_path, self.patient_ctx.current_plan.patient_orientation)

                else:
                    self.maprt_ctx.load_surface_file(file_path, _orientation)

                if self.collision_map is not None:
                    self.collision_map_view_box.removeItem(self.collision_map)

    def collision_map_mouse_moved(self, event):
        # print('MainWindow.collision_map_mouse_moved')
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
        print('MainWindow.maprt_surface_color_changed')
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
        print('MainWindow.maprt_surface_opacity_changed')
        self.w_l_obj_opacity.setText(str(self.w_hs_obj_opacity.value()))
        if self.maprt_actor is not None:
            self.maprt_actor.property.opacity = self.w_hs_obj_opacity.value() / 100.0
            self.vtk_render_window.Render()
        else:
            pass

    ####################################################################################
    # ui manipulation methods                                                          #
    ####################################################################################

    def show_settings_dialog(self):
        print('MainWindow.show_settings_dialog')
        settings_dialog = SettingsDialog()

        if settings_dialog.exec():
            print("writing settings")

            self.dicom_data_directory = settings_dialog.w_le_dicom_directory.text()
            self.arc_check_resolution = settings_dialog.w_sb_arc_check_resolution.value()
            self.maprt_api.api_url = settings_dialog.w_le_api_url.text()
            self.maprt_api.token = settings_dialog.w_le_api_token.text()
            self.maprt_api.user_agent = settings_dialog.w_le_api_user_agent.text()

            self.settings.dicom.dicom_data_directory = self.dicom_data_directory
            self.settings.dicom.arc_check_resolution = self.arc_check_resolution

            self.settings.maprt.api_url =  self.maprt_api.api_url
            hidden_token = base64.b64encode(binascii.hexlify(self.maprt_api.token.encode('utf-8'))).decode('utf-8')
            self.settings.maprt.api_token = hidden_token
            self.settings.maprt.api_user_agent =  self.maprt_api.user_agent

            with open('settings.json', 'w') as settings:
                settings.write(self.settings.model_dump_json(indent=4))
        else:
            print("ignoring settings changes")

    def ui_show_info_message(self, message):
        print('MainWindow.ui_show_info_message')
        qtw.QMessageBox.information(self, "Information", message, qtw.QMessageBox.Ok)

    def _get_laser_marks(self, polydata):
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
        xy_cut_actor = vtk.vtkActor()
        xy_cut_actor.SetMapper(xy_cut_mapper)
        xy_cut_actor.GetProperty().SetColor(1, 0, 0)  # Red color for the cut surface

        yz_cut_mapper = vtk.vtkPolyDataMapper()
        yz_cut_mapper.SetInputData(yz_glyphFilter.GetOutput())
        yz_cut_actor = vtk.vtkActor()
        yz_cut_actor.SetMapper(yz_cut_mapper)
        yz_cut_actor.GetProperty().SetColor(1, 0, 0)  # Red color for the cut surface

        zx_cut_mapper = vtk.vtkPolyDataMapper()
        zx_cut_mapper.SetInputData(zx_glyphFilter.GetOutput())
        zx_cut_actor = vtk.vtkActor()
        zx_cut_actor.SetMapper(zx_cut_mapper)
        zx_cut_actor.GetProperty().SetColor(1, 0, 0)  # Red color for the cut surface

        return (xy_cut_actor, yz_cut_actor, zx_cut_actor)

    def laser_color_changed(self):
        print('MainWindow.laser_color_changed')
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
        print('MainWindow.laser_transparency_changed')
        self.w_l_laser_opacity.setText(str(self.w_hs_laser_opacity.value()))
        if self.maprt_actor is not None:
            for laser_actor in self.maprt_laser_actors:
                laser_actor.property.opacity = self.w_hs_laser_opacity.value() / 100.0
            self.vtk_render_window.Render()

        if self.dicom_actor is not None:
            for laser_actor in self.dicom_laser_actors:
                laser_actor.property.opacity = self.w_hs_laser_opacity.value() / 100.0
            self.vtk_render_window.Render()

    def _get_current_color(self, frame):
        print('MainWindow._get_current_color')
        palette = frame.palette()
        background_color = palette.color(qtg.QPalette.ColorRole.Window)
        return background_color.getRgb()

    def _get_viewing_bounds(self):
        print('MainWindow._get_viewing_bounds')
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

    def vtk_render_window_background_color_changed(self):
        print('MainWindow.vtk_render_window_background_color_changed')
        _R, _G, _B, _A = self._get_current_color(self.w_fr_background_color)
        color = qtw.QColorDialog.getColor(qtg.QColor(_R, _G, _B), self, "Select Color")

        if color.isValid():
            R, G, B, A = color.getRgb()
            self.w_fr_background_color.setStyleSheet(f"background-color: rgb({R}, {G}, {B});")
            self.w_fr_background_color.show()

            self.vtk_renderer.SetBackground(R/255.0, G/255.0, B/255.0)
            self.vtk_render_window.Render()

    def save_3d_image(self):
        print('MainWindow.save_3d_image')
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
        print('MainWindow.set_camera_to_plus_x')
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
            self.vtk_render_window.Render()

    def set_camera_to_minus_x(self):
        print('MainWindow.set_camera_to_minus_x')
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
            self.vtk_render_window.Render()

    def set_camera_to_plus_y(self):
        print('MainWindow.set_camera_to_plus_y')
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
            self.vtk_render_window.Render()

    def set_camera_to_minus_y(self):
        print('MainWindow.set_camera_to_minus_y')
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
            self.vtk_render_window.Render()

    def set_camera_to_plus_z(self):
        print('MainWindow.set_camera_to_plus_z')
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
            self.vtk_render_window.Render()

    def set_camera_to_minus_z(self):
        print('MainWindow.set_camera_to_minus_z')
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
            self.vtk_render_window.Render()


        pass

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())