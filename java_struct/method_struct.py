#!/usr/bin/env python
# -*- coding: utf-8 -*-
import constants as constants

'''
	方法
		注解
		返回值类型
		方法名
		参数
		方法体
'''

class MethodStruct(object):
	method_annotate = []
	method_return_type = ''
	method_name = ''
	method_params = []
	method_statement = []
	extra_space = ''
	extra_need_br = False

	def __init__(self,method_annotate,method_return_type,method_name,method_params):
		self.method_annotate = method_annotate
		self.method_return_type = method_return_type
		self.method_name = method_name
		self.method_params = method_params

	def generateStr(self):
		generateStr = ''
		if len(self.method_annotate):
			for item in self.method_annotate:
				generateStr = generateStr + constants.ONE_TAB + self.extra_space + item + constants.END_LINE
		generateStr = generateStr + constants.ONE_TAB + self.extra_space + 'public ' \
			+ self.method_return_type + ' ' + self.method_name + '(' 
		if len(self.method_params) != 0:
			if self.extra_need_br:
				generateStr = generateStr + constants.END_LINE
				for item in self.method_params:
					if item == self.method_params[len(self.method_params) - 1]:
						generateStr = generateStr + constants.THREE_TAB + self.extra_space + item.generateStr();
						generateStr = generateStr[0:len(generateStr)-1] + constants.END_LINE
					else:
						generateStr = generateStr + constants.THREE_TAB + self.extra_space + item.generateStr() \
							 + constants.END_LINE
			else:
				#不需要br的，
				for item in self.method_params:
					if item == self.method_params[len(self.method_params) - 1]:
						generateStr = generateStr + item.generateStr();
						generateStr = generateStr[0:len(generateStr)-1] 
					else:
						generateStr = generateStr + item.generateStr() 
		if len(self.method_statement) == 0:
			if len(self.method_params) == 0:
				generateStr = generateStr + self.extra_space + ');'+ constants.SPACE_LINE
			else:
				generateStr = generateStr + constants.ONE_TAB + self.extra_space + ');'+ constants.SPACE_LINE
		else:
			if self.extra_need_br:
				generateStr = generateStr + constants.ONE_TAB + self.extra_space + '){'+ constants.END_LINE
			else:
				generateStr = generateStr + '){'+ constants.END_LINE
			for item in self.method_statement:
				generateStr = generateStr + constants.TWO_TAB + self.extra_space + item

			generateStr = generateStr + constants.ONE_TAB + self.extra_space + "}" + constants.SPACE_LINE
		return generateStr
	
