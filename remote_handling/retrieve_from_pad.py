import subprocess

remote_user = "root"
remote_host = "192.168.1.49"
remote_path = "/mnt/data/images/*"
# local_directory = "C:\\Users\\andre\\Desktop\\Project_Test\\scp-test-playground"

# remote commands
rmv = "rm -rf /mnt/data/images/*"

# returns 1 on success and -1 on failure
def transfer_images_from_remote(dir: str) -> int:
    scp_command = f"scp -r {remote_user}@{remote_host}:{remote_path} {dir}"

    try:
        subprocess.run(scp_command, shell=True, check=True)
        subprocess.Popen(f"ssh {remote_user}@{remote_host} {rmv}", shell=True,
                 stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

        return 1
    except subprocess.CalledProcessError:
        return -1