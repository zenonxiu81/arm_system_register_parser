# * Copyright (C) 2023 Zenon Xiu

import xml.etree.ElementTree as ET
import re


def _feature_set(text):
	return set(re.findall(r'FEAT_[A-Za-z0-9_]+', text or ''))


def find_fields_by_id(node, field_id_to_match, reg_name, value, writer=print, collector=None, condition_text=None):
	writer_fn = writer if writer is not None else (lambda *_: None)
	for element in node.findall('*'):
		for fields in element.findall('fields'):
			fields_id = fields.get('id')
			if fields_id == field_id_to_match:
				reg_bit_field_decode(fields, reg_name, value, writer_fn, collector, condition_text)
				return fields
		find_fields_by_id(element, field_id_to_match, reg_name, value, writer_fn, collector, condition_text)


def reg_bit_field_decode(fields, reg_name, value, writer=print, collector=None, condition_text=None):
	writer_fn = writer if writer is not None else (lambda *_: None)
	for field in fields.findall('field'):
		writer_fn('-------------------------------------------------------------')
		field_name_node = field.find('field_name')
		field_name = ''.join(field_name_node.itertext()) if field_name_node is not None else ''
		field_description_para = field.find('field_description').find('para')
		if field_description_para is not None:
			field_description_full_text = ET.tostring(field_description_para, encoding='unicode')
			field_description_text = re.sub('<.*?>', '', field_description_full_text)
		else:
			field_description_text = ''
		field_msb = int(field.find('field_msb').text)
		field_lsb = int(field.find('field_lsb').text)
		mask = (1 << (field_msb - field_lsb + 1)) - 1
		bit_field_value = (value >> field_lsb) & mask
		writer_fn(f"bit[{field_msb}:{field_lsb}] is {bin(bit_field_value)}")
		if field_name:
			writer_fn(f"Field Name: {field_name}")
		if field_description_text:
			writer_fn(f"Field Description: {field_description_text}")

		fields_condition = field.find('fields_condition')
		if fields_condition is not None and fields_condition.text is not None:
			writer_fn(fields_condition.text)
		condition_str = condition_text or ''
		if fields_condition is not None and fields_condition.text:
			condition_str = fields_condition.text if not condition_str else f"{condition_str}\n{fields_condition.text}"

		entry = {
			'msb': field_msb,
			'lsb': field_lsb,
			'bit_value': bit_field_value,
			'bit_value_bin': bin(bit_field_value),
			'name': field_name,
			'description': field_description_text,
			'meaning_text': field_description_text,
			'meaning_features': _feature_set(condition_str) | _feature_set(field_description_text),
			'condition_text': condition_str,
			'field_value_text': '',
		}

		field_values_instance = field.find('field_values')
		if field_values_instance is not None:
			for field_value_instance in field_values_instance.findall('field_value_instance'):
				field_value_text = ''
				para_text = ''
				field_value = field_value_instance.find('field_value')
				if field_value is not None:
					field_value_text = field_value.text
					field_value_num = int(field_value_text, 2)

				if bit_field_value == field_value_num:
					para = field_value_instance.find('field_value_description/para')
					if para is not None:
						para_full_text = ET.tostring(para, encoding='unicode')
						para_text = re.sub('<.*?>', '', para_full_text)
					writer_fn(f"{field_value_text}:{para_text}")
					entry['field_value_text'] = field_value_text
					entry['meaning_text'] = para_text or entry['meaning_text']
					entry['meaning_features'] = _feature_set(entry['condition_text']) | _feature_set(para_text)
					field_value_link = field_value_instance.find('.//field_value_links_to')
					if field_value_link is not None:
						linked_field_id = field_value_link.get('linked_field_id')
						linked_field_condition = field_value_link.get('linked_field_condition')
						if linked_field_id is not None:
							find_fields_by_id(fields, linked_field_id, reg_name, value, writer_fn, collector, linked_field_condition or condition_str)

		if collector is not None:
			collector.append(entry)


def reg_bit_fields_decode(node, reg_name, value, writer=print, collector=None):
	writer_fn = writer if writer is not None else (lambda *_: None)
	for fields in node.findall('fields'):
		condition = fields.find('fields_condition')
		condition_text = condition.text if condition is not None else None
		if condition_text:
			writer_fn('')
			writer_fn('######################')
			writer_fn(condition_text)
			writer_fn('######################')
		reg_bit_field_decode(fields, reg_name, value, writer_fn, collector, condition_text)


def start_reg_decode(xmlstring, reg_name, value, writer=print, collector=None):
	xmlstring = "<root>\n" + xmlstring + "</root>\n"
	root = ET.XML(xmlstring)
	reg_bit_fields_decode(root, reg_name, value, writer, collector)
