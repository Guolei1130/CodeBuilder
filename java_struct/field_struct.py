#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
	字段
		注解
		字段类型
		字段名
'''

import constants as constants

class FieldStruct(object):

	field_annotate = []
	field_name = ''
	field_type = ''
	extra_space = ''

	def __init__(self, field_annotate, field_type, field_name):
		self.field_annotate = field_annotate
		self.field_type = field_type
		self.field_name = constants.generate_java_field_name(field_name)


	def generateStr(self):
		generateStr = ''
		if len(self.field_annotate) != 0:
			for annoate in self.field_annotate:
				generateStr = generateStr + constants.ONE_TAB + self.extra_space + annoate + constants.END_LINE				
		return  generateStr + constants.ONE_TAB + self.extra_space + 'private ' + self.field_type + ' ' \
				+ self.field_name + ';' + constants.END_LINE