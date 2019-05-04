#%%
import os
import re
import shutil
from pathlib import Path

basepath = Path(
    r'D:\Users\Naim\OneDrive\CloudDocs\UNIVERSITY\S8\MPhys_s8\results\first_run'
)

outpath = Path(
    r'D:\Users\Naim\OneDrive\CloudDocs\UNIVERSITY\S8\MPhys_s8\results\first_run_allheadlines'
)

for foldername in os.listdir(str(basepath)):
    parentfp = basepath / foldername
    display(parentfp)
    for subfoldername in os.listdir(str(parentfp)):
        childpath = parentfp / subfoldername
        for filename in os.listdir(childpath):
            res = re.match('headline_.*_.*\.png', str(filename))
            if res is not None:
                imgpath = childpath / filename
                shutil.copy(imgpath, outpath)

#%%
