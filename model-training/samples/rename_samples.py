import os
import sys

path = "/Volumes/SSD/collection/5_5"
files = os.listdir(path)

for index, file in enumerate(files):
    old_path = os.path.join(path, file)
    if file[0] == '.':
        pass
    else:
        segment = int(file.split('_')[1])
        frame = file.split('_')[2].split('.')[0]
        new_name = f"5_{53+segment}_{frame}.npy"
        
        new_path = os.path.join(path, new_name)

        os.rename(old_path, new_path)


print(files)