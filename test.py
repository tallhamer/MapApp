import vtk
import trimesh
import open3d as o3d
import numpy as np


renderer = vtk.vtkRenderer()
render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window_interactor = vtk.vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)


# OBJ  File Processing
original_mesh = trimesh.load(r"C:\__python__\Projects\MapApp\data\matched_mergedSurface.obj")

points = np.asarray(original_mesh.vertices)

obj_mesh = o3d.geometry.TriangleMesh()
obj_mesh.vertices = o3d.utility.Vector3dVector(original_mesh.vertices)
obj_mesh.triangles = o3d.utility.Vector3iVector(np.array(original_mesh.faces))

obj_mesh.compute_vertex_normals()
obj_mesh.compute_triangle_normals()

obj_points = vtk.vtkPoints()
point_polydata = vtk.vtkPolyData()

for point in obj_mesh.vertices:
    obj_points.InsertNextPoint(*point)

point_polydata.points = obj_points

for i in range(10):
    p = point_polydata.GetPoint(i)
    print(f"Point {i}: {p}")

transform = vtk.vtkTransform()
matrix = transform.GetMatrix()
matrix.Identity()
matrix.SetElement(0, 0, 0)
matrix.SetElement(0, 1, 1)
matrix.SetElement(1, 1, 0)
matrix.SetElement(1, 2, 1)
matrix.SetElement(2, 1, 1)
matrix.SetElement(2, 2, 0)
print(matrix)

# Create a transform filter
transform_filter = vtk.vtkTransformFilter()
transform_filter.SetInputData(point_polydata)
transform_filter.SetTransform(transform)
transform_filter.Update()

obj_polydata = transform_filter.GetPolyDataOutput()
# obj_polydata.points = obj_points
obj_cells = vtk.vtkCellArray()

for i in range(len(obj_mesh.triangles)):
    obj_cells.InsertNextCell(3, obj_mesh.triangles[i])
obj_polydata.polys = obj_cells

for i in range(10):
    p = obj_polydata.GetPoint(i)
    print(f"Point {i}: {p}")

# self.obj_mapper = vtk.vtkOpenGLPolyDataMapper()
obj_mapper = vtk.vtkPolyDataMapper()
obj_polydata >> obj_mapper

obj_actor = vtk.vtkActor(mapper=obj_mapper)
obj_actor.GetProperty().SetColor(127 / 255.0, 127 / 255.0, 127 / 255.0)

renderer.AddActor(obj_actor)
renderer.ResetCamera()

render_window.Render()
render_window_interactor.Start()

# # Create a vtkPolyData object (replace with your data)
# points = vtk.vtkPoints()
# points.InsertNextPoint(1, 2, 3)
# points.InsertNextPoint(4, 5, 6)
# polydata = vtk.vtkPolyData()
# polydata.SetPoints(points)
#
# # Create a transform to swap Y and Z coordinates
# transform = vtk.vtkTransform()
# matrix = transform.GetMatrix()
# matrix.Identity()
# matrix.SetElement(1, 1, 0)
# matrix.SetElement(1, 2, 1)
# matrix.SetElement(2, 1, 1)
# matrix.SetElement(2, 2, 0)
# print(matrix)
#
# # Create a transform filter
# transform_filter = vtk.vtkTransformFilter()
# transform_filter.SetInputData(polydata)
# transform_filter.SetTransform(transform)
# transform_filter.Update()
#
# # Get the transformed polydata
# transformed_polydata = transform_filter.GetOutput()
#
# # Verify the coordinate swap
# for i in range(transformed_polydata.GetNumberOfPoints()):
#     p = transformed_polydata.GetPoint(i)
#     print(f"Point {i}: {p}")