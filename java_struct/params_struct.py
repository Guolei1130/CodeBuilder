#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
	参数的结构
		注解
		类型
		名称

"""


class ParamsStruct(object):
	params_annotate = ''
	params_type = ''
	params_name = ''

	def __init__(self,params_annotate,params_type,params_name):
		self.params_annotate = params_annotate
		self.params_type = params_type
		self.params_name = params_name

	def generateStr(self):
		generateStr = ''
		if len(self.params_annotate) != 0:
			generateStr = generateStr + self.params_annotate + ' '
		return generateStr + self.params_type + ' ' + self.params_name + ','
		