#!/usr/bin/env python
# -*- coding: utf-8 -*-

import constants as constants


'''
	
	类结构
		包语句
		import 语句
		类名
		字段
		一系列方法
		内部类
		
'''

class ClassStruct(object):

	class_package_statement = ''
	class_import_statement = []
	class_annotate = []
	class_is_interface = True
	class_name = ''
	class_fields = []
	class_methods = []
	class_inner_class = []
	extra_space = ''

	def __init__(self, import_statement, is_interface, class_name, class_fields, class_methods):
		self.class_import_statement = import_statement
		self.class_is_interface = is_interface
		self.class_name = class_name
		self.class_fields = class_fields
		self.class_methods = class_methods
		
	def generateStr(self):
		generateStr = ''
		# 包语句
		if self.class_package_statement != '':
			generateStr = generateStr + self.extra_space + self.class_package_statement + constants.END_LINE
		#import 语句
		if len(self.class_import_statement) != 0:
			for item in self.class_import_statement:
				generateStr = generateStr + self.extra_space + item + constants.END_LINE
		# 类注解
		if len(self.class_annotate) != 0:
			for item in self.class_annotate:
				generateStr = generateStr + self.extra_space + item + constants.END_LINE
		# 接口还是正常类
		if self.class_is_interface:
			generateStr = generateStr + self.extra_space + 'public interface ' + self.class_name + '{' + constants.SPACE_LINE
		else:
			generateStr = generateStr + self.extra_space + 'public class ' + self.class_name + '{' + constants.SPACE_LINE
		# 字段
		if len(self.class_fields) != 0:
			for item in self.class_fields:
				item.extra_space = self.extra_space
				generateStr = generateStr + item.generateStr() + constants.END_LINE
		generateStr = generateStr + constants.END_LINE		
		# 方法
		if len(self.class_methods) != 0:
			for item in self.class_methods:
				item.extra_need_br = self.class_is_interface
				item.extra_space = self.extra_space
				generateStr = generateStr + item.generateStr()
		# 内部类
		if len(self.class_inner_class) != 0:
			for item in self.class_inner_class:
				item.extra_space = constants.ONE_TAB + self.extra_space
				generateStr = generateStr + item.generateStr()	
		generateStr = generateStr + self.extra_space + '}' + constants.END_LINE 
		return generateStr


