# * Copyright (C) 2023 Zenon Xiu


import os
from extract_xml import extract_reg_xml as extract_reg_xml

def search_directory(directory, namestring):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if namestring in file:
                return os.path.join(root, file)
    return None


register_name=input("Enter the register name:")
register_name_='-'+register_name
value = int(input("Enter the register value(hex format): "),16)


cwd = os.getcwd()
directory =os.path.join(cwd,'sys_reg_xml')
file_name = search_directory(directory, register_name_)
if file_name:
    extract_reg_xml(file_name,register_name,value)
else:
    print("register '{register_name}' not found")
