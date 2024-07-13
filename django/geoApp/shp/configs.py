import os


from geoApp.exceptions import UncoherentConfigurationsError
from geoApp.utils import generate_current_timestamp

# function define
#--------------------------------------------------------

def generate_uploaded_shp_file_relpath(uploaded_shp_files_folder_relpath_from_media_root):

    """
    this function generates the relative path to be passed to "Upload_to" argument of filefield.

    basically, this function takes the parameter 'uploaded_shp_files_folder_relpath_from_media_root'
    and join its path before a new folder/series of folders which have some ties with
    the uploaded file or the uploaded time of upload.

    uploaded_shp_files_folder_relpath_from_media_root:
    the input of this function must be the piece of path 
    between the MEDIA_ROOT folder and the filename, extremes excluded.
    """

    # name = instance.name.replace(" ", "_").replace("-", "_").lower()
    timestamp = generate_current_timestamp()

    

    # name of the folder which will contain the uploaded file
    # current_file_subfolder = name +  "_" + timestamp
    current_file_subfolder = timestamp

    # relative path of the folder which will contain the uploaded file
    uploaded_shp_file_relpath = os.path.join(
        uploaded_shp_files_folder_relpath_from_media_root,  
        current_file_subfolder
        )

    # print("generated new uploaded_shp_file_relpath: {}".format(uploaded_shp_file_relpath) )

    print(UPLOADED_SHP_FILES_FOLDER_DIR, timestamp,uploaded_shp_file_relpath)

    # it is a relative path from media folder to the folder immediately before the file
    return uploaded_shp_file_relpath


# variables define
#--------------------------------------------

# useless for now
# SHP_FILES_FOLDER_DEFAULT_RELPATH_FROM_MEDIA_ROOT = 'shp/shp_default'

# SHP_FILES_FOLDER_DEFAULT_ABSPATH = os.path.join(
#     MEDIA_ROOT, SHP_FILES_FOLDER_DEFAULT_RELPATH_FROM_MEDIA_ROOT)

UPLOADED_SHP_FILES_FOLDER_DIR = 'shp'

UPLOADED_SHP_FILES_MUST_BE_ZIPPED = True
# if this is true, then also DETECT_AND_UNZIP_LOADED_ZIPFILE_IN_SHP must be true

DETECT_AND_UNZIP_LOADED_ZIPFILE_IN_SHP = True


# variables validation
#-----------------------

if UPLOADED_SHP_FILES_MUST_BE_ZIPPED == True:
    if DETECT_AND_UNZIP_LOADED_ZIPFILE_IN_SHP != True:
        raise UncoherentConfigurationsError(
            "UPLOADED_SHP_FILES_MUST_BE_ZIPPED is True\nSo DETECT_AND_UNZIP_LOADED_ZIPFILE_IN_SHP must also be True")