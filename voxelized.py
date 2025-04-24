# import open3d as o3d
# import numpy as np
#
#
# def voxel_grid_to_numpy(voxel_grid):
#     """
#     Converts an Open3D VoxelGrid to a NumPy 3D array.
#
#     Args:
#         voxel_grid: The Open3D VoxelGrid object.
#
#     Returns:
#         A NumPy 3D array representing the voxel grid.
#     """
#     voxels = voxel_grid.get_voxels()
#     if not voxels:
#         return np.array([])
#
#     indices = np.stack([voxel.grid_index for voxel in voxels])
#
#     # Calculate the dimensions of the grid
#     min_bound = np.min(indices, axis=0)
#     max_bound = np.max(indices, axis=0)
#     grid_size = max_bound - min_bound + 1
#
#     # Create an empty NumPy array
#     numpy_grid = np.zeros(grid_size, dtype=bool)
#
#     # Fill the NumPy array with voxel data
#     indices_shifted = indices - min_bound
#     numpy_grid[indices_shifted[:, 0], indices_shifted[:, 1], indices_shifted[:, 2]] = True
#
#     return numpy_grid
#
#
# # Example usage:
# # 1. Create a sample point cloud (replace with your data)
# pcd = o3d.geometry.PointCloud()
# pcd.points = o3d.utility.Vector3dVector(np.random.rand(100, 3))
#
# # 2. Create a voxel grid from the point cloud
# voxel_size = 0.1
# voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(pcd, voxel_size=voxel_size)
#
# # 3. Convert the voxel grid to a NumPy array
# numpy_array = voxel_grid_to_numpy(voxel_grid)
#
# # 4. Print the shape of the NumPy array
# print(f"NumPy array shape: {numpy_array.shape}")
#
# import open3d as o3d
# import numpy as np


def voxel_grid_to_numpy(voxel_grid):
    """
    Converts an Open3D VoxelGrid to a grayscale NumPy 3D array.

    Args:
        voxel_grid: The Open3D VoxelGrid object.

    Returns:
        A NumPy 3D array representing the voxel grid in grayscale.
    """
    bounds_min = voxel_grid.get_min_bound()
    bounds_max = voxel_grid.get_max_bound()

    # Calculate grid dimensions
    dimensions = np.ceil((bounds_max - bounds_min) / voxel_grid.voxel_size).astype(int)

    # Initialize an empty NumPy array with the calculated dimensions
    numpy_grid = np.zeros(dimensions, dtype=np.uint8)

    # Get the voxel data
    voxels = voxel_grid.get_voxels()

    # Iterate through the voxels and update the NumPy array
    for voxel in voxels:
        index = voxel.grid_index
        # Calculate grayscale value from color (if color exists, otherwise use 255)
        if voxel.color is not None:
            gray_value = int(np.mean(voxel.color) * 255)
        else:
            gray_value = 255
        numpy_grid[index[0], index[1], index[2]] = gray_value

    return numpy_grid


# Example usage (assuming you have a voxel_grid object):
# Create a sample voxel grid (replace with your actual voxel grid)
pcd = o3d.geometry.PointCloud.create_from_point_cloud_down_sample(
    o3d.geometry.PointCloud.make_xyz_grid(size=5, extent=1),
    voxel_size=0.2)
voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(pcd, voxel_size=0.2)

numpy_array = voxel_grid_to_numpy(voxel_grid)

# Now you have the voxel grid as a grayscale NumPy array
print(f"NumPy array shape: {numpy_array.shape}")
print(f"NumPy array data type: {numpy_array.dtype}")