import pyautogui
import subprocess
import time
import wmi

"Pix4dfields.exe"
def process_running_wmi(process_name):
    c = wmi.WMI()
    for process in c.Win32_Process():
        if process.Name.lower() == process_name.lower():
            return True
    return False

def automate_pix4d(img_set_folder : str, field_name : str):
    subprocess.Popen("C:\\Program Files\\Pix4Dfields\\bin\\Pix4Dfields.exe")

    # clicks '+' button
    time.sleep(5.0)
    pyautogui.click(1876, 986)

    # clicks 'Edit Name' button, this position may change if 'unnamed projects'
    # gets to triple digits
    time.sleep(2.5)
    pyautogui.click(309, 49)

    # clicks 'Name' text field
    time.sleep(2.5)
    pyautogui.click(916, 476)

    # populates 'Name' field with 'stuff'
    time.sleep(2.5)
    with pyautogui.hold('ctrl'):
            pyautogui.press(['a'])
    pyautogui.press('backspace')
    pyautogui.typewrite(field_name)

    # clicks 'Save', saves the name
    time.sleep(2.5)
    pyautogui.click(1093, 619)

    # clicks 'Folder' button
    time.sleep(2.5)
    pyautogui.click(153, 507)

    # populates 'Folder' text box
    time.sleep(2.5)
    # folder = "F:\\AutomationTestFolder"
    pyautogui.typewrite(img_set_folder)

    # clicks 'Select Folder', time will vary. ~3 mins safe for the largest folders
    time.sleep(2.5)
    pyautogui.click(1146, 806)
    time.sleep(1.0)
    pyautogui.click(1091, 616) # safety click for img type selection pop up,
                               # tif files are auto selected.

    # *** CHANGE in real case scenario, ~3.0 * 60 for example ***      
    time.sleep(1.0 * 60)

    # clicks 'Apply'
    time.sleep(2.5)
    pyautogui.click(1190, 778)
    # safety click, in case dumb 'pansharpening' thing comes up
    time.sleep(1.0) 
    pyautogui.click(1190, 811)

    # clicks 'Start Processing', time will vary. ~30 mins safe for the largest
    # folders
    time.sleep(2.5)
    pyautogui.click(140, 1006)
    time.sleep(1.0)
    pyautogui.click(1238, 688) # safety click for 'bands' issue

    # *** CHANGE in real case scenario, ~30.0 * 60 for example ***
    time.sleep(3.0) # CHANGE to 30.0 * 60 in real case scenario

    # clicks exit button
    # pyautogui.click(1891, 10)
    # time.sleep(3.0)

    # pyautogui.click(1083, 566) # safety click for 'Yes' to exit out if prompted
    # time.sleep(2.0)

    # alternative way of exiting
    subprocess.call("TASKKILL /F /IM Pix4dFields.exe")
    time.sleep(3.0)
