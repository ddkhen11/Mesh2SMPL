# Mesh2SMPL

Mesh2SMPL is a project that utilizes the [MultiviewSMPLifyX](https://github.com/ZhengZerong/MultiviewSMPLifyX) and [PaMIR](https://github.com/ZhengZerong/PaMIR) projects to convert a textured mesh scan of a human into a SMPL model.

## Citation

If you use this code, please cite the following papers:

```bibtex
@ARTICLE{zheng2020pamir,
  author={Zheng, Zerong and Yu, Tao and Liu, Yebin and Dai, Qionghai},
  journal={IEEE Transactions on Pattern Analysis and Machine Intelligence}, 
  title={PaMIR: Parametric Model-Conditioned Implicit Representation for Image-based Human Reconstruction}, 
  year={2021},
  volume={},
  number={},
  pages={1-1},
  doi={10.1109/TPAMI.2021.3050505}}


@inproceedings{SMPL-X:2019,
  title = {Expressive Body Capture: 3D Hands, Face, and Body from a Single Image},
  author = {Pavlakos, Georgios and Choutas, Vasileios and Ghorbani, Nima and Bolkart, Timo and Osman, Ahmed A. A. and Tzionas, Dimitrios and Black, Michael J.},
  booktitle = {Proceedings IEEE Conf. on Computer Vision and Pattern Recognition (CVPR)},
  year = {2019}
}
```

## Instructions to Run the Program

### 1. Get Multiview Images

1. Create a conda environment for Python 3.9:
```cmd
conda create --name myenv python=3.9
conda activate myenv
```

2. Clone the repository and navigate into it:
```cmd
git clone --recurse-submodules https://github.com/ddkhen11/Mesh2SMPL
cd Mesh2SMPL
```

3. Install dependencies using pip:
```cmd
pip install --upgrade setuptools wheel build
pip install pyembree
pip install -r requirements.txt
```

4. Download the PyOpenGL wheel specific to Python 3.9 from [Google Drive](https://drive.google.com/drive/folders/1mz7faVsrp0e6IKCQh8MyZh-BcCqEGPwx) (filename: PyOpenGL-3.1.7-cp39-cp39-win_amd64.whl).

5. Install PyOpenGL from the downloaded wheel:
```cmd
pip install PyOpenGL-3.1.7-cp39-cp39-win_amd64
```

6. Place a folder containing your .obj mesh file, .mtl file, and .jpg texture file into `dataset_example/mesh_data`. Ensure that your mesh file contains UV coordinates.

7. Run the get_multiview_images.py script:
```cmd
python get_multiview_images.py
```

8. Your results will be in `dataset_example/image_data`.