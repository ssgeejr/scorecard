#!/usr/bin/env python3

import glob, os
from pathlib import Path

working_dir = "/opt/apps/sc.data"
os.chdir(working_dir)
for file in glob.glob("*.csv"):
    print(file)
    old_file = os.path.join(working_dir,file)
    new_file = os.path.join(working_dir,file+'.old')
    print('New File: ',new_file)
    # os.rename(old_file, new_file)
    print(os.path.basename(old_file))
    filename = Path(old_file).stem
    print('File Name: ',filename)
