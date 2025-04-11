import sys
import inspect
import numpy as np

import vtk

import PySide6.QtCore as qtc
import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg
import pyqtgraph as pg

# from ui.test_window import Ui_MainWindow
from ui.main_window import Ui_MainWindow
from models.dicom import DicomRTPlan, DicomFileValidationError
from models.obj import Surface
from models.maprt_api import MapRTCaller

class MainWindow(qtw.QMainWindow, Ui_MainWindow):
    def __init__(self):
        # print('MainWindow Function: ', inspect.stack()[0][3])
        # print('\tCaller: ', inspect.stack()[1][3])

        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Map App")
        self.w_tw_patient_settings.setCurrentIndex(0)
        self.w_tw_visualizations.setCurrentIndex(1)

        # TEST Code for Collision Map

        self.collision_map = None
        layout = qtw.QHBoxLayout(self.w_gb_collision_map)

        self.map_lut = np.array([[175, 15, 15], [41,48, 66]], dtype=np.uint8)
        # self.map_view = pg.ImageItem(axisOrder='row-major')
        # self.map_view.setZValue(0)
        # self.map_view.setLookupTable(self.map_lut)

        self.plot_widget = pg.PlotWidget()
        self.view_box = self.plot_widget.getViewBox()
        self.view_box.setMouseEnabled(x=False, y=False)

        # Create crosshair lines
        self.v_line = pg.InfiniteLine(angle=90, movable=False)
        self.v_line.setZValue(10)
        self.h_line = pg.InfiniteLine(angle=0, movable=False)
        self.v_line.setZValue(11)
        self.view_box.addItem(self.v_line, ignoreBounds=True)
        self.view_box.addItem(self.h_line, ignoreBounds=True)

        # self.plot_widget.addItem(self.map_view)
        self.plot_widget.showAxes(True)
        self.plot_widget.invertY(True)

        # proxy = pg.SignalProxy(app.desktop().eventFilter, rateLimit=60, slot=mouse_moved)
        self.view_box.scene().sigMouseMoved.connect(self.mouse_moved)

        layout.addWidget(self.plot_widget)

        # TEST Code for Collision Map


        # OBJ File Widget Setup
        self.obj_model = Surface()
        self.obj_model.file_path_changed.connect(self.w_le_obj_file.setText)
        self.obj_model.vtk_actor_updated.connect(self.update_obj_visualization)

        self.maprt_caller = MapRTCaller("https://maprtpkr.adventhealth.com:5000",
                                        "82212e3b-7edb-40e4-b346-c4fe806a1a0b",
                                        "VisionRT.Integration.Saturn/1.2.8"
                                        )
        self.w_pb_api_ping.clicked.connect(self._update_api_status)
        self.maprt_caller.maprt_treatment_rooms_updated.connect(self._update_maprt_treatment_rooms)
        self.maprt_caller.maprt_surfaces_updated.connect(self._update_maprt_surfaces)
        self.w_cb_surface_for_map.currentTextChanged.connect(self.get_surface_from_api)
        self._update_api_status()
        if self.maprt_caller.get_status() == 200:
            self.maprt_caller.get_all_treatment_rooms()

        self.active_map = None
        self.w_pb_get_map.clicked.connect(self.display_map)

        # VTK rendering setup
        self.dcm_actor = None
        self.obj_actor = None

        # 3D Scene Widget Setup
        self.vtk_renderer = vtk.vtkRenderer()
        self.vtk_render_window = self.vtk_widget.GetRenderWindow()
        self.vtk_render_window.AddRenderer(self.vtk_renderer)
        self.vtk_interactor = self.vtk_widget.GetRenderWindow().GetInteractor()
        self.vtk_interactor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())

        # Patient Context Widget Setup
        ## DICOM RT File Widget Setup
        self.dicomrt_plan_model = None

        self.w_gb_dicomrt_files.setVisible(self.w_ch_use_dicomrt.isChecked())
        self.w_ch_use_dicomrt.checkStateChanged.connect(self.show_dicomrt_file_input_widgets)
        self.w_ch_use_dicomrt.checkStateChanged.connect(self._clear_patient_context)

        self.w_pb_dcm_plan_file.clicked.connect(self.open_dcm_plan_file)
        self.w_pb_dcm_struct_file.clicked.connect(self.open_dcm_struct_file)

        self.w_pb_dcm_color.clicked.connect(self.dcm_color_changed)
        self.w_fr_dcm_color.setStyleSheet(f"background-color: rgb({0}, {127}, {0});")
        self.w_fr_dcm_color.show()
        self.w_hs_dcm_transparency.valueChanged.connect(self.dcm_transparency_changed)

        #OBJ Code

        self.w_gb_obj_file.setVisible(self.w_ch_use_obj.isChecked())
        self.w_ch_use_obj.checkStateChanged.connect(self.show_obj_file_input_widgets)
        self.w_pb_obj_file.clicked.connect(self.open_obj_file)

        self.w_fr_obj_color.setStyleSheet(f"background-color: rgb({127}, {127}, {127});")
        self.w_fr_obj_color.show()
        self.w_pb_obj_color.clicked.connect(self.obj_color_changed)
        self.w_hs_obj_transparency.valueChanged.connect(self.obj_transparency_changed)

        self.w_rb_hfs.toggled.connect(self.orientation_changed)
        self.w_rb_hfp.toggled.connect(self.orientation_changed)
        self.w_rb_ffs.toggled.connect(self.orientation_changed)
        self.w_rb_ffp.toggled.connect(self.orientation_changed)

        self.w_pb_background_color.clicked.connect(self.background_color_changed)
        self.w_fr_background_color.setStyleSheet(f"background-color: rgb({0}, {0}, {0});")
        self.w_fr_background_color.show()

        self.w_pb_save_image.clicked.connect(self.save_image)

        self.w_rb_plusX.toggled.connect(self.set_camera_to_plus_x)
        self.w_rb_minusX.toggled.connect(self.set_camera_to_minus_x)
        self.w_rb_plusY.toggled.connect(self.sset_camera_to_plus_y)
        self.w_rb_minusY.toggled.connect(self.set_camera_to_minus_y)
        self.w_rb_plusZ.toggled.connect(self.set_camera_to_plus_z)
        self.w_rb_minusZ.toggled.connect(self.set_camera_to_minus_z)

        self.vtk_interactor.Initialize()
        self.vtk_widget.show()

    # Function to update crosshair and text position
    def mouse_moved(self, event):
        # print(evt)
        pos = event  # using signal proxy turns original event into tuple
        if self.view_box.sceneBoundingRect().contains(pos):
            mouse_point = self.view_box.mapSceneToView(pos)
            self.v_line.setPos(mouse_point.x())
            self.v_line.setZValue(10)
            self.h_line.setPos(mouse_point.y())
            self.h_line.setZValue(11)
            # self.text_item.setText(f"x={mouse_point.x():.2f}, y={mouse_point.y():.2f}")
            print(f"x={mouse_point.x():.2f}, y={mouse_point.y():.2f}")

    def display_map(self):
        map = self.maprt_caller.get_map(self.dicomrt_plan_model.isocenter,
                                        self.w_dsb_api_couch_buffer.value()*10,
                                        self.w_dsb_api_patient_buffer.value()*10,
                                        self.w_cb_surface_for_map.currentText(),
                                        self.w_cb_treatment_room.currentText(),
                                        self.w_ch_high_res.isChecked()
                                        )
        lst = map.split()
        new_str = ','.join(lst[1:-1])
        a = np.fromstring(new_str, dtype=int, sep=',')
        a = a.reshape((int(len(a)/3), 3))
        couch, gantry, isOK = a.T
        unique_couch = np.unique(couch)
        unique_gantry = np.unique(gantry)

        # print(unique_couch)
        # print(len(unique_couch))
        # print(unique_gantry)
        # print(len(unique_gantry))

        gantry_idx = np.hstack((unique_gantry[np.where(unique_gantry >= 180)],
                                unique_gantry[np.where(unique_gantry < 180)]
                                )
                               )

        couch_idx = np.hstack((unique_couch[np.where(unique_couch >= 180)],
                               unique_couch[np.where(unique_couch <= 90)]
                               )
                              )

        # print(couch_idx)
        # print(len(couch_idx))
        # print(gantry_idx)
        # print(len(gantry_idx))


        x_map = dict([(str(couch_idx[i]), i) for i in range(len(couch_idx))])
        y_map = dict([(str(gantry_idx[i]), i) for i in range(len(gantry_idx))])

        x_labels = [(i, str(couch_idx[i])) for i in np.arange(0, len(couch_idx), 10)]
        x_ticks = [x_labels]
        bottom_axis = self.plot_widget.getAxis('bottom')
        bottom_axis.setTicks(x_ticks)

        y_labels = [(j, str(gantry_idx[j])) for j in np.arange(0, len(gantry_idx), 10)]
        y_ticks = [y_labels]
        left_axis = self.plot_widget.getAxis('left')
        left_axis.setTicks(y_ticks)

        self.map_view = pg.ImageItem(axisOrder='row-major')
        self.map_view.setZValue(0)
        self.map_view.setLookupTable(self.map_lut)

        self.collision_map = np.zeros((len(gantry_idx), len(couch_idx)), dtype=int)
        for j in range(len(couch)):
            self.collision_map[y_map[str(gantry[j])], x_map[str(couch[j])]] = isOK[j]

        self.map_view.setImage(self.collision_map)
        self.plot_widget.addItem(self.map_view)



    def _update_api_status(self):
        # print('MainWindow Function: ', inspect.stack()[0][3])
        # print('\tCaller: ', inspect.stack()[1][3])

        status = self.maprt_caller.get_status()
        self.w_l_api_status.setText(f'{status}')

        # if status == 200:
        #     self.maprt_caller.get_all_treatment_rooms()

    def _update_maprt_surfaces(self, surface_map):
        # print('MainWindow Function: ', inspect.stack()[0][3])
        # print('\tCaller: ', inspect.stack()[1][3])

        self.w_cb_surface_for_map.clear()
        self.w_cb_surface_for_map.addItems(surface_map.keys())

    def get_surface_from_api(self):
        # print('MainWindow Function: ', inspect.stack()[0][3])
        # print('\tCaller: ', inspect.stack()[1][3])

        surface_label = self.w_cb_surface_for_map.currentText()
        if surface_label in self.maprt_caller._surface_map:
            self.obj_model.update_from_api(self.maprt_caller.get_surface(surface_label))

    def _update_maprt_treatment_rooms(self, room_map):
        # print('MainWindow Function: ', inspect.stack()[0][3])
        # print('\tCaller: ', inspect.stack()[1][3])

        self.w_cb_treatment_room.clear()
        self.w_cb_treatment_room.addItems(room_map.keys())

    def show_info_message(self, message):
        # print('MainWindow Function: ', inspect.stack()[0][3])
        # print('\tCaller: ', inspect.stack()[1][3])
        
        res = qtw.QMessageBox.information(self, "Information", message, qtw.QMessageBox.Ok)

    def show_dicomrt_file_input_widgets(self):
        # print('MainWindow Function: ', inspect.stack()[0][3])
        # print('\tCaller: ', inspect.stack()[1][3])

        self.w_le_dcm_plan_file.clear()
        self.w_le_dcm_struct_file.clear()
        self.w_pb_dcm_struct_file.setEnabled(False)
        self.w_pb_esapi_search.setEnabled(not self.w_ch_use_dicomrt.isChecked())
        self.w_le_patinet_id.setEnabled(not self.w_ch_use_dicomrt.isChecked())
        self.w_cb_plan_id.setEnabled(not self.w_ch_use_dicomrt.isChecked())
        self.w_gb_dicomrt_files.setVisible(self.w_ch_use_dicomrt.isChecked())

        if self.dcm_actor is not None:
            self.vtk_renderer.RemoveActor(self.dcm_actor)
            self.vtk_render_window.Render()
            self.dcm_actor = None

    def show_obj_file_input_widgets(self):
        # print('MainWindow Function: ', inspect.stack()[0][3])
        # print('\tCaller: ', inspect.stack()[1][3])

        self.w_le_obj_file.clear()
        self.w_gb_obj_file.setVisible(self.w_ch_use_obj.isChecked())

    def open_dcm_plan_file(self):
        # print('MainWindow Function: ', inspect.stack()[0][3])
        # print('\tCaller: ', inspect.stack()[1][3])

        filename, _ = qtw.QFileDialog.getOpenFileName(self,
                                                      "Select DICOM Structureset File",
                                                      ".",
                                                      "DICOM Files (*.dcm)"
                                                      )
        if filename:
            try:
                self._clear_patient_context()
                self.dicomrt_plan_model = DicomRTPlan()
                self.dicomrt_plan_model.invalid_file_loaded.connect(self.show_info_message)
                self.dicomrt_plan_model.file_path_changed.connect(self.w_le_dcm_plan_file.setText)
                self.dicomrt_plan_model.plan_model_updated.connect(self.update_patient_context_from_dicom)

                self.dicomrt_plan_model.structure_set.invalid_file_loaded.connect(self.show_info_message)
                self.dicomrt_plan_model.structure_set.file_path_changed.connect(self.w_le_dcm_struct_file.setText)
                self.dicomrt_plan_model.structure_set.vtk_actor_updated.connect(self.update_dcm_visualization)
                self.dicomrt_plan_model.structure_set.structures_loaded.connect(self.update_structure_selections)
                self.w_cb_body_structure.currentTextChanged.connect(self.update_dcm_body_structure)

                self.dicomrt_plan_model.filepath = filename
            except DicomFileValidationError as e:
                self.dicomrt_plan_model = None
                print(e)

    def _clear_patient_context(self):
        # print('MainWindow Function: ', inspect.stack()[0][3])
        # print('\tCaller: ', inspect.stack()[1][3])

        self.maprt_caller.clear()

        self.w_le_patinet_id.clear()
        self.w_l_patient_first_name.setText('')
        self.w_l_patient_last_name.setText('')

        self.w_cb_plan_id.clear()
        self.w_cb_plan_id.setEnabled(False)
        self.w_l_plan_isocenter.setText('')

        self.w_cb_body_structure.currentTextChanged.disconnect()
        self.w_cb_body_structure.clear()
        self.w_cb_body_structure.setEnabled(False)

        self.w_tw_beams.clear()
        self.w_tw_beams.setRowCount(0)
        self.w_tw_beams.setColumnCount(0)

        self.w_le_dcm_struct_file.clear()
        self.w_pb_dcm_struct_file.setEnabled(False)

        if self.dcm_actor is not None:
            self.vtk_renderer.RemoveActor(self.dcm_actor)
            self.vtk_render_window.Render()
            self.dcm_actor = None

    def update_patient_context_from_dicom(self, model):
        # print('MainWindow Function: ', inspect.stack()[0][3])
        # print('\tCaller: ', inspect.stack()[1][3])

        self.w_le_patinet_id.setText(model.patient_id)

        self.w_l_patient_first_name.setText(model.patient_first_name)
        self.w_l_patient_last_name.setText(model.patient_last_name)
        self.w_cb_plan_id.setEnabled(False)
        self.w_cb_plan_id.addItem(model.plan_id)
        self.w_cb_plan_id.setCurrentIndex(0)
        X, Y, Z = model.isocenter
        self.w_l_plan_isocenter.setText(f'< {X}, {Y}, {Z} >')

        self.w_tw_beams.setRowCount(len(model.beams))
        self.w_tw_beams.setColumnCount(len(model.beams[0]))
        self.w_tw_beams.setHorizontalHeaderLabels(["Status",
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

        for row_index, row_data in enumerate(model.beams):
            for col_index, cell_data in enumerate(row_data):
                item = qtw.QTableWidgetItem(cell_data)
                item.setTextAlignment(qtc.Qt.AlignmentFlag.AlignCenter)
                self.w_tw_beams.setItem(row_index, col_index, item)

        self.w_tw_beams.resizeColumnsToContents()
        self.w_tw_beams.setSortingEnabled(True)
        self.w_pb_dcm_struct_file.setEnabled(True)

        self.obj_model.patient_orientation = self.dicomrt_plan_model.patient_orientation
        self.maprt_caller.get_all_treatment_rooms()
        self.maprt_caller.get_surfaces_for_patient(model.patient_id)

    def open_dcm_struct_file(self):
        # print('MainWindow Function: ', inspect.stack()[0][3])
        # print('\tCaller: ', inspect.stack()[1][3])

        filename, _ = qtw.QFileDialog.getOpenFileName(self,
                                                      "Select DICOM Structureset File",
                                                      ".",
                                                      "DICOM Files (*.dcm)"
                                                      )
        if filename:
            self.dicomrt_plan_model.structure_set.update_filepath(filename)

    def update_structure_selections(self, model):
        # print('MainWindow Function: ', inspect.stack()[0][3])
        # print('\tCaller: ', inspect.stack()[1][3])

        self.w_cb_body_structure.addItems(model.structures)
        self.w_cb_body_structure.setEnabled(True)

    def update_dcm_body_structure(self):
        # print('MainWindow Function: ', inspect.stack()[0][3])
        # print('\tCaller: ', inspect.stack()[1][3])

        if self.w_cb_body_structure.currentText() in self.dicomrt_plan_model.structure_set.structures:
            self.dicomrt_plan_model.structure_set.get_body_mesh(self.w_cb_body_structure.currentText())

    def update_dcm_visualization(self, model):
        # print('MainWindow Function: ', inspect.stack()[0][3])
        # print('\tCaller: ', inspect.stack()[1][3])

        if self.dcm_actor is None:
            self.dcm_actor = model.dcm_body_actor

            R, G, B, A = self._get_current_color(self.w_fr_dcm_color)
            self.dcm_actor.GetProperty().SetColor(R / 255.0, G / 255.0, B / 255.0)
            self.dcm_actor.property.opacity = self.w_hs_dcm_transparency.value() / 100.0

            self.vtk_renderer.AddActor(self.dcm_actor)
            self.vtk_renderer.ResetCamera()
        else:
            self.vtk_renderer.RemoveActor(self.dcm_actor)
            self.dcm_actor = model.dcm_body_actor

            R, G, B, A = self._get_current_color(self.w_fr_dcm_color)
            self.dcm_actor.GetProperty().SetColor(R / 255.0, G / 255.0, B / 255.0)
            self.dcm_actor.property.opacity = self.w_hs_dcm_transparency.value() / 100.0

            self.vtk_renderer.AddActor(self.dcm_actor)
            self.vtk_renderer.ResetCamera()

        self.vtk_render_window.Render()

    def open_obj_file(self):
        # print('MainWindow Function: ', inspect.stack()[0][3])
        # print('\tCaller: ', inspect.stack()[1][3])

        filename, _ = qtw.QFileDialog.getOpenFileName(self,
                                                      "Select DICOM Structureset File",
                                                      ".",
                                                      "OBJ Files (*.obj)"
                                                      )
        if filename:
            # self.obj_model = Surface()
            self.view_box.removeItem(self.map_view)
            if self.dicomrt_plan_model is not None:
                self.obj_model.patient_orientation = self.dicomrt_plan_model.patient_orientation
            # self.obj_model.file_path_changed.connect(self.w_le_obj_file.setText)
            # self.obj_model.vtk_actor_updated.connect(self.update_obj_visualization)

            self.obj_model.filepath = filename

    def update_obj_visualization(self, model):
        # print('MainWindow Function: ', inspect.stack()[0][3])
        # print('\tCaller: ', inspect.stack()[1][3])

        print("in update_obj_visualization")
        if self.obj_actor is None:
            self.obj_actor = model.obj_actor

            R, G, B, A = self._get_current_color(self.w_fr_obj_color)
            self.obj_actor.GetProperty().SetColor(R / 255.0, G / 255.0, B / 255.0)
            self.obj_actor.property.opacity = self.w_hs_obj_transparency.value() / 100.0

            self.vtk_renderer.AddActor(self.obj_actor)
            self.vtk_renderer.ResetCamera()
        else:
            self.vtk_renderer.RemoveActor(self.obj_actor)
            self.obj_actor = model.obj_actor

            R, G, B, A = self._get_current_color(self.w_fr_obj_color)
            self.obj_actor.GetProperty().SetColor(R / 255.0, G / 255.0, B / 255.0)
            self.obj_actor.property.opacity = self.w_hs_obj_transparency.value() / 100.0

            self.vtk_renderer.AddActor(self.obj_actor)
            self.vtk_renderer.ResetCamera()

        self.vtk_render_window.Render()

    def _get_current_color(self, frame):
        # print('MainWindow Function: ', inspect.stack()[0][3])
        # print('\tCaller: ', inspect.stack()[1][3])

        palette = frame.palette()
        background_color = palette.color(qtg.QPalette.ColorRole.Window)
        return background_color.getRgb()

    def dcm_color_changed(self):
        # print('MainWindow Function: ', inspect.stack()[0][3])
        # print('\tCaller: ', inspect.stack()[1][3])

        _R, _G, _B, _A = self._get_current_color(self.w_fr_dcm_color)
        color = qtw.QColorDialog.getColor(qtg.QColor(_R, _G, _B) , self, "Select Color")

        if color.isValid():
            R, G, B, A = color.getRgb()
            self.w_fr_dcm_color.setStyleSheet(f"background-color: rgb({R}, {G}, {B});")
            self.w_fr_dcm_color.show()

            if self.dcm_actor is not None:
                self.dcm_actor.GetProperty().SetColor(R / 255.0, G / 255.0, B / 255.0)
                self.vtk_render_window.Render()

    def obj_color_changed(self):
        # print('MainWindow Function: ', inspect.stack()[0][3])
        # print('\tCaller: ', inspect.stack()[1][3])

        _R, _G, _B, _A = self._get_current_color(self.w_fr_obj_color)
        color = qtw.QColorDialog.getColor(qtg.QColor(_R, _G, _B), self, "Select Color")

        if color.isValid():
            R, G, B, A = color.getRgb()
            self.w_fr_obj_color.setStyleSheet(f"background-color: rgb({R}, {G}, {B});")
            self.w_fr_obj_color.show()

            if self.obj_actor is not None:
                self.obj_actor.GetProperty().SetColor(R / 255.0, G / 255.0, B / 255.0)
                self.vtk_render_window.Render()

    def background_color_changed(self):
        # print('MainWindow Function: ', inspect.stack()[0][3])
        # print('\tCaller: ', inspect.stack()[1][3])

        _R, _G, _B, _A = self._get_current_color(self.w_fr_background_color)
        color = qtw.QColorDialog.getColor(qtg.QColor(_R, _G, _B), self, "Select Color")

        if color.isValid():
            R, G, B, A = color.getRgb()
            self.w_fr_background_color.setStyleSheet(f"background-color: rgb({R}, {G}, {B});")
            self.w_fr_background_color.show()

            self.vtk_renderer.SetBackground(R/255.0, G/255.0, B/255.0)
            self.vtk_render_window.Render()

    def dcm_transparency_changed(self):
        # print('MainWindow Function: ', inspect.stack()[0][3])
        # print('\tCaller: ', inspect.stack()[1][3])

        self.w_l_dcm_transparency.setText(str(self.w_hs_dcm_transparency.value()))
        if self.dcm_actor is not None:
            self.dcm_actor.property.opacity = self.w_hs_dcm_transparency.value() / 100.0
            self.vtk_render_window.Render()
        else:
            pass

    def obj_transparency_changed(self):
        # print('MainWindow Function: ', inspect.stack()[0][3])
        # print('\tCaller: ', inspect.stack()[1][3])

        self.w_l_obj_transparency.setText(str(self.w_hs_obj_transparency.value()))
        if self.obj_actor is not None:
            self.obj_actor.property.opacity = self.w_hs_obj_transparency.value() / 100.0
            self.vtk_render_window.Render()
        else:
            pass

    def orientation_changed(self, checked):
        # print('MainWindow Function: ', inspect.stack()[0][3])
        # print('\tCaller: ', inspect.stack()[1][3])

        print(">>orientationChanged")
        print(f"{self.sender()} is checked: {checked}")
        if checked:
            if self.sender().objectName() == 'w_rb_hfs':
                if self.obj_model is not None:
                    self.obj_model.patient_orientation = 'HFS'

            elif self.sender().objectName() == 'w_rb_hfp':
                if self.obj_model is not None:
                    self.obj_model.patient_orientation = 'HFP'

            elif self.sender().objectName() == 'w_rb_ffs':
                if self.obj_model is not None:
                    self.obj_model.patient_orientation = 'FFS'

            elif self.sender().objectName() == 'w_rb_ffp':
                if self.obj_model is not None:
                    self.obj_model.patient_orientation = 'FFP'

    def save_image(self):
        # print('MainWindow Function: ', inspect.stack()[0][3])
        # print('\tCaller: ', inspect.stack()[1][3])

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

    def __get_viewing_bounds(self):
        # print('MainWindow Function: ', inspect.stack()[0][3])
        # print('\tCaller: ', inspect.stack()[1][3])

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

    def set_camera_to_plus_x(self):
        # print('MainWindow Function: ', inspect.stack()[0][3])
        # print('\tCaller: ', inspect.stack()[1][3])

        if self.w_rb_plusX.isChecked():
            camera = self.vtk_renderer.GetActiveCamera()
            x_min, x_max, y_min, y_max, z_min, z_max = self.__get_viewing_bounds()
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

    def set_camera_to_minus_x(self):
        # print('MainWindow Function: ', inspect.stack()[0][3])
        # print('\tCaller: ', inspect.stack()[1][3])

        if self.w_rb_minusX.isChecked():
            camera = self.vtk_renderer.GetActiveCamera()
            x_min, x_max, y_min, y_max, z_min, z_max = self.__get_viewing_bounds()
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

    def sset_camera_to_plus_y(self):
        # print('MainWindow Function: ', inspect.stack()[0][3])
        # print('\tCaller: ', inspect.stack()[1][3])

        if self.w_rb_plusY.isChecked():
            camera = self.vtk_renderer.GetActiveCamera()
            x_min, x_max, y_min, y_max, z_min, z_max = self.__get_viewing_bounds()
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

    def set_camera_to_minus_y(self):
        # print('MainWindow Function: ', inspect.stack()[0][3])
        # print('\tCaller: ', inspect.stack()[1][3])

        if self.w_rb_minusY.isChecked():
            camera = self.vtk_renderer.GetActiveCamera()
            x_min, x_max, y_min, y_max, z_min, z_max = self.__get_viewing_bounds()
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

    def set_camera_to_plus_z(self):
        # print('MainWindow Function: ', inspect.stack()[0][3])
        # print('\tCaller: ', inspect.stack()[1][3])

        if self.w_rb_plusZ.isChecked():
            camera = self.vtk_renderer.GetActiveCamera()
            x_min, x_max, y_min, y_max, z_min, z_max = self.__get_viewing_bounds()
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

    def set_camera_to_minus_z(self):
        # print('MainWindow Function: ', inspect.stack()[0][3])
        # print('\tCaller: ', inspect.stack()[1][3])

        if self.w_rb_minusZ.isChecked():
            camera = self.vtk_renderer.GetActiveCamera()
            x_min, x_max, y_min, y_max, z_min, z_max = self.__get_viewing_bounds()
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


        pass

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())