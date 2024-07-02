# Mesh2SMPL

Mesh2SMPL is a project that utilizes the PaMIR library for image-based human reconstruction. This project includes various functionalities to process and convert mesh data into parametric models.

## Citation

If you use this code, please cite the following paper:

```bibtex
@misc{zheng2020pamir,
    title={PaMIR: Parametric Model-Conditioned Implicit Representation for Image-based Human Reconstruction},
    author={Zerong Zheng, Tao Yu, Yebin Liu, Qionghai Dai},
    journal={IEEE Transactions on Pattern Analysis and Machine Intelligence},
    year={2021},
    primaryClass={cs.CV}
}
```

## Installation and Usage
To set up and run the Mesh2SMPL repository using Anaconda, follow the detailed step-by-step instructions below. You can use either PowerShell or the Anaconda Command Prompt to execute these instructions.

1. **Create and activate a conda environment for Python 3.9**

    First, create a new conda environment named myenv with Python 3.9 and activate it:
    ```cmd
    conda create --name myenv python=3.9
    conda activate myenv
    ```

2. Clone the repository and navigate into it

    Clone the Mesh2SMPL repository and navigate into the directory:
    ```cmd
    git clone --recurse-submodules https://github.com/ddkhen11/Mesh2SMPL
    cd Mesh2SMPL
    ```

4. Install dependencies using pip

    Install the necessary dependencies using pip:
    ```cmd
    pip install --upgrade setuptools wheel build
    pip install pyembree
    pip install -r requirements.txt
    ```

6. Download the PyOpenGL wheel specific to Python 3.9

    Download the PyOpenGL wheel specific to Python 3.9 from [Google Drive](https://drive.google.com/drive/folders/1mz7faVsrp0e6IKCQh8MyZh-BcCqEGPwx). The required file is named `PyOpenGL-3.1.7-cp39-cp39-win_amd64.whl`. Save this file to a known location on your computer.

8. Install PyOpenGL from the downloaded wheel

    Navigate to the directory where you downloaded the wheel file:
    ```cmd
    cd path\to\downloaded\wheel
    ```
    Install the PyOpenGL package from the downloaded wheel file:
    ```cmd
    pip install PyOpenGL-3.1.7-cp39-cp39-win_amd64
    ```

6. Prepare your 3D mesh data

    Place a folder containing your `.obj` mesh file, `.mtl` file, and `.jpg` texture file into `dataset_example/mesh_data`. Ensure that your mesh file contains UV coordinates.

8. Run the main.py script

    Navigate back to the Mesh2SMPL directory and execute the `main.py` script to process your mesh data:
    ```cmd
    python main.py
    ```

8. Acess your results
    After running the script, your results will be located in the `dataset_example/image_data directory`.
