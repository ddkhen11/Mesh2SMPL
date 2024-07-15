import os
import sys

# Adding the 'third_party/PaMIR/data' directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), 'third_party/PaMIR/data'))

from third_party.PaMIR.data.main_normalize_mesh import main as main_normalize_mesh
from third_party.PaMIR.data.main_calc_prt import main as main_calc_prt
from third_party.PaMIR.data.main_render_images import main as main_render_images
from third_party.PaMIR.data.main_sample_occ import main as main_sample_occ

def get_multiview_images():
    """
    Performs sequential tasks to generate multiview images:
    1. Normalizes mesh data
    2. Calculates PRT (Parameterized Reflectance Transfer)
    3. Renders images
    4. Samples occupancy
    """
    print("Normalizing mesh.")
    main_normalize_mesh()

    print("Calculating PRT.")
    main_calc_prt()

    print("Rendering images.")
    main_render_images()

    # print("Sampling occupancy.")
    # main_sample_occ()

if __name__ == "__main__":
    get_multiview_images()