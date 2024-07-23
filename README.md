# Mesh2SMPL

Mesh2SMPL is a project that utilizes the [MultiviewSMPLifyX](https://github.com/ZhengZerong/MultiviewSMPLifyX) and [PaMIR](https://github.com/ZhengZerong/PaMIR) projects to convert a textured mesh scan of a human into a SMPL model.

## Installation

If it is your first time running Mesh2SMPL, please follow the instructions in [docs/installation.md](docs/installation.md) in order to setup everything necessary to run this program.

## Usage

After you have completed all the necessary setup for Mesh2SMPL, follow the instructions in [docs/run.md](docs/run.md) to run this program. 


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


@ARTICLE{SMPL:2015,
    author = {Loper, Matthew and Mahmood, Naureen and Romero, Javier and Pons-Moll, Gerard and Black, Michael J.},
    journal = {ACM Transactions on Graphics, (Proc. SIGGRAPH Asia)},
    title = {{SMPL}: A Skinned Multi-Person Linear Model}, 
    year = {2015},
    month = oct,
    volume = {34},
    number = {6},
    pages = {248:1--248:16},
    publisher = {ACM}}


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