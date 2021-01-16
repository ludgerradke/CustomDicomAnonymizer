from utils import load_dicoms, load_config, platform_slash, anonymize_element, print_colored_text
import argparse
import os
from copy import deepcopy
import numpy as np


def anonymize(in_folder, out_folder, config_file):

    DICOMs = load_dicoms(in_folder)

    if len(DICOMs) == 0:
        return

    config = load_config(config_file)

    if os.path.isdir(out_folder + platform_slash() + os.path.basename(in_folder)):
        message = "Folder {} exist, please delete first.".format(
            out_folder + platform_slash() + os.path.basename(in_folder))
        print_colored_text(message)
        return
    else:
        os.mkdir(out_folder + platform_slash() + os.path.basename(in_folder))

    for ds, file in DICOMs:
        ds_anonym = deepcopy(ds)
        ds_anonym.clear()
        pixel_array = ds.pixel_array
        if pixel_array.dtype != np.uint16:
            pixel_array = pixel_array.astype(np.uint16)
        ds.PixelData = pixel_array.tostring()
        for key, bool in config:
            if key == 'InstitutionName':
                b = 2
            try:
                element = ds.pop(key.replace(' ', '').replace("'s", ""))
                if bool == 'True':
                    try:
                        element = anonymize_element(element)
                    except:
                        print("The parameter {} could not be anonymized and was deleted from the DICOM file: {}. "
                              "If you don't want to remove the parameter, change it to False in the config file "
                              "and repeat the anonymization.".format(key, file))
                        continue
                ds_anonym.add(element)
            except KeyError:
                pass
        for element in ds:
            ds_anonym.add(element)
        ds_anonym.save_as(out_folder + platform_slash() + os.path.basename(in_folder) + platform_slash() + file)


def get_args() -> argparse:
    parser = argparse.ArgumentParser(description='Anonymize folder of DICOMs.')
    parser.add_argument(
        '-i',
        '--in_folder',
        type=str,
        help='str: Folder which contains DICOM files')
    parser.add_argument(
        '-o',
        '--out_folder',
        type=str,
        default='.',
        help='str: Folder in which anonymized dicoms are saved. '
             'The folder has the same basename as the basename of the input file.')
    parser.add_argument(
        '-c',
        '--config_file',
        type=str,
        default='./default.csv',
        help='str: Folder in which the configured file should be saved [default = .]')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    anonymize(in_folder=args.in_folder,
              out_folder=args.out_folder,
              config_file=args.config_file)
