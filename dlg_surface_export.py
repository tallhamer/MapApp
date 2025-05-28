import numpy as np
import open3d as o3d
from scipy.ndimage import gaussian_filter

import PySide6.QtWidgets as qtw

import vtk
from vtkmodules.util.numpy_support import numpy_to_vtk, vtk_to_numpy

from ui.surface_export_dialog import Ui_SurfaceExportDialog

import logging
logger = logging.getLogger('MapApp')

class SurfaceExportDialog(qtw.QDialog, Ui_SurfaceExportDialog):
    def __init__(self, mainwindow):
        self.logger = logging.getLogger('MapApp.dlg_surface_export.SurfaceExportDialog')
        logger.debug("Setting up the SurfaceExportDialog UI")
        super().__init__()
        self.setupUi(self)

        self.mainwindow = mainwindow

        self.w_tw_visualizations.setCurrentIndex(0)
        self.w_tw_visualizations.setTabEnabled(1, False)
        self.w_dsb_voxel_size.setValue(1.0)
        self.w_ch_smooth.checkStateChanged.connect(self.enable_smooth_sigma)

        self._construct_3D_surface_view()
        # self._construct_3D_volume_view()

        self.w_dsb_x_bounds_min.valueChanged.connect(self.update_clipping_box)
        self.w_dsb_x_bounds_max.valueChanged.connect(self.update_clipping_box)
        self.w_dsb_y_bounds_min.valueChanged.connect(self.update_clipping_box)
        self.w_dsb_y_bounds_max.valueChanged.connect(self.update_clipping_box)
        self.w_dsb_z_bounds_min.valueChanged.connect(self.update_clipping_box)
        self.w_dsb_z_bounds_max.valueChanged.connect(self.update_clipping_box)

    def _construct_3D_surface_view(self):
        self.logger.debug("Setup VTK 3D visualization windows")

        # 3D Scene Widget Setup
        self.vtk_surface_renderer = vtk.vtkRenderer()
        self.vtk_surface_render_window = self.vtk_polydata_render_widget.GetRenderWindow()
        self.vtk_surface_render_window.AddRenderer(self.vtk_surface_renderer)
        self.vtk_surface_interactor = self.vtk_polydata_render_widget.GetRenderWindow().GetInteractor()
        self.vtk_surface_interactor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())

        # Create axes actor
        axes_actor = vtk.vtkAxesActor()

        # Create axis orientation marker widget
        self.axis_widget = vtk.vtkOrientationMarkerWidget()
        self.axis_widget.SetOutlineColor(0.9300, 0.5700, 0.1300)
        self.axis_widget.SetOrientationMarker(axes_actor)
        self.axis_widget.SetInteractor(self.vtk_surface_interactor)
        self.axis_widget.SetViewport(0.0, 0.0, 0.2, 0.2)  # Set size and position
        self.axis_widget.EnabledOn()
        self.axis_widget.InteractiveOff()

        # Create orientation manipulation widget
        self.cam_orient_widget = vtk.vtkCameraOrientationWidget(parent_renderer=self.vtk_surface_renderer,
                                                                     interactor=self.vtk_surface_interactor
                                                                     )
        # Enable the widget.
        self.cam_orient_widget.EnabledOn()

        self.polydata = self.mainwindow.maprt_transform_filter.GetOutput()
        x_min, x_max, y_min, y_max, z_min, z_max = self.polydata.GetBounds()
        self.w_dsb_x_bounds_min.setValue(x_min)
        self.w_dsb_x_bounds_max.setValue(x_max)
        self.w_dsb_y_bounds_min.setValue(y_min)
        self.w_dsb_y_bounds_max.setValue(y_max)
        self.w_dsb_z_bounds_min.setValue(z_min)
        self.w_dsb_z_bounds_max.setValue(z_max)

        self.export_box = vtk.vtkBox()
        self.export_box.SetBounds(x_min, x_max, y_min, y_max, z_min, z_max)

        self.clipper = vtk.vtkClipPolyData()
        self.clipper.SetInputData(self.polydata)
        self.clipper.SetClipFunction(self.export_box)
        self.clipper.SetInsideOut(1)  # Extract the portion inside the box

        self.clipper.Update()
        self.exportable_polydata = self.clipper.GetOutput()

        self.export_mapper = vtk.vtkPolyDataMapper()
        self.exportable_polydata >> self.export_mapper

        self.export_actor = vtk.vtkActor(mapper=self.export_mapper)

        self.vtk_surface_renderer.AddActor(self.export_actor)
        self.vtk_surface_renderer.ResetCamera()
        self.vtk_surface_render_window.Render()

        self.vtk_surface_interactor.Initialize()
        self.vtk_polydata_render_widget.show()

    def enable_smooth_sigma(self):
        self.w_dsb_sigma.setEnabled(self.w_ch_smooth.isChecked())

    def update_clipping_box(self):
        x_min = self.w_dsb_x_bounds_min.value()
        x_max = self.w_dsb_x_bounds_max.value()
        y_min = self.w_dsb_y_bounds_min.value()
        y_max = self.w_dsb_y_bounds_max.value()
        z_min = self.w_dsb_z_bounds_min.value()
        z_max = self.w_dsb_z_bounds_max.value()

        self.export_box.SetBounds(x_min, x_max, y_min, y_max, z_min, z_max)
        self.clipper.Update()
        self.vtk_surface_render_window.Render()