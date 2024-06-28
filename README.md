# Mesh2SMPL

Mesh2SMPL is a project that utilizes the PaMIR library for image-based human reconstruction. This project includes various functionalities to process and convert mesh data.

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

## Instructions to Run the Program

1. Create a conda environment for Python 3.9:
```cmd
conda create --name myenv python=3.9
conda activate myenv
```

2. Install dependencies using pip:
```cmd
pip install -r requirements.txt
```

3. Download the PyOpenGL wheel specific to Python 3.9 from [Google Drive](https://drive.google.com/drive/folders/1mz7faVsrp0e6IKCQh8MyZh-BcCqEGPwx) (filename: PyOpenGL-3.1.7-cp39-cp39-win_amd64.whl).

4. Install PyOpenGL from the downloaded wheel:
```cmd
pip install PyOpenGL-3.1.7-cp39-cp39-win_amd64
```

5. Clone the repository and navigate into it:
```cmd
git clone https://github.com/ddkhen11/Mesh2SMPL
cd Mesh2SMPL
```

6. Place a folder containing your .obj mesh file, .mtl file, and .jpg texture file into `dataset_example/mesh_data`. Ensure that your mesh file contains UV coordinates.

7. Run the main.py script:
```cmd
python main.py
```

8. Your results will be in `dataset_example/image_data`.