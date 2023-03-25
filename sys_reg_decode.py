# * Copyright (C) 2023 Zenon Xiu

import xml.etree.ElementTree as ET
import re

def find_fields_by_id(node, field_id_to_match,reg_name, value) :
	for element in node.findall('*'):
		for fields in element.findall('fields'):
			fields_id=fields.get('id')
			if fields_id==field_id_to_match:
				reg_bit_field_decode(fields,reg_name, value)
				return fields
		find_fields_by_id(element, field_id_to_match,reg_name, value)

def reg_bit_field_decode(fields, reg_name, value) :
	for field in fields.findall('field'):
		print('-------------------------------------------------------------')
		field_name = field.find('field_name')
		field_description = field.find('field_description').find('para')
		if (field_description is not None) :
			field_description_full_text = ET.tostring(field_description, encoding='unicode')
			field_description_text = re.sub('<.*?>', '', field_description_full_text)
		else:
			field_description_text=None
		# get the MSB and LSB values
		field_msb = int(field.find('field_msb').text)
		field_lsb = int(field.find('field_lsb').text)
		mask = (1 << (field_msb-field_lsb + 1))-1
		bit_field_value= (value >>field_lsb)&mask
		print('bit[',field_msb,':',field_lsb,']', 'is',bin(bit_field_value))
		# print the field information
		if(field_name is not None and field_name.text is not None ):
			print('Field Name:', ''.join(field_name.itertext()))
		if (field_description_text is not None) :
			print('Field Description:', field_description_text)

		fields_condition=field.find('fields_condition')
		if fields_condition is not None and fields_condition.text is not None:
			print(fields_condition.text)
		field_values_instance=field.find('field_values')
		if(field_values_instance is not None):
			for field_value_instance in field_values_instance.findall('field_value_instance'):
				field_value_text=''
				para_text=''
				field_value = field_value_instance.find('field_value')
				if field_value is not None and field_value is not None :
					field_value_text=field_value.text
					field_value_num=int(field_value_text,2)

				if bit_field_value==field_value_num :
					para = field_value_instance.find('field_value_description/para')
					if para is not None :
						para_full_text = ET.tostring(para,encoding='unicode')
						para_text = re.sub('<.*?>', '', para_full_text)
					print(field_value_text+':'+para_text)
					field_value_link=field_value_instance.find(".//field_value_links_to")
					if field_value_link is not None :
						linked_field_id = field_value_link.get('linked_field_id')
						linked_field_condition=field_value_link.get('linked_field_condition')
						if linked_field_id is not None :
							linked_feilds=find_fields_by_id(fields,linked_field_id,reg_name, value)


def reg_bit_fields_decode(node, reg_name, value) :
	for fields in node.findall('fields') :
		if (fields.find('fields_condition') is not None):
			print()
			print('######################')
			print(fields.find('fields_condition').text)
			print('######################')
			# iterate over the fields
		reg_bit_field_decode(fields,reg_name, value)

def start_reg_decode(xmlstring, reg_name, value):
	xmlstring = "<root>\n" + xmlstring + "</root>\n"
	root = ET.XML(xmlstring)
	reg_bit_fields_decode(root, reg_name, value)
