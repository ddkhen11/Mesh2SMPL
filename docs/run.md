# Mesh2SMPL Usage

To run Mesh2SMPL, follow the detailed step-by-step instructions below. You can use either PowerShell or the Anaconda Command Prompt to execute these instructions.

Video Instructions: [https://youtu.be/nS_rY6gBBZc](https://youtu.be/nS_rY6gBBZc)

### 1. Get Multiview Images

1. **Navigate into Mesh2SMPL directory**

    First, navigate into your Mesh2SMPL directory:
    ```cmd
    cd path\to\Mesh2SMPL
    ```

2. **Activate multiview conda environment for Python 3.9**

    Activate the Python 3.9 conda environment you created for getting the multiview images:
    ```cmd
    conda activate multiview
    ```

3. **Prepare your 3D mesh data**

    Place a folder containing your `.obj` mesh file and `.jpg` texture file into `dataset_example/mesh_data`. Ensure that your mesh file contains UV coordinates.

4. **Run the `get_multiview_images.py` script**

    Navigate back to the Mesh2SMPL directory and execute the `get_multiview_images.py` script to process your mesh data:
    ```cmd
    python get_multiview_images.py -n <your-mesh-folder-name> 
    ```

    Replace `<your-mesh-folder-name>` with what you named the folder containing your mesh file in the previous step.

    Your multiview images and camera data will be in `dataset_example/image_data/<your-mesh-folder-name>`.


### 2. Fit OpenPose to the Multiview Images

Due to the complexities of running OpenPose, we will instead use [AlphaPose](https://github.com/MVIG-SJTU/AlphaPose) on our multiview images and then convert the AlphaPose keypoints to OpenPose keypoints. The following set of instructions is a guide to running AlphaPose, so please refer to AlphaPose's GitHub repository if you need to troubleshoot anything.

1. **Activate AlphaPose conda environment for Python 3.7**

    If your previous conda environment is still active, make sure you deactivate it first:
    ```cmd
    conda deactivate
    ```
    Then, activate the Python 3.7 conda environment you created for running AlphaPose:
    ```cmd
    conda activate alphapose
    ```

2. **Run AlphaPose on the multiview images and convert to OpenPose**

    Run the following command to extract the AlphaPose 2D pose keypoints from each image and convert them to OpenPose keypoints:

    ```cmd
    python fit_openpose.py -n <your-mesh-folder-name> 
    ```
    
    Replace `<your-mesh-folder-name>` with what you named the folder containing your mesh file in step 3 of the previous set of these instructions.

    Your OpenPose keypoints will be in `dataset_example/image_data/<your-mesh-folder-name>/keypoints`. 



### 3. Render the SMPL Model

1. **Activate SMPL conda environment for Python 3.6**

    If your previous conda environment is still active, make sure you deactivate it first:
    ```cmd
    conda deactivate
    ```
    Then, activate the Python 3.6 conda environment you created for rendering the SMPL model:
    ```cmd
    conda activate fit-smpl
    ```

2. **Render the SMPL model from the multiview images and fitted 2D poses**

    Run the following command to render the SMPL model:
    ```cmd 
    python render_smpl.py -n <your-mesh-folder-name> -g <your-gender>
    ```
    Replace `<your-mesh-folder-name>` with what you named the folder containing your mesh file in step 3 of the first set of these instructions. Replace `<your-gender>` with the gender of the subject of your mesh scan (male, female, neutral).

3. **Access your results**

   After running the command, your results will be located in the `dataset_example/mesh_data/<your-mesh-folder-name>/smpl` directory. `smpl_mesh.obj` will contain your fitted SMPL model scaled back and aligned to the original size and position of your inputted mesh file. `smpl_param.pkl` will contains the parameters for your fitted SMPL model (not adjusted for scale).


## Full Mesh2SMPL Usage Command List In Order

```cmd
cd path\to\Mesh2SMPL
conda activate multiview
# Insert mesh folder
python get_multiview_images.py -n <your-mesh-folder-name> 

conda deactivate
conda activate alphapose
python fit_openpose.py -n <your-mesh-folder-name> 

conda deactivate
conda activate fit-smpl
python render_smpl.py -n <your-mesh-folder-name> -g <your-gender>
```
