import argparse
import subprocess

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

    render_smpl(mesh_folder_name, gender)