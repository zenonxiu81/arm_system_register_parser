# * Copyright (C) 2023 Zenon Xiu

from sys_reg_decode import start_reg_decode as start_reg_decode
import os


def extract_reg_xml(file_path,register_name,value) : 
    # open the file and read its contents
	with open(file_path, 'r') as f:
		between_flag_and_end=False
		for line in f:
			if line.startswith('<fields id') and not line.startswith((' ', '\t')):
				between_flag_and_end = True
				current_lines = line
			elif line.startswith('</fields>') and not line.startswith((' ', '\t')) and between_flag_and_end:
				between_flag_and_end = False
				current_lines=current_lines+line
				start_reg_decode(current_lines,register_name,value)
			elif between_flag_and_end:
				current_lines=current_lines+line
