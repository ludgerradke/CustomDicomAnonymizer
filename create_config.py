from utils import platform_slash, get_example_dicom, save_config
import argparse


# Only change variables, do NOT delete them!
Default_False = ['FlipAngle', 'Modality', 'MRAcquisitionType', 'SliceThickness', 'RepetitionTime', 'EchoTime',
                 'NumberOfAverages', 'ImagingFrequency', 'InstanceNumber', 'AcquisitionNumber', 'InversionTime',
                 'Rows', 'Columns', 'RequestAttributesSequence', 'ReferencedImageSequence']

Default_True = ['PatientBirthDate', 'InstitutionName', 'InstitutionAddress', 'ReferringPhysicianName',
                'InstitutionalDepartmentName', 'PatientName', 'PatientID', 'PatientSex', 'PatientAge',
                'PatientWeight', 'TransmitCoilName', 'Private Creator', 'SeriesNumber']


def remove_important_elements(config_dict: dict) -> dict:
    """
    Important elements are removed from the config file
    so that you can't mistakenly set them to false.

    Note: Some can still be sorted out, this will be done in the following versions.
    """
    for key in ['BitsAllocated', 'BitsStored', 'HighBit ', 'SmallestImagePixelValue', 'LargestImagePixelValue',
                'PixelData', 'ImagedNucleus', 'PixelSpacing', 'AcquisitionMatrix', 'dBdt', 'WindowWidth',
                'WindowCenterWidthExplanation', 'WindowCenter', 'VariableFlipAngleFlag',
                'SliceLocation', 'SequenceVariant', 'SamplesPerPixel', 'PixelRepresentation', 'SeriesNumber',
                'PixelBandwidth', 'PercentPhaseFieldOfView', 'NumberOfPhaseEncodingSteps', 'ImagePositionPatient',
                'ImageOrientationPatient']:
        try:
            config_dict.pop(key)
        except KeyError:
            pass
    return config_dict


def set_some_elements_to(config_dict: dict, keys: list, boolean: bool) -> dict:
    """
    Function which uses the global parameters Default_False and Default_True to adjust
    the config file by custom parameters.

    IMPORTANT: Parameters should only be modified but not deleted.
    """
    for key in keys:
        try:
            config_dict[key] = boolean
        except KeyError:
            pass
    return config_dict


def create_config(d_input: str, default_bool: bool = False, path: str = r'./', name: str = 'default.csv'):
    """
    Creates a config file to specify which parameters of the Dicom file should be anonymized.

    :param d_input: Example DICOM file or a folder in which DICOM files are located*.
    :param default_bool:Boolean defines if the parameters should be anoymized by default (bool = True) or '
             'if they should be taken over (bool = False).
    :param path: Folder in which the configured file should be saved
    :param name: Filename of configured file
    ---------------------------------------------------------------------------------------------
    hit: * first DICOM file which is found is used as a template
    """

    config_file = path + platform_slash() + name
    d_example = get_example_dicom(d_input)
    config_dict = []
    for element in d_example:
        # Check pydicom for the different class shortcuts
        if element.VR in ['AS', 'DA', 'DT', 'LO', 'LT', 'PN', 'ST', 'SH', 'TM', 'UN', 'UT']:
            config_dict.append((element.description(), default_bool))
    config_dict = dict(config_dict)

    config_dict = remove_important_elements(config_dict)
    config_dict = set_some_elements_to(config_dict, Default_True, True)
    config_dict = set_some_elements_to(config_dict, Default_False, False)
    save_config(config_file, config_dict)


def get_args() -> argparse:
    parser = argparse.ArgumentParser(description='Creates a config file to specify which parameters of the Dicom file '
                                                 'should be anonymized.')
    parser.add_argument(
        '-i',
        '--d_input',
        type=str,
        help='str: Example DICOM file or a folder in which DICOM files are located')
    parser.add_argument(
        '-b',
        '--default_bool',
        type=bool,
        default=True,
        help='bool: Boolean defines if the parameters should be anoymized by default (bool = True) or '
             'if they should be taken over (bool = False). [default = True]')
    parser.add_argument(
        '-p',
        '--path',
        type=str,
        default='.',
        help='str: Folder in which the configured file should be saved [default = .]')
    parser.add_argument(
        '-n',
        '--name',
        type=str,
        default=r'./default.csv',
        help='str: Filename of configured file [default = default.csv]')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    create_config(d_input=args.d_input,
                  default_bool=args.default_bool,
                  path=args.path,
                  name=args.name)
