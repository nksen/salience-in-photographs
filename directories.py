"""
--Naim Sen--
--Toby Ticehurst--
Dec 18

directories.py

Creation of a directory that will be used for the input and output images/metadata
"""

import os
import cv2


# a folder is a tuple of "name" and sub-folders
# sub-folders is a list of folders
# directories is a list of folders to create in the working directory
directories = [
    ("test1", [
        ("test1.1", []), 
        ("test1.2", [
            ("test1.2.1", [])
        ])
    ]),
]

# Recursive function takes the a list of sub folders to create (defined in the directories list)
# and the name of the current folder (from the working directory)
def create_directories(sub_dirs, parent_dir_name = ""):

    # loop through list of sub-folders
    for child in sub_dirs:

        dir_name = parent_dir_name + child[0]

        # Create target Directory if don't exist
        if not os.path.exists(dir_name):
            #print("Directory " , dir_name ,  " Created ")
            os.mkdir(dir_name)
        else:
            #print("Directory " , dir_name ,  " already exists")

        # recursive call
        create_directories(child[1], dir_name + "/")


create_directories(directories)
cv2.waitKey(0)