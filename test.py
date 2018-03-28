#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
# import dircache

# import constants as constants

# apis = dircache.listdir('apis/')

# parentDir = "./apis/"

# for api in apis:
# 	path = parentDir+api
# 	f = open(path,'r')
# 	jsonstr = json.load(f)
# 	print type(jsonstr)



# f = open('./test.java','w')

# # dictJson = json.load(f)


# # print type(dictJson)

# # for key in dictJson.keys():
# #  	print isinstance(dictJson[key],int)

# f.write("import java.*")
# f.write(constants.blackLine)
# f.write("public class Main {")

# f.write("}")


import re

import java_struct.class_struct as cs
import java_struct.params_struct as ps
import java_struct.method_struct as ms
import java_struct.field_struct as fs

import constants as constants
import generate_file as builder

import sys

mydict = {
	int:"xxx",
	"b":"xxx"
}

mylist = []

jsonstr = '{					\
											\
					"__id":"1111",			\
					"content":"11111",		\
					"name":"1111",			\
					"count":1, 				\
					"created_at":1234567899, \
                    "items":[1,2,3,4,5,6,7]  \
											\
			}'
json_dict = json.loads(jsonstr)

print(type(json_dict['items'][0]))


# print(constants.get_java_type(mydict))
# print(constants.get_java_type('abc'))
# print(constants.get_java_type(111))
# print(constants.get_java_type(12345678911))
# print(constants.get_java_type(0.1))
# print(constants.get_java_type(mylist))
# print(constants.get_java_type("true"))
# print(constants.get_java_type('false'))


# reload(sys)

# sys.setdefaultencoding('uft-8')

# print constants.generate_java_field_name("comment_count")
# print constants.generate_java_field_name("comment")
# print constants.generate_java_field_name("__COuNt")

# def parsePath(path):
# 	pathPattern = '(:[a-zA-Z]*)'
# 	m = re.findall(pathPattern,path)
# 	for i in m:
# 		path = path.replace(i,'{'+i.replace(':','')+'}')
# 	return path,m

# path = '/api/okr/objectives/id/detail/parent/'

# print parsePath(path)[0]
# print parsePath(path)[1]



# myps = ps.params_struct("@GET","String","id")
# mypss = [myps]
# myms = ms.method_struct(["@GET(/api/xx/xxx)","@Expose"],"Observable<BaseResponse>","getInfos",mypss)
# mymss = [myms]
# myfs = fs.field_struct("String","name")
# myfss =[myfs]

# mycs = cs.class_struct([],True,"Test",myfss,mymss)

# print mycs.generateStr()


# exists = os.path.exists('build/apis/')
# if exists:
# 	pass
# else:
# 	os.makedirs('build/apis/')
# f = open('build/apis/testaApi.java','w')
# f.write('hello world')


# builder.generate_file('Text','println xxx',True)



















