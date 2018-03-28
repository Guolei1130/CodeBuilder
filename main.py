#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dircache
import os

import constants as constants
import parse_api_file as parse
import generate_file as builder

def start_parse():
	apis = dircache.listdir(constants.APIS_FILE_DIR)
	if len(apis) == 0:
		print "apis dir not have any api file"
		exit()
	for api in apis:
		if os.path.splitext(constants.APIS_FILE_DIR + api)[1] == constants.JSON_EXT:
			#解析文件
			parse.parse_api_file(api)


if __name__ == '__main__':
	builder.init_dir()
	start_parse()
