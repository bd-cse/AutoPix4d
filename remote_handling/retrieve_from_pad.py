import os
import subprocess

remote_user = "root"
remote_host = "192.168.1.49"
remote_path = "/mnt/data/images/*"
# local_directory = "C:\\Users\\andre\\Desktop\\Project_Test\\scp-test-playground"

# remote commands
rmv = "rm -rf /mnt/data/images/*"

# returns 1 on success and -1 on failure
def transfer_images_from_remote(dir:  str) -> int:
    scp_command = f"scp -r {remote_user}@{remote_host}:{remote_path} {dir}"

    try:
        subprocess.run(scp_command, shell=True, check=True)
        subprocess.Popen(f"ssh {remote_user}@{remote_host} {rmv}", shell=True,
                 stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

        return 1
    except subprocess.CalledProcessError:
        return -1
    
def transfer_images_to_local(working_dir : str):
    scp_command = f"scp -r {remote_user}@{remote_host}:{remote_path} {dir}"

    subprocess.run(scp_command, shell=True, check=True)
    subprocess.Popen(f"ssh {remote_user}@{remote_host} {rmv}", shell=True,
                 stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    
def move_images_locally(working_dir : str, sd_dir : str):
    #sd_dir = os.path.join(sd_dir, '*')
    cp_command = f"xcopy {sd_dir} {working_dir} /E /H /i" # /i should tell it that it is a directory but if something weird happens it might be this
    subprocess.run(cp_command, shell=True, check=True)

def move_images_locally2(working_dir : str, sd_dir : str):
    sd_dir = os.path.join(sd_dir, "*")
    cmd = ['copy -r', sd_dir, working_dir]
    subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def clean_sd_card(sd_dir : str):
    rm_command = f"del /Q {sd_dir}"
    subprocess.run(rm_command, shell=True, check=True)
