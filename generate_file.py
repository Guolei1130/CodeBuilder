#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import constants as constants
import shutil

def init_dir():
	if os.path.exists(constants.BUILD_API_FILE_DIR):
		shutil.rmtree(constants.BUILD_API_FILE_DIR)
		print 'delete {0} success'.format(constants.BUILD_API_FILE_DIR)
	if os.path.exists(constants.BUILD_BEAN_FILE_DIR):
		shutil.rmtree(constants.BUILD_BEAN_FILE_DIR)
		print 'delete {0} success'.format(constants.BUILD_BEAN_FILE_DIR)
	print 'init success'		

def generate_file(filename,content,is_api,cover=False):
	ensure_build_dir_exit()
	mydir = ensure_dir_exit(is_api)
	filename = constants.first_char_upper(filename)

	filename = mydir + filename + constants.JAVA_EXT
	if os.path.exists(filename) and not cover:			
		print '{0} exist'.format(filename)
	else:
		try:
			f = open(filename,'w')
			f.write(content)
		finally:
			f.close

def ensure_build_dir_exit():
	build_dir = './build'
	if not os.path.exists(build_dir):
		os.mkdir(build_dir)

def ensure_dir_exit(is_api):
	file_dir = ''
	if is_api:
		file_dir = constants.BUILD_API_FILE_DIR
	else:
		file_dir = constants.BUILD_BEAN_FILE_DIR

	if os.path.exists(file_dir):
		pass
	else:
		os.mkdir(file_dir)

	return file_dir

