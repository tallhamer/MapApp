import sys
import vtk

import PySide6.QtCore as qtc
import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg


# from ui.test_window import Ui_MainWindow
from ui.main_window import Ui_MainWindow
from model.dicom import DicomRTPlan, DicomRTStructureSet, DicomFileValidationError
from model.obj import ObjFile

OBJ = ObjFile()

class MainWindow(qtw.QMainWindow, Ui_MainWindow):
    def __init__(self):
        print(">>Application __init__")
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Map App")

        # VTK rendering setup
        self.dcm_actor = None
        self.obj_actor = None

        # 3D Scene Widget Setup
        self.vtk_renderer = vtk.vtkRenderer()
        self.vtk_render_window = self.vtk_widget.GetRenderWindow()
        self.vtk_render_window.AddRenderer(self.vtk_renderer)
        self.vtk_interactor = self.vtk_widget.GetRenderWindow().GetInteractor()
        self.vtk_interactor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())

        self.named_colors = vtk.vtkNamedColors()
        color_names_string = self.named_colors.GetColorNames()
        color_names_list = color_names_string.split('\n')

        # Patient Context Widget Setup


        ## DICOM RT File Widget Setup
        self.dicomrt_plan_model = None

        self.w_gb_dicomrt_files.setVisible(False)
        self.w_ch_use_dicomrt.checkStateChanged.connect(self.show_dicomrt_file_input_widgets)
        self.w_ch_use_dicomrt.checkStateChanged.connect(self._clear_patient_context)

        self.w_pb_dcm_plan_file.clicked.connect(self.open_dcm_plan_file)
        self.w_pb_dcm_struct_file.clicked.connect(self.open_dcm_struct_file)

        self.w_pb_dcm_color.clicked.connect(self.dcm_color_changed)
        self.w_fr_dcm_color.setStyleSheet(f"background-color: rgb({0}, {127}, {0});")
        self.w_fr_dcm_color.show()
        self.w_hs_dcm_transparency.valueChanged.connect(self.dcm_transparency_changed)

        self.w_pb_obj_file.clicked.connect(self.open_obj_file)

        self.w_pb_obj_color.clicked.connect(self.obj_color_changed)
        self.w_fr_obj_color.setStyleSheet(f"background-color: rgb({127}, {127}, {127});")
        self.w_fr_obj_color.show()
        self.w_hs_obj_transparency.valueChanged.connect(self.obj_transparency_changed)

        self.w_le_obj_file.textChanged.connect(OBJ.update_obj_file)
        OBJ.vtk_actor_updated.connect(self.update_obj_visualization)

        self.w_rb_hfs.toggled.connect(self.orientationChanged)
        self.w_rb_hfp.toggled.connect(self.orientationChanged)
        self.w_rb_ffs.toggled.connect(self.orientationChanged)
        self.w_rb_ffp.toggled.connect(self.orientationChanged)

        self.w_pb_background_color.clicked.connect(self.background_color_changed)
        self.w_fr_background_color.setStyleSheet(f"background-color: rgb({0}, {0}, {0});")
        self.w_fr_background_color.show()

        self.w_pb_save_image.clicked.connect(self.saveImage)

        self.w_rb_plusX.toggled.connect(self.setCameraToPlusX)
        self.w_rb_minusX.toggled.connect(self.setCameraToMinusX)
        self.w_rb_plusY.toggled.connect(self.setCameraToPlusY)
        self.w_rb_minusY.toggled.connect(self.setCameraToMinusY)
        self.w_rb_plusZ.toggled.connect(self.setCameraToPlusZ)
        self.w_rb_minusZ.toggled.connect(self.setCameraToMinusZ)

        self.vtk_interactor.Initialize()
        self.vtk_widget.show()

    def show_info_message(self, message):
        res = qtw.QMessageBox.information(self, "Information", message, qtw.QMessageBox.Ok)

    def show_dicomrt_file_input_widgets(self):
        self.w_le_dcm_plan_file.clear()
        self.w_le_patinet_id.setEnabled(not self.w_ch_use_dicomrt.isChecked())
        self.w_cb_plan_id.setEnabled(not self.w_ch_use_dicomrt.isChecked())
        self.w_gb_dicomrt_files.setVisible(self.w_ch_use_dicomrt.isChecked())

        if self.dcm_actor is not None:
            self.vtk_renderer.RemoveActor(self.dcm_actor)
            self.vtk_render_window.Render()
            self.dcm_actor = None

    def open_dcm_plan_file(self):
        filename, _ = qtw.QFileDialog.getOpenFileName(self,
                                                      "Select DICOM Structureset File",
                                                      ".",
                                                      "DICOM Files (*.dcm)"
                                                      )
        if filename:
            try:
                self.dicomrt_plan_model = DicomRTPlan()
                self.dicomrt_plan_model.invalid_file_loaded.connect(self.show_info_message)
                self.dicomrt_plan_model.file_path_changed.connect(self.w_le_dcm_plan_file.setText)
                self.dicomrt_plan_model.plan_model_updated.connect(self.update_patient_context)

                self.dicomrt_plan_model.structure_set.invalid_file_loaded.connect(self.show_info_message)
                self.dicomrt_plan_model.structure_set.file_path_changed.connect(self.w_le_dcm_struct_file.setText)
                self.dicomrt_plan_model.structure_set.vtkActorUpdated.connect(self.update_dcm_visualization)

                self.dicomrt_plan_model.filepath = filename
            except DicomFileValidationError as e:
                self.dicomrt_plan_model = None
                print(e)

    def _clear_patient_context(self):
        self.w_le_patinet_id.clear()
        self.w_l_patient_first_name.setText('')
        self.w_l_patient_last_name.setText('')
        self.w_cb_plan_id.clear()
        self.w_cb_plan_id.setEnabled(False)
        self.w_l_plan_isocenter.setText('')
        self.w_cb_body_structure.clear()
        self.w_cb_body_structure.setEnabled(False)
        self.w_tw_beams.clear()

    def update_patient_context(self):
        self.w_le_patinet_id.setText(self.dicomrt_plan_model.patient_id)

        self.w_l_patient_first_name.setText(self.dicomrt_plan_model.patient_first_name)
        self.w_l_patient_last_name.setText(self.dicomrt_plan_model.patient_last_name)
        self.w_cb_plan_id.setEnabled(False)
        self.w_cb_plan_id.addItem(self.dicomrt_plan_model.plan_id)
        self.w_cb_plan_id.setCurrentIndex(0)
        X, Y, Z = self.dicomrt_plan_model.isocenter
        self.w_l_plan_isocenter.setText(f'< {X}, {Y}, {Z} >')

        self.w_tw_beams.setRowCount(len(self.dicomrt_plan_model.beams))
        self.w_tw_beams.setColumnCount(len(self.dicomrt_plan_model.beams[0]))
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

        for row_index, row_data in enumerate(self.dicomrt_plan_model.beams):
            for col_index, cell_data in enumerate(row_data):
                item = qtw.QTableWidgetItem(cell_data)
                item.setTextAlignment(qtc.Qt.AlignmentFlag.AlignCenter)
                self.w_tw_beams.setItem(row_index, col_index, item)

        self.w_tw_beams.resizeColumnsToContents()
        self.w_tw_beams.setSortingEnabled(True)

    def open_dcm_struct_file(self):
        filename, _ = qtw.QFileDialog.getOpenFileName(self,
                                                      "Select DICOM Structureset File",
                                                      ".",
                                                      "DICOM Files (*.dcm)"
                                                      )
        if filename:
            self.dicomrt_plan_model.structure_set.update_filepath(filename)

    def update_dcm_visualization(self):
        if self.dcm_actor is None:
            self.dcm_actor = self.dicomrt_plan_model.structure_set.dcm_body_actor

            # R, G, B = self.named_colors.GetColor3ub(self.w_cb_dcm_color.currentText())
            R, G, B, A = self._get_current_dcm_color(self.w_fr_dcm_color)
            self.dcm_actor.GetProperty().SetColor(R / 255.0, G / 255.0, B / 255.0)
            self.dcm_actor.property.opacity = self.w_hs_dcm_transparency.value() / 100.0

            self.vtk_renderer.AddActor(self.dcm_actor)
            self.vtk_renderer.ResetCamera()
        else:
            self.vtk_renderer.RemoveActor(self.dcm_actor)
            # self.dcm_actor = RS.dcm_body_actor
            self.dcm_actor = self.dicomrt_plan_model.structure_set.dcm_body_actor

            # R, G, B = self.named_colors.GetColor3ub(self.w_cb_dcm_color.currentText())
            R, G, B, A = self._get_current_dcm_color(self.w_fr_dcm_color)
            self.dcm_actor.GetProperty().SetColor(R / 255.0, G / 255.0, B / 255.0)
            self.dcm_actor.property.opacity = self.w_hs_dcm_transparency.value() / 100.0

            self.vtk_renderer.AddActor(self.dcm_actor)
            self.vtk_renderer.ResetCamera()

        self.vtk_render_window.Render()

    def open_obj_file(self):
        filename, _ = qtw.QFileDialog.getOpenFileName(self,
                                                      "Select DICOM Structureset File",
                                                      ".",
                                                      "OBJ Files (*.obj)"
                                                      )
        if filename:
            self.w_le_obj_file.setText(filename)

    def update_obj_visualization(self):
        if self.obj_actor is None:
            self.obj_actor = OBJ.obj_actor

            R, G, B = self.named_colors.GetColor3ub(self.w_fr_obj_color.currentText())
            self.obj_actor.GetProperty().SetColor(R / 255.0, G / 255.0, B / 255.0)
            self.obj_actor.property.opacity = self.w_hs_obj_transparency.value() / 100.0

            self.vtk_renderer.AddActor(self.obj_actor)
            self.vtk_renderer.ResetCamera()
        else:
            self.vtk_renderer.RemoveActor(self.obj_actor)
            self.obj_actor = OBJ.obj_actor

            R, G, B = self.named_colors.GetColor3ub(self.w_fr_obj_color.currentText())
            self.obj_actor.GetProperty().SetColor(R / 255.0, G / 255.0, B / 255.0)
            self.obj_actor.property.opacity = self.w_hs_obj_transparency.value() / 100.0

            self.vtk_renderer.AddActor(self.obj_actor)
            self.vtk_renderer.ResetCamera()

        self.vtk_render_window.Render()

    def _get_current_dcm_color(self, frame):
        palette = frame.palette()
        background_color = palette.color(qtg.QPalette.ColorRole.Window)
        return background_color.getRgb()

    def dcm_color_changed(self):
        _R, _G, _B, _A = self._get_current_dcm_color(self.w_fr_dcm_color)
        color = qtw.QColorDialog.getColor(qtg.QColor(_R, _G, _B) , self, "Select Color")

        if color is not None:
            R, G, B, A = color.getRgb()
            self.w_fr_dcm_color.setStyleSheet(f"background-color: rgb({R}, {G}, {B});")
            self.w_fr_dcm_color.show()

            if self.dcm_actor is not None:
                self.dcm_actor.GetProperty().SetColor(R / 255.0, G / 255.0, B / 255.0)
                self.vtk_render_window.Render()

    def obj_color_changed(self):
        _R, _G, _B, _A = self._get_current_dcm_color(self.w_fr_obj_color)
        color = qtw.QColorDialog.getColor(qtg.QColor(_R, _G, _B), self, "Select Color")

        if color is not None:
            R, G, B, A = color.getRgb()
            self.w_fr_obj_color.setStyleSheet(f"background-color: rgb({R}, {G}, {B});")
            self.w_fr_obj_color.show()

            if self.obj_actor is not None:
                self.obj_actor.GetProperty().SetColor(R / 255.0, G / 255.0, B / 255.0)
                self.vtk_render_window.Render()

    def background_color_changed(self):
        _R, _G, _B, _A = self._get_current_dcm_color(self.w_fr_background_color)
        color = qtw.QColorDialog.getColor(qtg.QColor(_R, _G, _B), self, "Select Color")

        if color is not None:
            R, G, B, A = color.getRgb()
            self.w_fr_background_color.setStyleSheet(f"background-color: rgb({R}, {G}, {B});")
            self.w_fr_background_color.show()

            self.vtk_renderer.SetBackground(R/255.0, G/255.0, B/255.0)
            self.vtk_render_window.Render()

    def dcm_transparency_changed(self):
        self.w_l_dcm_transparency.setText(str(self.w_hs_dcm_transparency.value()))
        if self.dcm_actor.property is not None:
            self.dcm_actor.property.opacity = self.w_hs_dcm_transparency.value() / 100.0
            self.vtk_render_window.Render()
        else:
            pass

    def obj_transparency_changed(self):
        self.w_l_obj_transparency.setText(str(self.w_hs_obj_transparency.value()))
        if self.obj_actor.property is not None:
            self.obj_actor.property.opacity = self.w_hs_obj_transparency.value() / 100.0
            self.vtk_render_window.Render()
        else:
            pass



    def orientationChanged(self, checked):
        print(">>orientationChanged")
        print(f"{self.sender()} is checked: {checked}")
        if checked:
            if self.sender().objectName() == 'w_rb_hfs':
                # self.patient_orientation = 'HFS'
                OBJ.patient_orientation = 'HFS'

                # if self.obj_actor is not None:
                #     self._loadOBJMesh(self.w_le_obj_file.text())


            elif self.sender().objectName() == 'w_rb_hfp':
                # self.patient_orientation = 'HFP'
                OBJ.patient_orientation = 'HFP'

                # if self.obj_actor is not None:
                #     self._loadOBJMesh(self.w_le_obj_file.text())

            elif self.sender().objectName() == 'w_rb_ffs':
                # self.patient_orientation = 'FFS'
                OBJ.patient_orientation = 'FFS'
                #
                # if self.obj_actor is not None:
                #     self._loadOBJMesh(self.w_le_obj_file.text())

            elif self.sender().objectName() == 'w_rb_ffp':
                # self.patient_orientation = 'FFP'
                OBJ.patient_orientation = 'FFP'

                # if self.obj_actor is not None:
                #     self._loadOBJMesh(self.w_le_obj_file.text())

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

    def _getViewingBounds(self):
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


        pass


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())