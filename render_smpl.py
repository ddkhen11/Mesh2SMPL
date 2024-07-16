import argparse
import glob
import subprocess

import trimesh
import numpy as np

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

    subprocess.run(["python", "third_party/MultiviewSMPLifyX/main.py", "--config", config, "--data_folder", data_folder, "--output_folder", output_folder, "--model_folder", model_folder, "--vposer_ckpt", vposer_ckpt, "--use_cuda", use_cuda, "--gender", gender], check=True)

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
    Aligns the rendered SMPL model to the original position of the input mesh.
    """
    print("Aligning SMPL model.")
    
    # Define file paths for the SMPL model and original mesh
    smpl_model_path = f"./dataset_example/mesh_data/{mesh_folder_name}/smpl/smpl_mesh.obj"
    norm_og_scan_path = glob.glob(f"./dataset_example/mesh_data/{mesh_folder_name}/original/*.obj")[0]
    
    # Load the SMPL model mesh
    smpl_mesh = trimesh.load(smpl_model_path)
    
    # Load the original mesh
    og_mesh = trimesh.load(norm_og_scan_path)
    
    # Get vertices of both meshes
    smpl_vertices = smpl_mesh.vertices
    og_vertices = og_mesh.vertices

    # Find the lowest x-values of both meshes
    x_lowest_smpl = np.min(smpl_vertices[:, 0]) 
    x_lowest_og = np.min(og_vertices[:, 0]) 
    
    # Find the lowest points of both meshes along the y-axis
    lowest_point_smpl = np.min(smpl_vertices[:, 1]) 
    lowest_point_og = np.min(og_vertices[:, 1]) 

    # Find the lowest z-values of both meshes
    z_lowest_smpl = np.min(smpl_vertices[:, 2]) 
    z_lowest_og = np.min(og_vertices[:, 2]) 
    
    # Compute the translation required to align the points
    translation_x = x_lowest_og - x_lowest_smpl
    translation_y = lowest_point_og - lowest_point_smpl
    translation_z = z_lowest_og - z_lowest_smpl
    translation_matrix = np.array([translation_x, translation_y, translation_z])
    
    # Apply the translation to the SMPL mesh vertices
    translated_vertices_smpl = smpl_vertices + translation_matrix
    smpl_mesh.vertices = translated_vertices_smpl
    
    # Export the translated SMPL mesh
    trimesh.base.export_mesh(smpl_mesh, smpl_model_path)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--mesh-folder-name', dest='mesh_folder_name', 
                        required=True, type=str,
                        help='The name of the folder containing your mesh data')
    parser.add_argument('--gender', dest='gender',
                        required=True, type=str,
                        help='The gender of the subject of your mesh scan', 
                        choices=["male", "female", "neutral"])

    args = parser.parse_args()
    mesh_folder_name = args.mesh_folder_name
    gender = args.gender

    # render_smpl(mesh_folder_name, gender)
    # rescale_smpl(mesh_folder_name)
    align_smpl(mesh_folder_name)