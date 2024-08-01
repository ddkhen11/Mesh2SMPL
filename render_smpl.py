import argparse
import glob
import os
import subprocess

import trimesh
import numpy as np
import open3d as o3d

def render_smpl(mesh_folder_name, gender):
    """
    Renders a SMPL model from the inputted multiview images and 2D pose keypoints fitted to each image.
    """
    # Arguments for running main.py in MultiviewSMPLifyX
    config = "third_party/MultiviewSMPLifyX/cfg_files/fit_smpl.yaml"
    data_folder = f"./dataset_example/image_data//{mesh_folder_name}"
    output_folder = f"./dataset_example/mesh_data//{mesh_folder_name}/smpl"
    model_folder = "third_party/MultiviewSMPLifyX/smplx/models"
    vposer_ckpt = "third_party/MultiviewSMPLifyX/vposer/models"
    use_cuda = "False"
    gender = gender

    print("Rendering SMPL models.")

    subprocess.run([
        "python", "third_party/MultiviewSMPLifyX/main.py", 
        "--config", config, 
        "--data_folder", data_folder, 
        "--output_folder", output_folder, 
        "--model_folder", model_folder, 
        "--vposer_ckpt", vposer_ckpt, 
        "--use_cuda", use_cuda, 
        "--gender", gender
        ], 
        check=True)

def rescale_smpl(mesh_folder_name):
    """
    Rescales the rendered SMPL model and associated joints to the original size of the input mesh.
    """
    print("Rescaling SMPL model.")
    
    # Define file paths for the SMPL model
    smpl_model_path = f"./dataset_example/mesh_data/{mesh_folder_name}/smpl/smpl_mesh.obj"
    scale_file_path = f"./dataset_example/mesh_data/{mesh_folder_name}/scale.txt"
    
    # Load the SMPL model mesh
    smpl_mesh = trimesh.load(smpl_model_path)
    
    # Read the scale factor from the scale.txt file
    with open(scale_file_path, 'r') as file:
        scale = float(file.read().strip())
    
    # Rescale the SMPL model vertices
    smpl_mesh.vertices /= scale
    
    # Export the rescaled SMPL mesh
    trimesh.base.export_mesh(smpl_mesh, smpl_model_path)

    # Rescale the joints
    joints_path = os.path.join(os.path.split(smpl_model_path)[0], "joints.npy")
    joints = np.load(joints_path)
    joints /= scale
    np.save(joints_path, joints)

