import os

directory = os.path.join("stanford-ct-new")

dir_list = os.listdir(directory)
dir_list.sort()
for filename in dir_list:
    file_ending = filename.split(".")[-1]
    if file_ending.isdigit():
        new_filename = file_ending.zfill(2)
        os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename + ".tif"))
