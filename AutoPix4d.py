from remote_handling.retrieve_from_pad import transfer_images_from_remote
from NFLoc.EXIF_handling.get_gps_data import _get_coordinates_as_point
from NFLoc.geojson_handling.get_geojson_info import _make_dict_with_coordinates_list
from NFLoc.folder_handling.parse_files_in_folder import _get_all_images_given_folder
from automation_scripts.autopix import automate_pix4d, process_running_wmi
from time import strftime
import os
import sys
import logging
import shutil

# This is the script to automate stitching field images in Pix4dFields. It must
# be supplied the directory with all of the image sets as a command line
# argument.
# 
# It will name the projects in Pix4dFields after the locations found in the tif
# EXIF data alongside a count of how many images it found in that field.
#
# The projects will need to be visually observed for correctness.
#
# If the script terminates prematurely it is most likely because Pix4d threw a
# pop-up that prevented the auto-clicker from pressing the exit button.
#
# It will create a log with information about its execution and what it
# accomplished found in the logs folder.

# Gets all the image sets, excludes a folder named 'processed' which will store
# processed image sets so they are not reused
def get_sub_directory_paths(start_directory):
    return [os.path.join(start_directory, f) for f in os.listdir(start_directory) 
            if (os.path.isdir(os.path.join(start_directory, f)))]

def process_all_images_in_set(folder_path : str) -> dict:
    images = _get_all_images_given_folder(folder_path)
    coords = []

    for image in images:
        coords.append(_get_coordinates_as_point(image))

    return _make_dict_with_coordinates_list("Fields.geojson", coords)

def interleave_field_and_num_of_images(fields_dict : dict) -> list:
    res = []
    for field in fields_dict:
        res.append(field + "-" + str(fields_dict[field]) + "tifs")
    return res

def get_field_with_max_value(fields_dict : dict) -> str:
    return max(fields_dict, key=fields_dict.get)

if __name__ == '__main__':
    date = strftime("%Y-%m-%d")
    timestamp = strftime("%Y-%m-%dT%H%M%S")
    logging.basicConfig(filename=('logs\\' + timestamp + '.log'), level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info('Began process at ' + timestamp + '\n\n')

    if (len(sys.argv) != 2 and len(sys.argv) != 3):
        logger.error("Invalid arguments given")
        print("Usage: python AutoPix4d.py [path to image sets] [optional: 'scp']")
        exit(-1)

    if len(sys.argv) == 3:
        if transfer_images_from_remote(sys.argv[1]) == 1:
            logger.info('Successfully retrieved images from launchpad\n\n')
        else:
            logger.error('Did not retrieve images from launchpad')
            exit(-1)

    # start_directory = "F:\\20230906_CemeteryHPNorth"
    tif_sets = get_sub_directory_paths(sys.argv[1])
    processed_folder = os.path.join(sys.argv[1], "processed")

    for set in tif_sets:
        if set == processed_folder:
            continue

        img_dict = process_all_images_in_set(set)
        field_name = get_field_with_max_value(img_dict)
        logger.info('Retrieved EXIF data in ' + set + ' ... ' + field_name)

        logger.info("Opening Pix4d to create project...")
        automate_pix4d(set, field_name + "_" + date)

        # if process_running_wmi("Pix4dfields.exe"):
        #    logger.error(set + " in Pix4d did not close as expected.")
        #    break

        logger.info("Made project: " + field_name + "_" + date + '\n\n')

        try:
            time = strftime("%H%M")
            set = shutil.move(set, date + "_" + field_name + time)
            shutil.move(set, processed_folder, copy_function = shutil.copytree)
            log.info("Moved " + set + " to " + processed_folder + "\n\n")
        except:
            logger.error("Failed to move set to processed folder\n\n")

    logger.info("Script terminated at " + strftime("%Y-%m-%dT%H%M%S"))