def align_smpl(mesh_folder_name, mcd_multiplier):
    """
    Aligns the rescaled SMPL model to the original scan using RANSAC-based global registration followed by ICP.
    """
    print("Aligning SMPL model.")

    # Define file paths for the SMPL model and original mesh
    smpl_model_path = f"./dataset_example/mesh_data/{mesh_folder_name}/smpl/smpl_mesh.obj"
    norm_og_scan_path = glob.glob(f"./dataset_example/mesh_data/{mesh_folder_name}/original/*.obj")[0]

    # Load original mesh
    og_mesh = o3d.io.read_triangle_mesh(norm_og_scan_path)

    # Get point cloud of original mesh
    if len(og_mesh.triangles) > 0:
        cloud_og = og_mesh.sample_points_uniformly(number_of_points=10000)
    else:
        temp_path = f"./dataset_example/mesh_data/{mesh_folder_name}/original/temp.ply"
        og_mesh_obj = trimesh.load_mesh(norm_og_scan_path)
        og_mesh_obj.export(temp_path)
        cloud_og = o3d.io.read_point_cloud(temp_path)
        os.remove(temp_path)
    
    # Load SMPL model mesh
    smpl_mesh = o3d.io.read_triangle_mesh(smpl_model_path)

    # Convert SMPL model mesh to point cloud
    cloud_smpl = smpl_mesh.sample_points_uniformly(number_of_points=10000)
    
    # Compute normals for the point clouds (for more robust ICP)
    cloud_og.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
    cloud_smpl.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
    
    # Perform global registration using RANSAC
    def execute_global_registration(source_down, target_down, source_fpfh, target_fpfh, voxel_size):
        distance_threshold = voxel_size * 1.5
        result = o3d.pipelines.registration.registration_ransac_based_on_feature_matching(
            source_down, target_down, source_fpfh, target_fpfh, True,
            distance_threshold,
            o3d.pipelines.registration.TransformationEstimationPointToPoint(False),
            3, [
                o3d.pipelines.registration.CorrespondenceCheckerBasedOnEdgeLength(
                    0.9),
                o3d.pipelines.registration.CorrespondenceCheckerBasedOnDistance(
                    distance_threshold)
            ], o3d.pipelines.registration.RANSACConvergenceCriteria(100000, 0.999))
        return result
    
    # Prepare datasets for global registration
    def prepare_dataset(voxel_size):
        trans_init = np.identity(4)  # Initial transformation (identity matrix)
        
        # Downsample and preprocess point clouds
        source_down, source_fpfh = preprocess_point_cloud(cloud_smpl, voxel_size)
        target_down, target_fpfh = preprocess_point_cloud(cloud_og, voxel_size)
        
        return source_down, target_down, source_fpfh, target_fpfh, trans_init
    
    # Function to preprocess point clouds
    def preprocess_point_cloud(pcd, voxel_size):
        pcd_down = pcd.voxel_down_sample(voxel_size)
    
        radius_normal = voxel_size * 2
        pcd_down.estimate_normals(
            o3d.geometry.KDTreeSearchParamHybrid(radius=radius_normal, max_nn=30))
    
        radius_feature = voxel_size * 5
        pcd_fpfh = o3d.pipelines.registration.compute_fpfh_feature(
            pcd_down,
            o3d.geometry.KDTreeSearchParamHybrid(radius=radius_feature, max_nn=100))
        return pcd_down, pcd_fpfh
    
    # Execute global registration
    voxel_size = 0.05  # Voxel size for downsampling
    source_down, target_down, source_fpfh, target_fpfh, trans_init = prepare_dataset(voxel_size)
    result_ransac = execute_global_registration(source_down, target_down, source_fpfh, target_fpfh, voxel_size)
    
    # Perform ICP refinement
    def refine_registration(source, target, transformation):
        distance_threshold = voxel_size * 0.4
        result = o3d.pipelines.registration.registration_icp(
            source, target, distance_threshold, transformation,
            o3d.pipelines.registration.TransformationEstimationPointToPlane())
        return result
    
    # Refine alignment using ICP
    result_icp = refine_registration(cloud_smpl, cloud_og, result_ransac.transformation)
    
    # Apply final transformation to SMPL mesh
    smpl_mesh.transform(result_icp.transformation)
    
    # Print Chamfer distance
    dists1 = cloud_og.compute_point_cloud_distance(cloud_smpl)
    dists1 = np.asarray(dists1)
    dists2 = cloud_smpl.compute_point_cloud_distance(cloud_og)
    dists2 = np.asarray(dists2)
    chamfer = (np.mean(dists1) + np.mean(dists2)) / 2
    print(f"Chamfer distance between SMPL model and original scan: {chamfer}")
    
    # Save the aligned mesh
    o3d.io.write_triangle_mesh(smpl_model_path, smpl_mesh)
    print(f"SMPL model aligned to original scan")

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--mesh-folder-name', dest='mesh_folder_name', 
                        required=True, type=str,
                        help='The name of the folder containing your mesh data')
    parser.add_argument('-g', '--gender', dest='gender',
                        required=True, type=str,
                        help='The gender of the subject of your mesh scan', 
                        choices=["male", "female", "neutral"])

    args = parser.parse_args()
    mesh_folder_name = args.mesh_folder_name
    gender = args.gender

    render_smpl(mesh_folder_name, gender)
    rescale_smpl(mesh_folder_name)
    align_smpl(mesh_folder_name, 0.5)