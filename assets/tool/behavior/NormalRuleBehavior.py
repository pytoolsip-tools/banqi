# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2019-09-23 17:43:12
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-09-23 23:10:41

from _Global import _GG;
from function.base import *;

def __getExposeData__():
	return {
		# "exposeDataName" : {},
	};

def __getExposeMethod__(DoType):
	return {
		"onCheckItem" : DoType.Override,
		"getTipsItems" : DoType.Override,
	};

def __getDepends__():
	return [
		# {
		# 	"path" : "tempBehavior", 
		# 	"basePath" : _GG("g_CommonPath") + "behavior/",
		# },
	];

class NormalRuleBehavior(_GG("BaseBehavior")):
	def __init__(self):
		super(NormalRuleBehavior, self).__init__(__getDepends__(), __getExposeData__(), __getExposeMethod__, __file__);
		self._className_ = NormalRuleBehavior.__name__;
		pass;

	# 默认方法【obj为绑定该组件的对象，argList和argDict为可变参数，_retTuple为该组件的前个函数返回值】
	# def defaultFun(self, obj, *argList, _retTuple = None, **argDict):
	# 	_GG("Log").i(obj._className_);
	# 	pass;

	def onCheckItem(self, obj, curItem, item, _retTuple = False):
		if curItem.getChessBitmap().color() == item.getChessBitmap().color():
			return False;
		if curItem.getChessBitmap().point() >= item.getChessBitmap().point():
			return True;
		return False;

	def getTipsItems(self, obj, curItem, _retTuple = False):
		row, col = obj.getItemMt(curItem);
		items = [];
		def checkItem(r, c):
			item = obj.getItem(r, c);
			if item:
				items.append(item);
		checkItem(row-1, col);
		checkItem(row+1, col);
		checkItem(row, col-1);
		checkItem(row, col+1);
		return items;
