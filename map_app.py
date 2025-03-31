import sys
import vtk
import PySide6.QtWidgets as qtw

from ui.test_window import Ui_MainWindow
from model.dicom import DicomFileSyncModel
from model.obj import ObjFileModel

DFS = DicomFileSyncModel()
OFM = ObjFileModel()

class MainWindow(qtw.QMainWindow, Ui_MainWindow):
    def __init__(self):
        print(">>Application __init__")
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("VTK Test Window")

        # VTK rendering setup
        self.dcm_actor = None
        self.obj_actor = None

        self.vtk_renderer = vtk.vtkRenderer()
        self.vtk_render_window = self.vtk_widget.GetRenderWindow()
        self.vtk_render_window.AddRenderer(self.vtk_renderer)
        self.vtk_interactor = self.vtk_widget.GetRenderWindow().GetInteractor()

        self.named_colors = vtk.vtkNamedColors()
        color_names_string = self.named_colors.GetColorNames()
        color_names_list = color_names_string.split('\n')

        self.w_pb_dcm_plan_file.clicked.connect(self.openDcmPlanFile)
        self.w_pb_dcm_struct_file.clicked.connect(self.openDcmStructFile)
        self.w_cb_dcm_color.addItems(color_names_list)
        self.w_cb_dcm_color.currentTextChanged.connect(self.dcmColorNameChanged)
        self.w_cb_dcm_color.setCurrentText('green')
        self.w_hs_dcm_transparency.valueChanged.connect(self.dcmTransparencyChanged)

        self.w_le_dcm_plan_file.textChanged.connect(DFS.update_plan_file)
        self.w_le_dcm_struct_file.textChanged.connect(DFS.update_structure_file)

        DFS.vtk_actor_updated.connect(self.updateDcmVisualization)

        self.patient_orientation = None

        self.w_pb_obj_file.clicked.connect(self.openObjFile)
        self.w_cb_obj_color.addItems(color_names_list)
        self.w_cb_obj_color.currentTextChanged.connect(self.objColorNameChanged)
        self.w_cb_obj_color.setCurrentText('light_grey')
        self.w_hs_obj_transparency.valueChanged.connect(self.objTransparencyChanged)

        self.w_le_obj_file.textChanged.connect(OFM.update_obj_file)

        OFM.vtk_actor_updated.connect(self.updateObjVisualization)

        self.w_rb_hfs.toggled.connect(self.orientationChanged)
        self.w_rb_hfp.toggled.connect(self.orientationChanged)
        self.w_rb_ffs.toggled.connect(self.orientationChanged)
        self.w_rb_ffp.toggled.connect(self.orientationChanged)

        self.w_cb_background_color.addItems(color_names_list)
        self.w_cb_background_color.currentTextChanged.connect(self.backgroundColorNameChanged)
        self.w_cb_background_color.setCurrentText('black')

        self.w_pb_save_image.clicked.connect(self.saveImage)

        self.w_rb_plusX.toggled.connect(self.setCameraToPlusX)
        self.w_rb_minusX.toggled.connect(self.setCameraToMinusX)
        self.w_rb_plusY.toggled.connect(self.setCameraToPlusY)
        self.w_rb_minusY.toggled.connect(self.setCameraToMinusY)
        self.w_rb_plusZ.toggled.connect(self.setCameraToPlusZ)
        self.w_rb_minusZ.toggled.connect(self.setCameraToMinusZ)

        self.vtk_interactor.Initialize()
        self.vtk_widget.show()

    def openDcmPlanFile(self):
        print(">>openDcmPlanFile")
        filename, _ = qtw.QFileDialog.getOpenFileName(self,
                                                      "Select DICOM Structureset File",
                                                      ".",
                                                      "DICOM Files (*.dcm)"
                                                      )
        if filename:
            # This will trigger model update through connection to the DicomFileSyncModel.update_plan_file
            # Slot made in the __init__ method.
            self.w_le_dcm_plan_file.setText(filename)

            # ds = pydicom.dcmread(filename)
            #
            # current_orientation = None
            # bypass = False
            #
            # for setup in ds.PatientSetupSequence:
            #     if current_orientation is None:
            #         current_orientation = setup.PatientPosition
            #     elif current_orientation != setup.PatientPosition:
            #         print("There are multiple patient orientations reported in the DICOM Plan")
            #     else:
            #         pass
            #
            #     if (self.patient_orientation is None) or \
            #             (self.patient_orientation != setup.PatientPosition and not bypass):
            #         print("In Bypass loop")
            #         if setup.PatientPosition == 'HFS':
            #             self.w_rb_hfs.setChecked(True)
            #         elif setup.PatientPosition == 'HFP':
            #             self.w_rb_hfp.setChecked(True)
            #         elif setup.PatientPosition == 'FFS':
            #             self.w_rb_ffs.setChecked(True)
            #         elif setup.PatientPosition == 'FFP':
            #             self.w_rb_ffp.setChecked(True)
            #         else:
            #             pass
            #         bypass = True
            #     else:
            #         pass

    def openDcmStructFile(self):
        print(">>openDcmStructFile")
        filename, _ = qtw.QFileDialog.getOpenFileName(self,
                                                      "Select DICOM Structureset File",
                                                      ".",
                                                      "DICOM Files (*.dcm)"
                                                      )
        if filename:
            # This will trigger model update through connection to the DicomFileSyncModel.update_structure_file
            # Slot made in the __init__ method.
            self.w_le_dcm_struct_file.setText(filename)

    def updateDcmVisualization(self):
        if self.dcm_actor is None:
            self.dcm_actor = DFS.dcm_body_actor

            R, G, B = self.named_colors.GetColor3ub(self.w_cb_dcm_color.currentText())
            self.dcm_actor.GetProperty().SetColor(R / 255.0, G / 255.0, B / 255.0)
            self.dcm_actor.property.opacity = self.w_hs_dcm_transparency.value() / 100.0

            self.vtk_renderer.AddActor(self.dcm_actor)
            self.vtk_renderer.ResetCamera()
        else:
            self.vtk_renderer.RemoveActor(self.dcm_actor)
            self.dcm_actor = DFS.dcm_body_actor

            R, G, B = self.named_colors.GetColor3ub(self.w_cb_dcm_color.currentText())
            self.dcm_actor.GetProperty().SetColor(R / 255.0, G / 255.0, B / 255.0)
            self.dcm_actor.property.opacity = self.w_hs_dcm_transparency.value() / 100.0

            self.vtk_renderer.AddActor(self.dcm_actor)
            self.vtk_renderer.ResetCamera()

        self.vtk_render_window.Render()

    def openObjFile(self):
        print(">>openObjFile")
        filename, _ = qtw.QFileDialog.getOpenFileName(self,
                                                      "Select DICOM Structureset File",
                                                      ".",
                                                      "OBJ Files (*.obj)"
                                                      )
        if filename:
            self.w_le_obj_file.setText(filename)

    def updateObjVisualization(self):
        if self.obj_actor is None:
            self.obj_actor = OFM.obj_actor

            R, G, B = self.named_colors.GetColor3ub(self.w_cb_obj_color.currentText())
            self.obj_actor.GetProperty().SetColor(R / 255.0, G / 255.0, B / 255.0)
            self.obj_actor.property.opacity = self.w_hs_obj_transparency.value() / 100.0

            self.vtk_renderer.AddActor(self.obj_actor)
            self.vtk_renderer.ResetCamera()
        else:
            self.vtk_renderer.RemoveActor(self.obj_actor)
            self.obj_actor = OFM.obj_actor

            R, G, B = self.named_colors.GetColor3ub(self.w_cb_obj_color.currentText())
            self.obj_actor.GetProperty().SetColor(R / 255.0, G / 255.0, B / 255.0)
            self.obj_actor.property.opacity = self.w_hs_obj_transparency.value() / 100.0

            self.vtk_renderer.AddActor(self.obj_actor)
            self.vtk_renderer.ResetCamera()

        self.vtk_render_window.Render()

    def dcmColorNameChanged(self):
        print(">>dcmColorNameChanged")
        R, G, B = self.named_colors.GetColor3ub(self.w_cb_dcm_color.currentText())
        self.w_dcm_color_frame.setStyleSheet(f"background-color: rgb({R}, {G}, {B});")
        self.w_dcm_color_frame.show()

        if self.dcm_actor is not None:
            self.dcm_actor.GetProperty().SetColor(R / 255.0, G / 255.0, B / 255.0)
            self.vtk_render_window.Render()

    def dcmTransparencyChanged(self):
        print(">>dcmTransparencyChanged")
        self.w_l_dcm_transparency.setText(str(self.w_hs_dcm_transparency.value()))
        if self.dcm_actor.property is not None:
            self.dcm_actor.property.opacity = self.w_hs_dcm_transparency.value() / 100.0
            self.vtk_render_window.Render()
        else:
            pass

    def objColorNameChanged(self):
        print(">>objColorNameChanged")
        R, G, B = self.named_colors.GetColor3ub(self.w_cb_obj_color.currentText())
        self.w_obj_color_frame.setStyleSheet(f"background-color: rgb({R}, {G}, {B});")
        self.w_obj_color_frame.show()

        if self.obj_actor is not None:
            self.obj_actor.GetProperty().SetColor(R / 255.0, G / 255.0, B / 255.0)
            self.vtk_render_window.Render()

    def objTransparencyChanged(self):
        print(">>objTransparencyChanged")
        self.w_l_obj_transparency.setText(str(self.w_hs_obj_transparency.value()))
        if self.obj_actor.property is not None:
            self.obj_actor.property.opacity = self.w_hs_obj_transparency.value() / 100.0
            self.vtk_render_window.Render()
        else:
            pass

    def backgroundColorNameChanged(self):
        print(">>backgroundColorNameChanged")
        R, G, B = self.named_colors.GetColor3ub(self.w_cb_background_color.currentText())
        self.w_background_color_frame.setStyleSheet(f"background-color: rgb({R}, {G}, {B});")
        self.w_background_color_frame.show()

        self.vtk_renderer.SetBackground(R/255.0, G/255.0, B/255.0)
        self.vtk_render_window.Render()

    def orientationChanged(self, checked):
        print(">>orientationChanged")
        print(f"{self.sender()} is checked: {checked}")
        if checked:
            if self.sender().objectName() == 'w_rb_hfs':
                self.patient_orientation = 'HFS'
                OFM.patient_orientation = 'HFS'

                # if self.obj_actor is not None:
                #     self._loadOBJMesh(self.w_le_obj_file.text())


            elif self.sender().objectName() == 'w_rb_hfp':
                self.patient_orientation = 'HFP'
                OFM.patient_orientation = 'HFP'

                # if self.obj_actor is not None:
                #     self._loadOBJMesh(self.w_le_obj_file.text())

            elif self.sender().objectName() == 'w_rb_ffs':
                self.patient_orientation = 'FFS'
                OFM.patient_orientation = 'FFS'
                #
                # if self.obj_actor is not None:
                #     self._loadOBJMesh(self.w_le_obj_file.text())

            elif self.sender().objectName() == 'w_rb_ffp':
                self.patient_orientation = 'FFP'
                OFM.patient_orientation = 'FFP'

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


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())