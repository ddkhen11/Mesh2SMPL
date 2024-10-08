import argparse
import os
import os.path as osp
import glob

import pickle

import numpy as np


def clean_fn(fn, output_folder='output'):
    with open(fn, 'rb') as body_file:
        body_data = pickle.load(body_file, encoding='latin1')

    output_dict = {}
    for key, data in body_data.items():
        if 'chumpy' in str(type(data)):
            output_dict[key] = np.array(data)
        else:
            output_dict[key] = data

    if osp.split(fn)[1] == "basicModel_neutral_lbs_10_207_0_v1.0.0.pkl":
        out_fn = "SMPL_NEUTRAL.pkl"
    elif osp.split(fn)[1] == "basicmodel_m_lbs_10_207_0_v1.0.0.pkl":
        out_fn = "SMPL_MALE.pkl"
    elif osp.split(fn)[1] == "basicModel_f_lbs_10_207_0_v1.0.0.pkl":
        out_fn = "SMPL_FEMALE.pkl"
    else:
        raise ValueError('Unknown model: {}'.format(fn))

    out_path = osp.join(output_folder, out_fn)
    with open(out_path, 'wb') as out_file:
        pickle.dump(output_dict, out_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-models', dest='input_models', nargs='+',
                        required=True, type=str,
                        help='The path to the models that will be processed')
    parser.add_argument('--output-folder', dest='output_folder',
                        required=True, type=str,
                        help='The path to the output folder')

    args = parser.parse_args()

    input_models = []
    for pattern in args.input_models:
        input_models.extend(glob.glob(pattern))
        
    output_folder = args.output_folder
    if not osp.exists(output_folder):
        print('Creating directory: {}'.format(output_folder))
        os.makedirs(output_folder)

    for input_model in input_models:
        clean_fn(input_model, output_folder=output_folder)