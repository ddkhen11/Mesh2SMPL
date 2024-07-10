# Mesh2SMPL

Mesh2SMPL is a project that utilizes the [MultiviewSMPLifyX](https://github.com/ZhengZerong/MultiviewSMPLifyX) and [PaMIR](https://github.com/ZhengZerong/PaMIR) projects to convert a textured mesh scan of a human into a SMPL model.

## Installation and Usage
To set up and run the Mesh2SMPL repository using Anaconda, follow the detailed step-by-step instructions below. You can use either PowerShell or the Anaconda Command Prompt to execute these instructions.

### 1. Get Multiview Images

1. **Create and activate a conda environment for Python 3.9**

    First, create a new conda environment for Python 3.9 and activate it:
    ```cmd
    conda create --name multiview python=3.9
    conda activate multiview
    ```

2. **Clone the repository and navigate into it**

    Clone the Mesh2SMPL repository and navigate into the directory:
    ```cmd
    git clone --recurse-submodules https://github.com/ddkhen11/Mesh2SMPL
    cd Mesh2SMPL
    ```

3. **Install dependencies using pip**

    Install the necessary dependencies using pip:
    ```cmd
    pip install --upgrade setuptools wheel build
    pip install pyembree
    pip install -r requirements-multiview.txt
    ```

4. **Download the PyOpenGL wheel specific to Python 3.9**

    Download the PyOpenGL wheel specific to Python 3.9 from [Google Drive](https://drive.google.com/drive/folders/1mz7faVsrp0e6IKCQh8MyZh-BcCqEGPwx). The required file is named `PyOpenGL-3.1.7-cp39-cp39-win_amd64.whl`. Save this file to a known location on your computer.

5. **Install PyOpenGL from the downloaded wheel**

    Navigate to the directory where you downloaded the wheel file:
    ```cmd
    cd path\to\downloaded\wheel
    ```
    Install the PyOpenGL package from the downloaded wheel file:
    ```cmd
    pip install PyOpenGL-3.1.7-cp39-cp39-win_amd64.whl
    ```
    After that is done, navigate back to the Mesh2SMPL directory:
    ```cmd
    cd path\to\Mesh2SMPL
    ```

6. **Prepare your 3D mesh data**

    Place a folder containing your `.obj` mesh file, `.mtl` file, and `.jpg` texture file into `dataset_example/mesh_data`. Ensure that your mesh file contains UV coordinates.

7. **Run the `get_multiview_images.py` script**

    Navigate back to the Mesh2SMPL directory and execute the `get_multiview_images.py` script to process your mesh data:
    ```cmd
    python get_multiview_images.py
    ```

8. **Access your results**

   After running the script, your results will be located in the `dataset_example/image_data` directory.

### 2. Fit OpenPose to the Multiview Images

Due to the complexities of installing and running OpenPose, we will instead use [AlphaPose](https://github.com/MVIG-SJTU/AlphaPose) on our multiview images and then convert the AlphaPose keypoints to OpenPose keypoints. The following set of instructions is a detailed guide to installing and running AlphaPose, so please refer to AlphaPose's GitHub repository if you need to troubleshoot anything.

1. **Create and activate a conda environment for Python 3.7**

    If your previous conda environment is still active, make sure you deactivate it first:
    ```cmd
    conda deactivate
    ```
    Then create a new conda environment for Python 3.7 and activate it:
    ```cmd
    conda create --name alphapose python=3.7
    conda activate alphapose
    ```

2. **Clone the repository and navigate into it**

    Check if your current directory is still `Mesh2SMPL`:
    ```cmd
    ls
    ```
    If it is, make sure you navigate out of it:
    ```cmd
    cd ..
    ```
    Then, clone the AlphaPose repository and navigate into the directory:
    ```cmd
    git clone https://github.com/MVIG-SJTU/AlphaPose.git
    cd AlphaPose
    ```
    Here's how your folder structure should look right now:
    ```
    ├── AlphaPose  # current directory
    └── Mesh2SMPL
    ```

3. **Install dependencies using pip**

    Install the necessary dependencies using pip:
    ```cmd
    pip install Cython easydict matplotlib numpy natsort opencv-python PyYAML scipy setuptools torch torchvision tqdm
    ```

4. **Delete necessary lines and files from AlphaPose directory**

    In the AlphaPose directory (which should be your current directory right now), open `setup.py` and delete [line 211](https://github.com/MVIG-SJTU/AlphaPose/blob/master/setup.py#L211). Don't forget to save the file before exiting.

    In the same directory, delete the `setup.cfg` file.

5. **Build and install AlphaPose**

    Build and install AlphaPose:
    ```cmd
    python setup.py build develop
    ```

6. **Download pretrained models**

    First, download the YOLO object detection model from this [link](https://drive.google.com/file/d/1D47msNOOiJKvPOXlnpyzdKA3k6E97NTC/view) and place the file in `detector/yolo/data`.

    Then, download the pretrained Fast Pose pose estimation model from this [link](https://drive.google.com/file/d/1Bb3kPoFFt-M0Y3ceqNO8DTXi1iNDd4gI/view) and place the file in the `pretrained_models` directory.

7. **Run AlphaPose on the multiview images**

    Run AlphaPose on the multiview images to extract the 2D pose keypoints from each image:
    ```cmd
    python scripts/demo_inference.py --cfg configs/halpe_coco_wholebody_136/resnet/256x192_res50_lr1e-3_2x-regression.yaml --checkpoint pretrained_models/multi_domain_fast50_regression_256x192.pth --indir ../Mesh2SMPL/dataset_example/image_data/<your-mesh-folder-name>/color --outdir ../Mesh2SMPL/dataset_example/image_data/<your-mesh-folder-name> 
    ```
    
    Replace `<your-mesh-folder-name>` with what you named the folder containing your mesh file in step 6 of the previous set of instructions. 

8. **Access your results**

    After running AlphaPose on the multiview images, your AlphaPose keypoints will be in `alphapose-results.json` in `Mesh2SMPL/dataset_example/image_data/<your-mesh-folder-name>`.

9. **Convert AlphaPose keypoints to OpenPose keypoints**

    First, navigate out of the AlphaPose directory and navigate back into the Mesh2SMPL directory:
    ```cmd
    cd ../Mesh2SMPL
    ```
    Then, run the script to convert the AlphaPose keypoints to OpenPose keypoints, where `<your-mesh-folder-name>` is what you named the folder containing your mesh file in step 6 of the previous set of instructions:
    ```cmd
    python tools/alpha_to_open.py --alphapose-json dataset_example/image_data/<your-mesh-folder-name>/alphapose-results.json
    ```
    Your OpenPose keypoints will be in `Mesh2SMPL/dataset_example/image_data/<your-mesh-folder-name>/keypoints`.

### 3. Render the SMPL Model

1. **Create and activate a conda environment for Python 3.6**

    If your previous conda environment is still active, make sure you deactivate it first:
    ```cmd
    conda deactivate
    ```
    Then create a new conda environment for Python 3.6 and activate it:
    ```cmd
    conda create --name fit-smpl python=3.6
    conda activate fit-smpl
    ```

2. **Install dependencies**

    Install the necessary dependencies:
    ```cmd
    pip install -r requirements-smpl.txt
    conda install pytorch-cpu==1.0.0 torchvision-cpu==0.2.1 cpuonly -c pytorch
    ```

3. **Download and clean the SMPL model files**

    Go to https://smpl.is.tue.mpg.de/, make an account, and download version 1.0.0 of SMPL for Python Users from the downloads page. Extract this zip file. In the extracted folder, go to `SMPL_python_v.1.0.0/smpl/models`. Copy and paste the files in this folder to `tools/smpl_models` in your Mesh2SMPL directory.

    Then, go to https://smplify.is.tue.mpg.de/, make an account, and download `SMPLIFY_CODE_V2.ZIP` from the downloads page. Extract this zip file. In the extracted folder, go to `smplify_public/code/models`. Copy and paste `basicModel_neutral_lbs_10_207_0_v1.0.0.pkl` to `tools/smpl_models` in your Mesh2SMPL directory.

    Finally, run the following command (make sure your current directory is still Mesh2SMPL):
    ```cmd
    python tools/clean_models.py --input-models tools/smpl_models/*.pkl --output-folder third_party/MultiviewSMPLifyX/smplx/models/smpl
    ```

4. **Download pretrained VPoser models**

    Go to https://smpl-x.is.tue.mpg.de/, make an account, and download `VPoser v1.0 - CVPR'19 (2.5 MB)` from the downloads page. Extract this zip file. In the extracted folder, go to `vposer_v1_0/snapshots`. Copy and paste the `*.pt` files to `third_party/MultiviewSMPLifyX/vposer/models/snapshots` in your Mesh2SMPL directory.

5. **Render the SMPL model from the multiview images and fitted 2D poses**

    Run the following command to render the SMPL model:
    ```cmd 
    python render_smpl.py <your-mesh-folder-name> dataset --gender <your-gender>
    ```
    Replace `<your-mesh-folder-name>` with what you named the folder containing your mesh file in step 6 of the first set of instructions. Replace `<your-gender>` with the gender of the subject of your mesh scan (male, female, neutral).

6. **Access your results**

   After running the command, your results will be located in the `dataset_example/mesh_data/<your-mesh-folder-name>/smpl` directory.

## Citation

If you use this code, please cite the following papers:

```bibtex
@ARTICLE{9321139,
  author={Zheng, Zerong and Yu, Tao and Liu, Yebin and Dai, Qionghai},
  journal={IEEE Transactions on Pattern Analysis and Machine Intelligence}, 
  title={PaMIR: Parametric Model-Conditioned Implicit Representation for Image-Based Human Reconstruction}, 
  year={2022},
  volume={44},
  number={6},
  pages={3170-3184},
  doi={10.1109/TPAMI.2021.3050505}}


@INPROCEEDINGS{8953319,
  author={Pavlakos, Georgios and Choutas, Vasileios and Ghorbani, Nima and Bolkart, Timo and Osman, Ahmed A. and Tzionas, Dimitrios and Black, Michael J.},
  booktitle={2019 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)}, 
  title={Expressive Body Capture: 3D Hands, Face, and Body From a Single Image}, 
  year={2019},
  volume={},
  number={},
  pages={10967-10977},
  doi={10.1109/CVPR.2019.01123}}


@ARTICLE{9954214,
  author={Fang, Hao-Shu and Li, Jiefeng and Tang, Hongyang and Xu, Chao and Zhu, Haoyi and Xiu, Yuliang and Li, Yong-Lu and Lu, Cewu},
  journal={IEEE Transactions on Pattern Analysis and Machine Intelligence}, 
  title={AlphaPose: Whole-Body Regional Multi-Person Pose Estimation and Tracking in Real-Time}, 
  year={2023},
  volume={45},
  number={6},
  pages={7157-7173},
  doi={10.1109/TPAMI.2022.3222784}}


@INPROCEEDINGS{8237518,
  author={Fang, Hao-Shu and Xie, Shuqin and Tai, Yu-Wing and Lu, Cewu},
  booktitle={2017 IEEE International Conference on Computer Vision (ICCV)}, 
  title={RMPE: Regional Multi-person Pose Estimation}, 
  year={2017},
  volume={},
  number={},
  pages={2353-2362},
  doi={10.1109/ICCV.2017.256}}


@INPROCEEDINGS{8954341,
  author={Li, Jiefeng and Wang, Can and Zhu, Hao and Mao, Yihuan and Fang, Hao-Shu and Lu, Cewu},
  booktitle={2019 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)}, 
  title={CrowdPose: Efficient Crowded Scenes Pose Estimation and a New Benchmark}, 
  year={2019},
  volume={},
  number={},
  pages={10855-10864},
  doi={10.1109/CVPR.2019.01112}}
```