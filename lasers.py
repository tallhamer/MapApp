import trimesh
import open3d as o3d
import vtk
from vtkmodules.util import numpy_support

_mesh = trimesh.load(r"C:\tmp\map app data\matched_mergedSurface.obj")

points = _mesh.vertices

pcloud = o3d.geometry.PointCloud()
pcloud.points = o3d.utility.Vector3dVector(points)

mesh = o3d.geometry.TriangleMesh()
mesh.vertices = o3d.utility.Vector3dVector(points)
mesh.triangles = o3d.utility.Vector3iVector(_mesh.faces)

mesh.compute_vertex_normals()
mesh.compute_triangle_normals()

polydata = vtk.vtkPolyData()
polydata.points = numpy_support.numpy_to_vtk(points)

cells = vtk.vtkCellArray()

for i in range(len(mesh.triangles)):
    cells.InsertNextCell(3, mesh.triangles[i])
polydata.polys = cells

# Create a planes
xy_plane = vtk.vtkPlane()
xy_plane.SetOrigin(0, 0, 0)
xy_plane.SetNormal(0, 0, 1)

# Create a planes
yz_plane = vtk.vtkPlane()
yz_plane.SetOrigin(0, 0, 0)
yz_plane.SetNormal(1, 0, 0)

# Create a planes
zx_plane = vtk.vtkPlane()
zx_plane.SetOrigin(0, 0, 0)
zx_plane.SetNormal(0, 1, 0)

# # Create a vtkSphereSource
# sphere_source = vtk.vtkSphereSource()
#
# # Set the radius of the sphere
# sphere_source.SetRadius(5.0)
#
# # Set the center of the sphere
# sphere_source.SetCenter(0.0, 0.0, 0.0)
#
# # Set the number of subdivisions along the latitude and longitude directions
# sphere_source.SetThetaResolution(24)
# sphere_source.SetPhiResolution(24)
#
# # Update the sphere source to apply the changes
# sphere_source.Update()
#
# # Get the output polydata
# polydata = sphere_source.GetOutput()

# Create sphere geometry
sphereSource = vtk.vtkSphereSource()
sphereSource.radius = 3
sphereSource.phi_resolution = 5
sphereSource.theta_resolution = 5

# Create a cutters
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

# Mapp the Sphere Glyph to the points
xy_glyphFilter = vtk.vtkGlyph3D()
xy_glyphFilter.SetInputData(xy_cutter.GetOutput())
xy_glyphFilter.SetSourceConnection(sphereSource.GetOutputPort())
xy_glyphFilter.SetScaling(False) # Disable scaling of glyphs
xy_glyphFilter.Update()

# Create a mapper and actor for the cut surface
xy_cut_mapper = vtk.vtkPolyDataMapper()
xy_cut_mapper.SetInputData(xy_glyphFilter.GetOutput())
xy_cut_actor = vtk.vtkActor()
xy_cut_actor.SetMapper(xy_cut_mapper)
xy_cut_actor.GetProperty().SetColor(1, 0, 0) # Red color for the cut surface

# # Create a mapper and actor for the cut surface
# xy_cut_mapper = vtk.vtkPolyDataMapper()
# xy_cut_mapper.SetInputData(xy_cutter.GetOutput())
# xy_cut_actor = vtk.vtkActor()
# xy_cut_actor.SetMapper(xy_cut_mapper)
# xy_cut_actor.GetProperty().SetColor(1, 0, 0) # Red color for the cut surface

yz_cut_mapper = vtk.vtkPolyDataMapper()
yz_cut_mapper.SetInputData(yz_cutter.GetOutput())
yz_cut_actor = vtk.vtkActor()
yz_cut_actor.SetMapper(yz_cut_mapper)
yz_cut_actor.GetProperty().SetColor(0, 1, 0) # Green color for the cut surface

zx_cut_mapper = vtk.vtkPolyDataMapper()
zx_cut_mapper.SetInputData(zx_cutter.GetOutput())
zx_cut_actor = vtk.vtkActor()
zx_cut_actor.SetMapper(zx_cut_mapper)
zx_cut_actor.GetProperty().SetColor(0, 0, 1) # Blue color for the cut surface

# Create a mapper and actor for the original surface
original_mapper = vtk.vtkPolyDataMapper()
original_mapper.SetInputData(polydata)
original_actor = vtk.vtkActor()
original_actor.SetMapper(original_mapper)
original_actor.GetProperty().SetColor(.9, .9, .9) # Blue color for the original surface

# Create a renderer and render window
renderer = vtk.vtkRenderer()
render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)

# Create an interactor
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Add actors to the renderer
renderer.AddActor(xy_cut_actor)
renderer.AddActor(yz_cut_actor)
renderer.AddActor(zx_cut_actor)
renderer.AddActor(original_actor)

# Set background color and render
renderer.SetBackground(1, 1, 1)
render_window.Render()

# Start interaction
interactor.Start()