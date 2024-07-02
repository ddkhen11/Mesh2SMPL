# Mesh2SMPL

Mesh2SMPL is a project that utilizes the [MultiviewSMPLifyX](https://github.com/ZhengZerong/MultiviewSMPLifyX) and [PaMIR](https://github.com/ZhengZerong/PaMIR) projects to convert a textured mesh scan of a human into a SMPL model.

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
  keywords={Image reconstruction;Three-dimensional displays;Surface reconstruction;Solid modeling;Estimation;Training;Shape;Body pose;human reconstruction;surface representation;parametric body model;implicit surface function},
  doi={10.1109/TPAMI.2021.3050505}}


@INPROCEEDINGS{8953319,
  author={Pavlakos, Georgios and Choutas, Vasileios and Ghorbani, Nima and Bolkart, Timo and Osman, Ahmed A. and Tzionas, Dimitrios and Black, Michael J.},
  booktitle={2019 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)}, 
  title={Expressive Body Capture: 3D Hands, Face, and Body From a Single Image}, 
  year={2019},
  volume={},
  number={},
  pages={10967-10977},
  keywords={Face;Gesture;and Body Pose;3D from Single Image},
  doi={10.1109/CVPR.2019.01123}}
```

## Installation and Usage
To set up and run the Mesh2SMPL repository using Anaconda, follow the detailed step-by-step instructions below. You can use either PowerShell or the Anaconda Command Prompt to execute these instructions.

### 1. Get Multiview Images

1. **Create and activate a conda environment for Python 3.9**

    First, create a new conda environment for Python 3.9 and activate it:
    ```cmd
    conda create --name myenv python=3.9
    conda activate myenv
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
    pip install -r requirements.txt
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
    pip install PyOpenGL-3.1.7-cp39-cp39-win_amd64
    ```

6. **Prepare your 3D mesh data**

    Place a folder containing your `.obj` mesh file, `.mtl` file, and `.jpg` texture file into `dataset_example/mesh_data`. Ensure that your mesh file contains UV coordinates.

7. **Run the `get_multiview_images.py` script**

    Navigate back to the Mesh2SMPL directory and execute the `get_multiview_images.py` script to process your mesh data:
    ```cmd
    python get_multiview_images.py
    ```

8. **Access your results**

   After running the script, your results will be located in the `dataset_example/image_data directory`.

### 2. Fit OpenPose to the Multiview Images

TBD

### 3. Render the SMPL Model

TBD