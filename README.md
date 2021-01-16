# CustomDicomAnonymizer
This is a Python tool to anonymize Dicom records on a customized basis.

The tool supports the operating systems Windows, Linux and MacOs.

_Note: Only tested on Windows and Linux, please contact me if you have problems with MacOs._

By [ludgerradke](https://github.com/ludgerradke)

## Important

Currently, the script only anonymises the dicom header, the folders and files have the same names as before. Make sure that they do not contain any private information.

## Installation

1. Clone this repository.
```Shell
git clone https://github.com/ludgerradke/CustomDicomAnonymizer
```
2. In the following, the cloned directory is called `$CustomDicomAnonymizer`.
```Shell
cd CustomDicomAnonymizer
```
3. install requirements.txt
```Shell
pip install -r /path/to/requirements.txt
```

_Note: Codes are based on Python 3+._

## Usage

### Create Config File
First, a Dicom file is read in as an example and an individual csv configuration file created.  You can modify this file with any editor.

```Shell
$CustomDicomAnonymizer create_config.py FOLDER_WITH_DICOMs
```
_Note: You can use create_config.py -h to display help for accurate input._


The created file will look like this:

```
Instance Creation Date;	True
Instance Creation Time;	True
SOP Class UID;	True
SOP Instance UID;	True
Study Date;	True
...
```

or in excel:
```
          A             |   B
----------------------- | ------
Instance Creation Date  | True
Instance Creation Time  | True
SOP Class UID           | True
SOP Instance UID        | True
Study Date              | True
...
```
_Note: True means that this parameter should be anonymized and False means that this parameter should be present as orginal._

### Anonymize Dicom

With this tool, a single folder can be anonymized.

```Shell
$CustomDicomAnonymizer anonymize_dicom_folder.py FOLDER_WITH_DICOMs, Output_Folder, Config_File
```

Or all folders in a folder can be anonymized directly:

```Shell
$CustomDicomAnonymizer anonymize_dicom_folders.py FOLDER_WITH_DICOM_Folders, Output_Folder, Config_File
```

### Call CustomDicomAnonymizer from Python Skript

The Python Skirpt `Call_CustomDicomAnonymizer_from_Function.py` shows an example of how this tool can be used to anonymise complex projects.

## Contributing
If you have any comments, errors or problems with the use, please feel free to contact me.

## License
[MIT](https://choosealicense.com/licenses/mit/)
