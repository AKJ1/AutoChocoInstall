import os
import shutil

path = os.environ['path']
local_app_data = os.environ['localappdata']
roaming_app_data = os.environ['appdata']
android_path = '\\Android\\android-sdk'

dirMap = {}
dirMap['LocalAppData'] = local_app_data
dirMap['RoamingAppData'] = roaming_app_data

def update_path_with_android_sdk():
    if local_app_data+android_path not in path :
        if os.path.exists(local_app_data + android_path) :
            print('Updating Path with Android SDK.')
            os.system('setx PATH %PATH%;'  + local_app_data + android_path)
        else:
            print('No android SDK found at path.')
    else:
        print('android sdk already added.')



cwd = os.getcwd()

def copy_program_settings():
    cwd = os.getcwd()
    for key,value in dirMap.items():
        # if os.path.exists(cwd + '\\' + key):
        for root, dirs, files in os.walk(cwd + '\\' + key):
            if root == (cwd + '\\' + key):
                for dir in dirs:
                    src = cwd + '\\' + key + '\\' + dir
                    dst = value + '\\' + dir
                    print("FOUND DIRECTORY TO COPY : " + dir)
                    print("COPYING DIRECTORY FROM " + src + " TO " + dst)
                    recursive_overwrite(src, dst)

        print("k:" +key)
        print("v:" + value)

def recursive_overwrite(src, dest, ignore=None):
    if os.path.isdir(src):
        if not os.path.isdir(dest):
            os.makedirs(dest)
        files = os.listdir(src)
        if ignore is not None:
            ignored = ignore(src, files)
        else:
            ignored = set()
        for f in files:
            if f not in ignored:
                recursive_overwrite(os.path.join(src, f),
                                    os.path.join(dest, f),
                                    ignore)
    else:
        shutil.copyfile(src, dest)

copy_program_settings()
update_path_with_android_sdk()