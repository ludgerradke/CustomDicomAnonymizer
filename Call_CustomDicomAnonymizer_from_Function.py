from glob import glob
from utils import platform_slash
from anonymize_dicom_folders import main
import os


"""
Warning: This code is for illustrative purposes only and must be modified.
"""

if __name__ == '__main__':
    patients = glob('./FOLDER WITH PATIENTS')
    target_folder = './TARGET_FOLDER'
    config_file = './default.csv'

    if not os.path.isdir(target_folder):
        os.mkdir(target_folder)

    for patient in patients:
        if not os.path.isdir(patient):
            os.mkdir(target_folder)
        RepeatedMeasurements = glob(patient + platform_slash() + '*')
        for Measurement in RepeatedMeasurements:
            main(in_folder=Measurement,
                 out_folder=target_folder + platform_slash() + os.path.basename(patient),
                 config_file=config_file)