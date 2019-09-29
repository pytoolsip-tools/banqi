# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2019-09-30 00:27:36
# @Last Modified by:   Administrator
# @Last Modified time: 2019-09-30 00:27:36

from _Global import _GG;
from function.base import *;

def __getExposeData__():
	return {
		# "exposeDataName" : {},
	};

def __getExposeMethod__(DoType):
	return {
		"toggleTurn" : DoType.AddToRear,
		"checkOpRight" : DoType.AddToRear,
	};

def __getDepends__():
	return [
		# {
		# 	"path" : "tempBehavior", 
		# 	"basePath" : _GG("g_CommonPath") + "behavior/",
		# },
	];

class NormalAIBehavior(_GG("BaseBehavior")):
	def __init__(self):
		super(NormalAIBehavior, self).__init__(__getDepends__(), __getExposeData__(), __getExposeMethod__, __file__);
		self._className_ = NormalAIBehavior.__name__;
		self.__isAiTurn = False;
		pass;

	# 默认方法【obj为绑定该组件的对象，argList和argDict为可变参数，_retTuple为该组件的前个函数返回值】
	# def defaultFun(self, obj, *argList, _retTuple = None, **argDict):
	# 	_GG("Log").i(obj._className_);
	# 	pass;

	def toggleTurn(self, obj, curTurn = -1, _retTuple = None):
		if obj.checkFirstTurn():
			return;
		self.__isAiTurn = True;
		# todo: 执行机器人逻辑
		self.__isAiTurn = False;
		pass;

	def checkOpRight(self, obj, _retTuple = None):
		if not _retTuple:
			if not obj.checkFirstTurn() and self.__isAiTurn:
				return True;
		return _retTuple;