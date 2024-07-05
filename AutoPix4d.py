from NFLoc.EXIF_handling.get_gps_data import _get_coordinates_as_point
from NFLoc.geojson_handling.get_geojson_info import _make_dict_with_coordinates_list
from NFLoc.folder_handling.parse_files_in_folder import _get_all_images_given_folder
from automation_scripts.autopix import automate_pix4d, process_running_wmi
import os

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
# accomplished.

# Gets all the image sets
def get_sub_directory_paths(start_directory):
    return [os.path.join(start_directory, f) for f in os.listdir(start_directory) 
            if os.path.isdir(os.path.join(start_directory, f))]

def process_all_images_in_set(folder_path : str) -> dict:
    images = _get_all_images_given_folder(folder_path)
    coords = []

    for image in images:
        coords.append(_get_coordinates_as_point(image))

    return _make_dict_with_coordinates_list("AutoPix4d\\Fields.geojson", coords)

def interleave_field_and_num_of_images(fields_dict : dict) -> list:
    res = []
    for field in fields_dict:
        res.append(field + "-" + str(fields_dict[field]) + "tifs")
    return res


start_directory = "C:\\Users\\andre\\Desktop\\Project_Test\\ideal_img_set_folder"
tif_sets = get_sub_directory_paths(start_directory)
res = []

for set in tif_sets:
    print("Processing images in " + set + "...")
    img_dict = process_all_images_in_set(set)
    field_name = str(interleave_field_and_num_of_images(img_dict))
    print("Done for " + field_name)

    print("Opening Pix4d to process " + set + "...")
    automate_pix4d(set, field_name)

    if process_running_wmi("Pix4dfields.exe"):
        print("Pix4d did not close properly... terminating script")
        break

    res.append(field_name)
    print("Completed " + set + "!")

for field in res:
    print("Made: " + field)

