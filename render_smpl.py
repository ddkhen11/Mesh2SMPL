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
    Rescales the rendered SMPL model to the original size of the input mesh.
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

def align_smpl(mesh_folder_name):
    """
    Aligns the rescaled SMPL model to the original scan using the Iterative Closest Point (ICP) algorithm.
    """
    # Define file paths for the SMPL model and original mesh
    smpl_model_path = f"./dataset_example/mesh_data/{mesh_folder_name}/smpl/smpl_mesh.obj"
    norm_og_scan_path = glob.glob(f"./dataset_example/mesh_data/{mesh_folder_name}/original/*.obj")[0]

    # Get point cloud of original mesh
    og_mesh = o3d.io.read_triangle_mesh(norm_og_scan_path)
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
    
    # Perform point-to-point ICP
    reg_icp = o3d.pipelines.registration.registration_icp(
        cloud_smpl, cloud_og, max_correspondence_distance=50, 
        estimation_method=o3d.pipelines.registration.TransformationEstimationPointToPoint()
    )
    
    # Check if ICP converged
    if reg_icp.fitness < 0.5:
        print(f"ICP did not converge. Fitness score: {reg_icp.fitness:.2f}. Consider adjusting ICP parameters.")
    else:
         print(f"ICP converged. Fitness score: {reg_icp.fitness:.2f}")
    
    # Apply transformation
    smpl_mesh.transform(reg_icp.transformation)
    
    # Save the aligned mesh
    o3d.io.write_triangle_mesh(smpl_model_path, smpl_mesh)
    
    print(f"Mesh B (SMPL model) aligned to Mesh A (original scan) and saved to '{smpl_model_path}'")

    
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
    align_smpl(mesh_folder_name)