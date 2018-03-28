#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import re
import constants as constants
import generate_file as builder

import java_struct.class_struct as cs
import java_struct.method_struct as ms
import java_struct.params_struct as ps
import java_struct.field_struct as fs 


module_name = ''

def parse_api_file(file_name):
	print 'start parse api file {0}'.format(file_name)
	f = open(constants.APIS_FILE_DIR + file_name,'r')
	try:
		json_list = json.load(f)
	except Exception as e:
		constants.log_error('{0} format error'.format(file_name))

	java_file_name = file_name.replace('.json','')
	global module_name 
	module_name = java_file_name.replace('Apis','') \
		.replace('apis','') \
		.replace('Api','')  \
		.replace('api','')  \
		.lower()

	is_api = True

	class_import_statement = constants.API_FILE_IMPORT
	class_is_interface = True
	class_name = java_file_name
	class_fields = []
	class_methods = []

	for item in json_list:
		#每个item是一个dict
		class_methods.append(parse_api(item))
	generate_class = cs.ClassStruct(class_import_statement,class_is_interface,
		class_name,class_fields,class_methods)
	builder.generate_file(java_file_name,generate_class.generateStr(),is_api)

	print 'end parse api file {0}'.format(file_name)

'''
	解析api，

	生成api涉及到的一些类

	返回值:method_struct
'''
def parse_api(item):
	constants.verify_api_item(item)
	real_path,paths = parse_api_path(item[constants.CONF_KEY_API])
	method = parse_api_method(item[constants.CONF_KEY_METHOD])
	# 注解：@GET(/api/okr/cycles/{id})
	method_annotates = []
	method_params = []
	method_name = item[constants.CONF_KEY_GENERATE_METHOD_NAME]
	method_return_type = 'Observable<BaseResponse<{0}>>'
	method_annotates.append('{0}({1})'.format(method,real_path))
	#处理接口中的path
	if len(paths) != 0:
		for path_item in paths:
			method_params.append(ps.ParamsStruct('@Path("{0}")'.format(path_item),'String',path_item)) 
	# 处理request中的数据
	if method == '@GET':
		if type(item[constants.CONF_KEY_REQUEST]) is dict and len(item[constants.CONF_KEY_REQUEST]) != 0:
			#转成map，因为有些参数可能不必要传，需要自己判断
			method_params.append(ps.ParamsStruct('@QueryMap','Map<String,Object>','params'))
		else:
			pass
	else:
		# 生成Request对象
		if type(item[constants.CONF_KEY_REQUEST]) is dict:
			if len(item[constants.CONF_KEY_REQUEST]) != 0:
				generate_request_bean(item[constants.CONF_KEY_REQUEST],method_name)
				field_type = constants.first_char_upper(method_name) + 'Request'
				method_params.append(ps.ParamsStruct('@Body',field_type,method_name + 'Request'))
			else:
				method_params.append(ps.ParamsStruct('@Body','EmptyRequest','emptyRequest'))
		else:
			constants.log_error("in apis file,request must be json object")
	response_name = item[constants.CONF_KEY_RESPONSE_NAME]
	if len(response_name) == 0:
		constants.log_error("response_name cannot be '',if response is Void,you should set response_name to any word")
	response = item[constants.CONF_KEY_RESPONSE]
	if type(response) is list:
		# 这种情况应该不会出现
		generate_response_bean(response[0],response_name)
		method_return_type = method_return_type.format('List<{0}>'.format(response_name))
	elif type(response) is dict and len(response) == 0:
		method_return_type = method_return_type.format('Void')
	else:
		if item.has_key(constants.CONF_KEY_RESPONSE_LIST):
			# 如果是list，先生成XXXResponse
			generate_response_class = generate_response_bean_with_list(response,response_name,method_name)
		else:
			generate_response_class = generate_response_bean(response,response_name,True)
		method_return_type = method_return_type.format(generate_response_class.class_name)
	print 'parse api {0} success'.format(real_path) 
	return ms.MethodStruct(method_annotates,method_return_type,method_name,method_params)
		

'''
	解析路径 /api/okr/objectives/:id/detail/:id2
	返回值 替换后的路径已经
'''

def parse_api_path(path):
	path = '"{0}"'.format(path)
	paths = []
	m = re.findall(constants.PATH_PATTERN,path)
	for i in m:
		targetStr = i.replace(':','')
		paths.append(targetStr)
		path = path.replace(i,'{'+targetStr+'}')
	return path, paths

'''
	将get、post等转为
	@GET @POST 
'''
def parse_api_method(method):
	return '@' + method.upper()

'''
	生成RequestBean
'''
def generate_request_bean(bean_dict,class_name):
	class_name = constants.first_char_upper(class_name) + 'Request'
	generate_class = parse_request_class(bean_dict,class_name)
	generate_class.class_package_statement = constants.REQUEST_BEAN_PACKAGE_STATEMENT_FORMAT.format(module_name)
	generate_class.class_import_statement = constants.REQUEST_BEAN_IMPORT
	builder.generate_file(class_name,generate_class.generateStr(),False)


