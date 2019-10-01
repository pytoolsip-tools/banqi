# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2019-09-30 00:27:36
# @Last Modified by:   Administrator
# @Last Modified time: 2019-09-30 00:27:36
import wx;
import random;
from functools import cmp_to_key;

from _Global import _GG;
from function.base import *;

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/") + "/";

ChessConst = require(CURRENT_PATH + "../config", "chess_config", "ChessConst");

def __getExposeData__():
	return {
		# "exposeDataName" : {},
	};

def __getExposeMethod__(DoType):
	return {
		"toggleTurn" : DoType.AddToRear,
		"checkOpRight" : DoType.AddToRear,
		"showDisableTipWin" : DoType.Override,
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
		if obj.checkFirstTurn() or self.__isAiTurn:
			return;
		# 执行机器人逻辑
		wx.CallLater(500, self.operateAI, obj);
		pass;

	def checkOpRight(self, obj, _retTuple = None):
		if not _retTuple:
			if not obj.checkFirstTurn() and self.__isAiTurn:
				return True;
		return _retTuple;

	def showDisableTipWin(self, obj, tips, _retTuple = None):
		if not self.__isAiTurn:
			wx.TipWindow(obj, tips);

	def operateAI(self, obj):
		_GG("Log").d("Start Playing by normal AI.");
		self.__isAiTurn = True;
		self.checkItems(obj);
		self.__isAiTurn = False;
		_GG("Log").d("End Playing by normal AI.");

	def getSelfItems(self, obj, isFirst = False, isShown = True):
		items = [];
		for item in obj.getChessList():
			if not isShown:
				if not item.isShownBitmap():
					items.append(item);
			elif item.isShownBitmap():
				bitmap = item.getChessBitmap();
				if bitmap.value() != ChessConst.Empty.value and obj.checkFirstColor(bitmap.color()) == isFirst:
					items.append(item);
		return items;

	def getAiTipsItems(self, obj, curItem):
		items = []
		for item in obj.getTipsItems(curItem):
			if obj.checkItem(item, curItem = curItem):
				items.append(item);
		return items;

	def getTipsItemsMap(self, obj):
		itemsMap, firstItemsMap = {}, {};
		for item in obj.getChessList():
			bitmap = item.getChessBitmap();
			if bitmap.value() != ChessConst.Empty.value:
				if obj.checkFirstColor(bitmap.color()):
					firstItemsMap[item] = self.getAiTipsItems(obj, item);
				else:
					itemsMap[item] = self.getAiTipsItems(obj, item);
		return itemsMap, firstItemsMap;

	def sortItems(self, items):
		def compareFunc(item1, item2):
			if not item2.isShownBitmap():
				return -1;
			if not item1.isShownBitmap():
				return 1;
			return item2.getChessBitmap().value() - item1.getChessBitmap().value();
		items.sort(key = cmp_to_key(compareFunc));

	# 检测吃完tipsItem棋子后是否会被吃
	def checkFirstItems(self, obj, item, tipsItem, firstItems):
		for firstItem in firstItems:
			for ftItem in obj.getTipsItems(firstItem):
				if ftItem == tipsItem:
					if obj.checkItem(item, curItem = firstItem):
						return True;
					break;
		return False;

	# 对方可能吃item的棋子
	def getFirstItems(self, obj, item, firstItems):
		items = [];
		for firstItem in firstItems:
			for ftItem in obj.getTipsItems(firstItem):
				if ftItem == item:
					items.append(firstItem);
					break;
		return items;

	def checkItems(self, obj):
		selfItems = self.getSelfItems(obj);
		self.sortItems(selfItems);
		firstItems = self.getSelfItems(obj, isFirst = True);
		hideItems = self.getSelfItems(obj, isShown = False);
		tipsItemsMap, firstItemsMap = self.getTipsItemsMap(obj);
		for item in selfItems:
			if item in tipsItemsMap:
				isBeEaten = self.checkFirstItems(obj, item, item, firstItems); # 是否会被吃
				for tipsItem in tipsItemsMap[item]:
					if isBeEaten or tipsItem.getChessBitmap().value() != ChessConst.Empty.value:
						# 判断吃后是否会被吃
						if not self.checkFirstItems(obj, item, tipsItem, firstItems):
							self.operateItem(obj, item, tipsItem);
							return True;
		# 进行翻棋
		if len(hideItems) > 0:
			for item in hideItems:
				if len(self.getFirstItems(obj, item, firstItems)) == 0:
					self.showItem(obj, item);
					return True;
			idx = random.randint(0, len(hideItems)-1);
			self.showItem(obj, hideItems[idx]);
			return True;
		# 移动棋子
		for i in range(len(selfItems)-1, -1,-1):
			item = selfItems[i];
			if item in tipsItemsMap:
				for tipsItem in tipsItemsMap[item]:
					self.operateItem(obj, item, tipsItem);
					return True;
		_GG("Log").e("Failed to click item by normal AI !");
		return False;

	def operateItem(self, obj, item, targetItem):
		obj.onRClickItem(item);
		obj.onClickItem(targetItem);
		pass;

	def showItem(self, obj, item):
		obj.onDClickItem(item);
		pass;