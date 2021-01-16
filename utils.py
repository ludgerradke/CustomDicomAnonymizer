import os
import platform
from termcolor import colored
from glob import glob
import pydicom
from pydicom.dataelem import RawDataElement
from pydicom.valuerep import PersonName
import hashlib


def print_colored_text(message, color='red'):
    print(colored(message, color))


def platform_slash():
    if "Windows" in platform.platform():
        slash = '\\'
    elif "Linux" in platform.platform():
        slash = r'/'
    elif "Darwin" in platform.platform():
        slash = r'/'
    else:
        message = "Unknown platform: {}".format(platform.platform())
        print_colored_text(message)
        raise SystemError
    return slash


def get_example_dicom(file_or_folder):
    if os.path.isfile(file_or_folder):
        try:
            return pydicom.dcmread(file_or_folder)
        except:
            message = '{} is not a Dicom file!'.format(file_or_folder)
            print_colored_text(message,)
    elif os.path.isdir(file_or_folder):
        files = glob(file_or_folder + '/*')
        for file in files:
            try:
                return pydicom.dcmread(file)
            except:
                continue
        message = "The folder {} does not contain a DICOM file".format(file_or_folder)
        print_colored_text(message)
    else:
        message = "{} is not a file or a folder".format(file_or_folder)
        print_colored_text(message)
    raise UserWarning


def save_config(config_file, config_dict):
    with open(config_file, 'w') as f:
        for key in config_dict.keys():
            f.write('%s;%s\n' % (key, config_dict[key]))
    message = "Config file: {} saved".format(config_file)
    print_colored_text(message, 'green')


def load_config(config_file):
    if not os.path.isfile(config_file):
        message = "{} not a config file".format(config_file)
        print_colored_text(message)
        raise OSError

    with open(config_file, 'r') as f:
        config = [c[:-1].split(';') for c in f.readlines()]

    message = "Config file: {} loaded".format(config_file)
    print_colored_text(message, 'green')
    return config


def load_dicoms(folder):
    data_list = glob(folder + platform_slash() + '*')
    dicoms = []

    for file in data_list:
        try:
            dicoms.append((pydicom.dcmread(file), os.path.basename(file)))
        except:
            message = '{} is not a DICOM file so it was ignored'.format(file)
            print_colored_text(message, 'blue')

    if len(dicoms) == 0:
        message = "The folder {} does not contain a DICOM file".format(folder)
        print_colored_text(message)
        return []

    return dicoms


def anonymize_element(element):
    type_ = element.value
    if type_.__class__ is bytes:
        value = element.value

        value = (str(int(hashlib.sha1(value).hexdigest(), 16) % (10 ** element.length))).encode("utf-8")

        element = RawDataElement(element.tag, element.VR, element.length, value, element.value_tell,
                                     element.is_implicit_VR, element.is_little_endian, element.is_raw)
    elif type_.__class__ is int:
        pass
    elif type_.__class__ is str:
        if element.description() in ['Institution Name', 'Patient Birth Date']:
            element.value = 'Anonymize'
    elif type_.__class__ is PersonName:
        element.value = 'Anonymize'
    else:
        pass
    return element