'''
	解析request部分的数据
'''		
def parse_request_class(bean_dict,class_name):
	class_name = constants.first_char_upper(class_name)
	class_inner_class = []
	class_field = []
	class_methods= []

	for key in bean_dict:
		field_annotates = generate_custom_field_annotate(key)
		if type(bean_dict[key]) is dict:
			# 内部类，jsonObject
			generate_inner_class = parse_request_class(bean_dict[key],key)
			class_inner_class.append(generate_inner_class)
			class_field.append(fs.FieldStruct(field_annotates,constants.first_char_upper(key),key))
		elif type(bean_dict[key]) is list:
			# list,但是对象需要转成内部类
			generate_inner_class = parse_request_class(bean_dict[key][0],key)
			class_inner_class.append(generate_inner_class)
			class_field.append(fs.FieldStruct(field_annotates,'List<{0}>'.format(constants.first_char_upper(key)),key))
		else:
			class_field.append(fs.FieldStruct(field_annotates,constants.get_java_type(bean_dict[key]),key))
	class_methods = generate_class_methods(class_field)

	generate_class = cs.ClassStruct([],False,class_name,class_field,class_methods)
	generate_class.class_inner_class = class_inner_class
	return generate_class
	
def generate_custom_field_annotate(serialize_name):
	return [
		'@SerializedName("{0}")'.format(serialize_name),
		"@Expose"
		]

'''
	生成类似GetCategorysResponse 这样的
'''
def generate_response_bean_with_list(response,response_name,method_name):
	if type(response) is not dict:
		constants.log_error('确认是不是请求列表类型的接口')

	class_name = constants.first_char_upper(method_name) + 'Response'
	class_field = []
	class_method = []
	for key in response:
		if type(response[key]) is list:
			generate_bean_class = generate_response_bean(response[key][0],response_name)
			class_field.append(fs.FieldStruct(generate_custom_field_annotate(key),
				'List<{0}>'.format(generate_bean_class.class_name),
				key))
		else:
			class_field.append(fs.FieldStruct(generate_custom_field_annotate(key),
				constants.get_java_type(response[key]),
				key))

	class_method  = generate_class_methods(class_field)

	generate_response_class = cs.ClassStruct(constants.RESPONSE_BEAN_IMPORT,False,class_name,
		class_field,class_method)

	generate_response_class.class_package_statement = constants.RESPONSE_BEAN_PACKAGE_STATEMENT_FORMAT.format(module_name)

	builder.generate_file(generate_response_class.class_name,generate_response_class.generateStr(),False)
	return generate_response_class
	

def generate_response_bean(response_dict,class_name,is_list=False):
	generate_class = parse_response_class(response_dict,class_name)
	generate_class.class_package_statement = constants.NORMAL_BEAN_PACKAGE_STATEMENT_FORMAT.format(module_name)
	builder.generate_file(generate_class.class_name,generate_class.generateStr(),False,is_list)
	return generate_class

'''
	解析response部分的数据
'''
def parse_response_class(response_dict,class_name):

	class_annotate = [
		'@Entity(\n\r{0}nameInDb="{1}",\n\r{0}generateGettersSetters = false,\n\r{0}generateConstructors = false)'
		.format(constants.TWO_TAB,class_name.lower())
	]
	class_name = constants.first_char_upper(class_name)
	class_field = []
	class_method = []

	for key in response_dict:
		field_annotates = generate_custom_field_annotate(key)
		if type(response_dict[key]) is list:
			if len(response_dict[key]) != 0:
				if type(response_dict[key][0]) is not dict:
					field_annotates.append('@Transient')
					class_field.append(fs.FieldStruct(field_annotates,
						'{0}[]'.format(constants.get_java_type(response_dict[key][0])),key))
				else:
					#生成新类	
					new_class_name = generate_response_bean(response_dict[key][0],key).class_name
					#to many的关系
					field_annotates.append('@ToMany(referencedJoinProperty = "foreignKeyId")')
					class_field.append(fs.FieldStruct(field_annotates,'List<{0}>'.format(new_class_name),key))
		elif type(response_dict[key]) is dict:
			#生成新类
			new_class_name = generate_response_bean(response_dict[key],key).class_name
			#to one的关系
			field_annotates.append('@ToOne(joinProperty = "id")')
			class_field.append(fs.FieldStruct(field_annotates,new_class_name,key))
			class_field.append(fs.FieldStruct([],'String','{0}_id'.format(constants.first_char_lower(new_class_name))))
		else:
			field_annotates.append('@Property(nameInDb = "{0}")'.format(key))
			class_field.append(fs.FieldStruct(field_annotates,constants.get_java_type(response_dict[key]),key))
	# 添加一个外键
	class_field.append(fs.FieldStruct(['@Property(nameInDb = "foreignkey_id")'],'String','foreignKeyId'))
	class_method = generate_class_methods(class_field)

 	generate_class = cs.ClassStruct(constants.RESPONSE_BEAN_IMPORT,False,class_name,class_field,class_method)
 	generate_class.class_annotate = class_annotate
	return generate_class

def generate_class_methods(class_fields):
	class_method = []
	for field in class_fields:
		if field.field_type.startswith('List'):
			continue
		temp_field_type = field.field_type
		temp_name = constants.first_char_upper(field.field_name)
		generate_params = ps.ParamsStruct('',field.field_type,field.field_name)
		generate_get_method = ms.MethodStruct([],temp_field_type,
			'get' + temp_name,
			[]
			)
		generate_get_method.method_statement = ['return {0};\n\r'.format(field.field_name) ]
		class_method.append(generate_get_method)
		generate_set_method = ms.MethodStruct([],'void',
			'set' + temp_name,
			[generate_params])
		generate_set_method.method_statement = ['this.{0} = {0}; \n\r'.format(field.field_name)]
		class_method.append(generate_set_method)

	return class_method