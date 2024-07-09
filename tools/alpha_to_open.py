import argparse
import json
import os

import numpy as np

openpose_to_alpha_mapping = {
    0: 0,    # Nose
    1: 18,   # Neck
    2: 6,    # RShoulder
    3: 8,    # RElbow
    4: 10,   # RWrist
    5: 5,    # LShoulder
    6: 7,    # LElbow
    7: 9,    # LWrist
    8: 19,   # MidHip
    9: 12,   # RHip
    10: 14,  # RKnee
    11: 16,  # RAnkle
    12: 11,  # LHip
    13: 13,  # LKnee
    14: 15,  # LAnkle
    15: 2,   # REye
    16: 1,   # LEye
    17: 4,   # REar
    18: 3,   # LEar
    19: 20,  # LBigToe
    20: 22,  # LSmallToe
    21: 24,  # LHeel
    22: 21,  # RBigToe
    23: 23,  # RSmallToe
    24: 25   # RHeel
}

def convert_alpha_to_openpose(alpha_entry):
    """
    Convert body keypoints
    """
    keypoints = alpha_entry["keypoints"]
    openpose_keypoints_2d = []

    for openpose_idx, alpha_idx in openpose_to_alpha_mapping.items():
        alpha_offset = alpha_idx * 3
        openpose_keypoints_2d.extend(keypoints[alpha_offset:alpha_offset + 3])


    """
    Convert face keypoints
    """
    face_keypoints_2d = []

    for alpha_idx in range(68):
        alpha_offset = (alpha_idx + 26) * 3
        face_keypoints_2d.extend(keypoints[alpha_offset:alpha_offset + 3])

    # Find centroid of right eye border to estimate right eye keypoint
    right_eye_border_list = []

    for alpha_idx in range(6):
        alpha_offset = (alpha_idx + 26 + 36) * 3
        keypoint = keypoints[alpha_offset:alpha_offset + 3]
        right_eye_border_list.append(keypoint)

    right_eye_border = np.array(right_eye_border_list)
    right_eye =  np.mean(right_eye_border, axis=0)
    face_keypoints_2d.extend(right_eye.tolist())

    # Find centroid of left eye border to estimate left eye keypoint
    left_eye_border_list = []

    for alpha_idx in range(6):
        alpha_offset = (alpha_idx + 26 + 42) * 3
        keypoint = keypoints[alpha_offset:alpha_offset + 3]
        left_eye_border_list.append(keypoint)

    left_eye_border = np.array(left_eye_border_list)
    left_eye =  np.mean(left_eye_border, axis=0)
    face_keypoints_2d.extend(left_eye.tolist())


    '''
    Convert hand keypoints
    '''
    hand_left_keypoints_2d = []
    hand_right_keypoints_2d = []

    # Left hand
    for alpha_idx in range(21):
        alpha_offset = (alpha_idx + 94) * 3
        hand_left_keypoints_2d.extend(keypoints[alpha_offset:alpha_offset + 3])

    # Right hand
    for alpha_idx in range(21):
        alpha_offset = (alpha_idx + 115) * 3
        hand_right_keypoints_2d.extend(keypoints[alpha_offset:alpha_offset + 3])

    openpose_data = {
        "version": 1.1,
        "people": [
            {
                "pose_keypoints_2d": openpose_keypoints_2d,
                "face_keypoints_2d": face_keypoints_2d,
                "hand_left_keypoints_2d": hand_left_keypoints_2d,
                "hand_right_keypoints_2d": hand_right_keypoints_2d,
                "pose_keypoints_3d": [],
                "face_keypoints_3d": [],
                "hand_left_keypoints_3d": [],
                "hand_right_keypoints_3d": []
            }
        ]
    }

    return openpose_data

def main():
    parser = argparse.ArgumentParser(description='Convert AlphaPose JSON to OpenPose JSON')
    parser.add_argument('--alphapose-json', type=str, required=True, help='Path to AlphaPose JSON file')
    args = parser.parse_args()

    alphapose_json_path = args.alphapose_json

    if not os.path.exists(alphapose_json_path):
        print(f"Error: The file '{alphapose_json_path}' does not exist.")
        return

    # Load AlphaPose JSON
    with open(alphapose_json_path, 'r') as f:
        alpha_data = json.load(f)

    # Create a directory for OpenPose JSONs if it doesn't exist
    output_dir = os.path.join(os.path.dirname(alphapose_json_path), 'keypoints')
    os.makedirs(output_dir, exist_ok=True)

    # Process each person's AlphaPose entry and save as OpenPose JSON
    for idx, person_entry in enumerate(alpha_data):
        openpose_data = convert_alpha_to_openpose(person_entry)
        idx = person_entry["image_id"].rstrip(".jpg")
        output_filename = os.path.join(output_dir, f'{idx}_keypoints.json')
        with open(output_filename, 'w') as outfile:
            json.dump(openpose_data, outfile, indent=4)

    print(f"Conversion completed. OpenPose JSON files saved in {output_dir}")

if __name__ == '__main__':
    main()