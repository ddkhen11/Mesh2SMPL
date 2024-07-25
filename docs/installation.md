# Mesh2SMPL Installation

Prerequisites: 64-bit Windows system, Python, Anaconda

To set up and run the Mesh2SMPL repository using Anaconda, follow the detailed step-by-step instructions below. You can use either PowerShell or the Anaconda Command Prompt to execute these instructions.

### 1. Setup Multiview Images Script

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

### 2. Setup Fitting OpenPose to the Multiview Images Script

Due to the complexities of installing and running OpenPose, we will instead use [AlphaPose](https://github.com/MVIG-SJTU/AlphaPose) on our multiview images and then convert the AlphaPose keypoints to OpenPose keypoints. The following set of instructions is a detailed guide to installing AlphaPose, so please refer to AlphaPose's GitHub repository if you need to troubleshoot anything.

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

2. **Install dependencies using pip**

    Install the necessary dependencies using pip:
    ```cmd
    pip install -r requirements-pose.txt
    ```

3. **Delete necessary lines and files from AlphaPose directory**

    In `third_party/AlphaPose` open `setup.py` and delete [line 211](https://github.com/MVIG-SJTU/AlphaPose/blob/master/setup.py#L211). Don't forget to save the file before exiting.

    In the same folder, delete the `setup.cfg` file.

4. **Build and install AlphaPose**

    Navigate to the AlphaPose directory, build and install AlphaPose, and navigate back to the Mesh2SMPL directory:
    ```cmd
    cd third_party/AlphaPose
    python setup.py build develop
    cd ../..
    ```

5. **Download pretrained models**

    First, download the YOLO object detection model from this [link](https://drive.google.com/file/d/1D47msNOOiJKvPOXlnpyzdKA3k6E97NTC/view) and place the file in `third_party/AlphaPose/detector/yolo/data`.

    Then, download the pretrained Fast Pose pose estimation model from this [link](https://drive.google.com/file/d/1Bb3kPoFFt-M0Y3ceqNO8DTXi1iNDd4gI/view) and place the file in the `third_party/AlphaPose/pretrained_models` directory.


### 3. Setup rendering the SMPL Model

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
    python -m pip install --upgrade pip
    pip install -r requirements-smpl.txt
    conda install pytorch-cpu==1.0.0 torchvision-cpu==0.2.1 cpuonly -c pytorch
    ```

    Also, install the necessary dependencies to help align your outputted SMPL model with your input mesh:
    ```cmd
    cd nricp/required_libs/scikit-sparse-0.4.4
    conda install -c conda-forge suitesparse

    # Assuming your current conda environment is named 'fit-smpl'
    $env:SUITESPARSE_INCLUDE_DIR='c:\users\<user>\.conda\envs\fit-smpl\Library\include\suitesparse'
    $env:SUITESPARSE_LIBRARY_DIR='c:\users\<user>\.conda\envs\fit-smpl\Library\lib'

    python setup.py install
    cd ../../..
    ```

    Replace `<user>` with the name of the current user on your computer.

3. **Download and clean the SMPL model files**

    Go to https://smpl.is.tue.mpg.de/, make an account, and download version 1.0.0 of SMPL for Python Users from the downloads page. Extract this zip file. In the extracted folder, go to `SMPL_python_v.1.0.0/smpl/models`. Copy and paste the files in this folder to `tools/smpl_models` in your Mesh2SMPL directory.

    Then, go to https://smplify.is.tue.mpg.de/, make an account, and download `SMPLIFY_CODE_V2.ZIP` from the downloads page. Extract this zip file. In the extracted folder, go to `smplify_public/code/models`. Copy and paste `basicModel_neutral_lbs_10_207_0_v1.0.0.pkl` to `tools/smpl_models` in your Mesh2SMPL directory.

    Finally, run the following command (make sure your current directory is still Mesh2SMPL):
    ```cmd
    python tools/clean_models.py --input-models tools/smpl_models/*.pkl --output-folder third_party/MultiviewSMPLifyX/smplx/models/smpl
    ```

4. **Download pretrained VPoser models**

    Go to https://smpl-x.is.tue.mpg.de/, make an account, and download `VPoser v1.0 - CVPR'19 (2.5 MB)` from the downloads page. Extract this zip file. In the extracted folder, go to `vposer_v1_0/snapshots`. Copy and paste the `*.pt` files to `third_party/MultiviewSMPLifyX/vposer/models/snapshots` in your Mesh2SMPL directory.

##

### After all of this setup, you are ready to run Mesh2SMPL. Follow the instructions in [run.md](run.md).