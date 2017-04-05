import os
import overwrite
import ctypes
import json
import shutil
import subprocess

path = os.environ['path']
local_app_data = os.environ['localappdata']
roaming_app_data = os.environ['appdata']
android_path = '\\Android\\android-sdk'
documnents_path = os.environ['userprofile'] + '\\' + 'Documents'
cwd = os.getcwd()

dirMap = {}
dirMap['LocalAppData'] = local_app_data
dirMap['RoamingAppData'] = roaming_app_data
dirMap['Documents'] = documnents_path

def update_path_with_android_sdk():
    if local_app_data+android_path not in path :
        if os.path.exists(local_app_data + android_path) :
            print('Updating Path with Android SDK.')
            os.system('setx PATH %PATH%;'  + local_app_data + android_path)
        else:
            print('No android SDK found at path.')
    else:
        print('android sdk already added.')


def copy_program_settings():
    for key,value in dirMap.items():
        # if os.path.exists(cwd + '\\' + key):
        print('Copying configs for : ' + key + ' to ' + value )
        for root, dirs, files in os.walk(cwd + '\\' + key):
            if root == (cwd + '\\' + key):
                for dir in dirs:
                    src = cwd + '\\' + key + '\\' + dir
                    dst = value + '\\' + dir
                    print("FOUND DIRECTORY TO COPY : " + dir)
                    print("COPYING DIRECTORY FROM " + src + " TO " + dst)
                    overwrite.recursive_overwrite(src, dst)

def run_installations():
    cmd = "where"
    if shutil.which('choco') is None:
        print("No chcoco found, checking system privileges.")
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        if not is_admin:
            print("Not admin, need more privileges.")
            os.system("pause")
            quit()
        else:
            os.system('@powershell -NoProfile -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString(' + "'https://chocolatey.org/install.ps1'" + '))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"')
            run_installations()
            return
    if os.path.exists(cwd + '\\packages.json'):
        with open('packages.json') as data_file:
            data = json.load(data_file)
            for package in data['packages']:
                os.system('@powershell choco install ' + package + ' -y')
    else:
        print('no packages specified')


run_installations()
update_path_with_android_sdk()
copy_program_settings()
print("All done. Have fun with your new install!")
os.system("Pause")
