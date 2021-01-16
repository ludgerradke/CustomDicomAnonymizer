from anonymize_dicom_folder import anonymize
from utils import platform_slash
import argparse
import os
from glob import glob


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


def main(in_folder, out_folder, config_file):
    folders = glob(in_folder + platform_slash() + '*')
    if not os.path.isdir(out_folder):
        os.mkdir(out_folder)
    for folder in folders:
        if os.path.isdir(folder):
            anonymize(in_folder=folder,
                      out_folder=out_folder,
                      config_file=config_file)


if __name__ == '__main__':
    args = get_args()
    main(in_folder=args.in_folder,
         out_folder=args.out_folder,
         config_file=args.config_file)
