import os
import sys

path = "/Volumes/SSD/collection/65"
files = os.listdir(path)

start = 31
target_folder = 63

for index, file in enumerate(files):
    old_path = os.path.join(path, file)
    if file[0] == '.':
        pass
    else:
        segment = int(file.split('_')[1])
        frame = file.split('_')[2].split('.')[0]
        new_name = f"{target_folder}_{start+segment}_{frame}.npy"
        
        new_path = os.path.join(path, new_name)

        os.rename(old_path, new_path)


print(files)