#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import logging
import copy

SPACE_LINE = "\n\r\n\r"
END_LINE = "\n\r"
ONE_TAB = '    '
TWO_TAB = ONE_TAB + ONE_TAB
THREE_TAB = ONE_TAB + TWO_TAB
FOUR_TAB = TWO_TAB + TWO_TAB

APIS_FILE_DIR = "apis/"

JSON_EXT = ".json"

CONF_KEY_API = "api"
CONF_KEY_METHOD = "method"
CONF_KEY_GENERATE_METHOD_NAME = "generate_method_name"
CONF_KEY_REQUEST = "request"
CONF_KEY_RESPONSE_NAME = "response_name"
CONF_KEY_RESPONSE = "response"
CONF_KEY_RESPONSE_LIST = "list"


PATH_PATTERN = '(:[a-zA-Z]*)'

BUILD_API_FILE_DIR = './build/apis/'
BUILD_BEAN_FILE_DIR = './build/bean/'
JAVA_EXT = '.java'



# todo
API_FILE_IMPORT = [
	'package com.worktile.kernel.network.api;',
	END_LINE,
	'import com.worktile.kernel.data.*;',
	'import com.worktile.kernel.network.data.*;',
	'import java.util.Map;',
	'import io.reactivex.Observable;',
	'import retrofit2.http.*;',
	END_LINE
]

REQUEST_BEAN_IMPORT = [
	'',
	'import com.google.gson.annotations.Expose;',
	'import com.google.gson.annotations.SerializedName;',
	'',
	'import java.util.List;',
	''
]

RESPONSE_BEAN_IMPORT = copy.deepcopy(REQUEST_BEAN_IMPORT)

RESPONSE_BEAN_IMPORT.insert(3,'import org.greenrobot.greendao.annotation.*;')

NORMAL_BEAN_PACKAGE_STATEMENT_FORMAT = 'package com.worktile.kernel.data.{0};' 
REQUEST_BEAN_PACKAGE_STATEMENT_FORMAT = 'package com.worktile.kernel.network.data.request.{0};'
RESPONSE_BEAN_PACKAGE_STATEMENT_FORMAT = 'package com.worktile.kernel.network.data.response.{0};'


def first_char_upper(string):
	if len(string) == 0:
		return string
	else:
		return string[0].upper() + string[1:]

def first_char_lower(string):
	if len(string) == 0:
		return string
	else:
		return string[0].lower() + string[1:]


FIELD_PATTERN = '[a-zA-Z]{1,}'
'''
	将__a_bbb_ccc 这种形式转成aBbbCcc
'''
def generate_java_field_name(string):
	result = ''
	if len(string) != 0:
		string = string.lower()
		m = re.findall(FIELD_PATTERN,string)
		for item in m:
			if m.index(item) == 0:
				result = result + item
			else:
				result = result + first_char_upper(item)
	return result

def verify_api_item(item):
	if type(item) is dict:
		if not item.has_key(CONF_KEY_API):
			log_verify_error(CONF_KEY_API)
		if not item.has_key(CONF_KEY_METHOD):
			log_verify_error(CONF_KEY_METHOD)
		if not item.has_key(CONF_KEY_GENERATE_METHOD_NAME):
			log_verify_error(CONF_KEY_GENERATE_METHOD_NAME)
		if not item.has_key(CONF_KEY_REQUEST):
			log_verify_error(CONF_KEY_REQUEST)
		if not item.has_key(CONF_KEY_RESPONSE_NAME):
			log_verify_error(CONF_KEY_RESPONSE_NAME)
		if not item.has_key(CONF_KEY_RESPONSE):
			log_verify_error(CONF_KEY_RESPONSE)			

	else:
		print "parse failed,in apis file,must be [{ },{ },...]"

def log_verify_error(string):
	logging.error('parse field, must have {0}'.format(string))
	exit()

def log_error(string):
	logging.error(string)

TYPE_MAP_DICT = {
	int : 'int',
	float : 'float',
	str : 'String',
	list : 'List',
	dict : 'Object', #这个不应该出现
	unicode : 'String'
}


'''
	获取对应的java语言类型
'''
def get_java_type(data):
	if type(data) is int and data >= 999999999:
		return 'long'
	if (type(data) is str or type(data) is unicode)  and \
		(data.upper() == 'TRUE' or data.upper() == 'FALSE'):
		return 'boolean'
	if TYPE_MAP_DICT.has_key(type(data)):
		result_type = TYPE_MAP_DICT[type(data)]
	else:
		result_type = 'String'
	return result_type

'''
	英文单词复数转单数
'''
def get_english_signle_type(string):

	pass
