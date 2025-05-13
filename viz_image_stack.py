import numpy as np
import vtk
from vtkmodules.util.numpy_support import numpy_to_vtk, vtk_to_numpy

# Example: Create a sample 3D array
data_array = np.random.rand(64, 64, 64)

# Convert the NumPy array to a VTK data array
vtk_data_array = numpy_to_vtk(num_array=data_array.ravel(order='F'), deep=True, array_type=vtk.VTK_FLOAT)

# Create a vtkImageData object
image_data = vtk.vtkImageData()
image_data.SetDimensions(data_array.shape)
image_data.SetSpacing([1, 1, 1])  # Adjust spacing as needed
image_data.GetPointData().SetScalars(vtk_data_array)


volume_property = vtk.vtkVolumeProperty()
volume_property.ShadeOn()
volume_property.SetInterpolationTypeToLinear()

# Define color and opacity transfer functions (adjust as needed)
color_transfer_function = vtk.vtkColorTransferFunction()
color_transfer_function.AddRGBPoint(0, 0.0, 0.0, 0.0)
color_transfer_function.AddRGBPoint(1, 1.0, 1.0, 1.0)

opacity_transfer_function = vtk.vtkPiecewiseFunction()
opacity_transfer_function.AddPoint(0, 0.0)
opacity_transfer_function.AddPoint(1, 1.0)

volume_property.SetColor(color_transfer_function)
volume_property.SetScalarOpacity(opacity_transfer_function)



# Create a volume mapper
volume_mapper = vtk.vtkGPUVolumeRayCastMapper()
volume_mapper.SetInputData(image_data)

# Create a volume actor
volume_actor = vtk.vtkVolume()
volume_actor.SetMapper(volume_mapper)
volume_actor.SetProperty(volume_property)


# Create a renderer and add the actor to it
renderer = vtk.vtkRenderer()
renderer.AddActor(volume_actor)
renderer.SetBackground(0.0, 0.0, 0.0)  # Set background color

# Create a render window and add the renderer to it
render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(600, 600)

# Create an interactor and start the rendering loop
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

render_window.Render()
interactor.Start()
