from remote_handling.retrieve_from_pad import transfer_images_from_remote, transfer_images_to_local, move_images_locally
from NFLoc.EXIF_handling.get_gps_data import _get_coordinates_as_point
from NFLoc.geojson_handling.get_geojson_info import _make_dict_with_coordinates_list, get_field_from_images
from NFLoc.folder_handling.parse_files_in_folder import _get_all_images_given_folder
from automation_scripts.autopix import automate_pix4d
from time import strftime
import os
import sys
import logging
import shutil

# retrieves fieldname, calls pix4d, names img folder to be date + field + time
def do_process(img_folder : str):
    date = strftime("%Y-%m-%d")
    time = strftime("%H%M")
    field_name = get_field_from_images(img_folder) + "_" + date
    path_head, path_tail = os.path.split(img_folder)

    automate_pix4d(img_folder, field_name)
    shutil.move(img_folder, os.path.join(path_head, field_name + "T" + time))

if __name__ == '__main__':

    if len(sys.argv) < 3:
        print("Invalid amount of arguments.")
        print("Usage_1: python AutoPix4dv2.py 'remote' [working_dir] [optional: remote_dir]")
        print("Usage_2: python AutoPix4dv2.py 'local' [working_dir] [sd_dir_1] ... [sd_dir_n]")
        exit(-1)

    routine = sys.argv[1]
    working_directory = sys.argv[2]

    if routine == 'remote':
        new_field_folder = os.path.join(working_directory, strftime("%Y-%m-%dT%H%M%S"))

        try:
            transfer_images_to_local(new_field_folder)
        except:
            print("Failed to retrieve files remotely")
            exit(-1)

        do_process(new_field_folder)

    elif routine == 'local':
        # local routine
        img_folders = sys.argv[3:]

        for img_folder in img_folders:
            new_field_folder = os.path.join(working_directory, strftime("%Y-%m-%dT%H%M%S"))

            try:
               move_images_locally(new_field_folder, img_folder)
            except:
               print("Failed to retrieve files locally")
               exit(-1)

            do_process(new_field_folder)

    else:
        print("Invalid argv[1] argument. Misspelled 'remote' or 'local'?")
        exit(-1)
