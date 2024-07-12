import argparse
import os
import subprocess


def fit_alphapose(mesh_folder_name):
    """
    Fit OpenPose on multiview images
    """

    # Arguments for running AlphaPose
    cfg = "configs/halpe_coco_wholebody_136/resnet/256x192_res50_lr1e-3_2x-regression.yaml"
    checkpoint = "pretrained_models/multi_domain_fast50_regression_256x192.pth"
    indir = f"../../dataset_example/image_data/{mesh_folder_name}/color"
    outdir = f"../../dataset_example/image_data/{mesh_folder_name}"

    print("Running AlphaPose fitting.")

    os.chdir("third_party/AlphaPose")

    subprocess.run(["python", "scripts/demo_inference.py", "--cfg", cfg, "--checkpoint", checkpoint, "--indir", indir, "--outdir", outdir], check=True)

    os.chdir("../..")


def convert_poses(mesh_folder_name):
    """
    Convert AlphaPose poses to OpenPose poses
    """
    # Arguments
    alphapose_json = f"dataset_example/image_data/{mesh_folder_name}/alphapose-results.json"

    print("Converting AlphaPose keypoints to OpenPose keypoints.")

    subprocess.run(["python", "tools/alpha_to_open.py", "--alphapose-json", alphapose_json])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--mesh-folder-name', dest='mesh_folder_name', 
                        required=True, type=str,
                        help='The name of the folder containing your mesh data')

    args = parser.parse_args()
    mesh_folder_name = args.mesh_folder_name

    fit_alphapose(mesh_folder_name)
    convert_poses(mesh_folder_name)