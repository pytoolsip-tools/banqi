# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2019-09-21 22:41:03
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-09-24 10:10:45

import wx;
import os;
import copy;
import math;
import random;

from _Global import _GG;
from function.base import *;

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/") + "/";

TurnConst = require(CURRENT_PATH + "../../config", "chess_config", "TurnConst");
ChessConst = require(CURRENT_PATH + "../../config", "chess_config", "ChessConst");
ChessCountConfig = require(CURRENT_PATH + "../../config", "chess_config", "ChessCountConfig");
ChessBitmap = require(CURRENT_PATH + "../../ui", "bitmap", "ChessBitmap");
GamePattern = require(CURRENT_PATH + "../../config", "chess_config", "GamePattern");

class BanQiViewUI(wx.Panel):
	"""docstring for BanQiViewUI"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None, params = {}):
		self.initParams(params);
		super(BanQiViewUI, self).__init__(parent, id, pos = self.__params["pos"], size = self.__params["size"], style = self.__params["style"]);
		self._className_ = BanQiViewUI.__name__;
		self._curPath = curPath;
		self.__viewCtr = viewCtr;
		self.__chessList = [];
		self.__bitmapList = [];
		self.__turn = -1;
		self.__firstTurn = -1;
		self.__curItem = None;
		self.__emptyBitmap = None;
		self.__tipsInfoMap = {};
		self.__pattern = GamePattern.Single.value;

	def initParams(self, params):
		# 初始化参数
		self.__params = {
			"pos" : (0,0),
			"size" : (-1,-1),
			"style" : wx.BORDER_THEME,
			"matrix" : (4,8),
			"focusColour" : wx.Colour(200,150,37),
			"blurColour" : wx.Colour(238,168,37),
			"emptyColour" : wx.Colour(255,255,255),
			"emptyFocusColour" : wx.Colour(210,210,210),
			"tipsColour" : wx.Colour(210,60,60),
			"onTurn" : None,
			"onGameOver" : None,
			"disableTips" : "禁止操作",
		};
		for k,v in params.items():
			self.__params[k] = v;

	def getCtr(self):
		return self.__viewCtr;

	def initView(self):
		self.createControls(); # 创建控件
		self.initViewLayout(); # 初始化布局

	def createControls(self):
		# self.getCtr().createCtrByKey("key", self._curPath + "***View"); # , parent = self, params = {}
		self.createChessViews();
		self.createEmptyBitmap();
		pass;
		
	def initViewLayout(self):
		rows, cols = self.getMatrix();
		gridSizer = wx.GridSizer(rows, cols, 0, 0);
		for chessView in self.__chessList:
			gridSizer.Add(chessView);
		self.SetSizerAndFit(gridSizer);
		pass;

	def updateView(self, data):
		pass;

	def setPattern(self, pattern):
		self.__pattern = pattern;

	def getPattern(self):
		return self.__pattern;

	def createEmptyBitmap(self):
		self.__emptyBitmap = ChessBitmap(ChessConst.Empty);

	def createChessViews(self):
		for chessKey, count in ChessCountConfig.items():
			for i in range(count):
				# 创建位图
				bitmap = ChessBitmap(chessKey);
				self.__bitmapList.append(bitmap);
				# 创建棋子视图
				chessCtr = CreateCtr(self._curPath + "../ChessView", self, params = {"bitmap" : bitmap});
				chessCtr.getUI().SetBackgroundColour(self.__params["emptyColour"]);
				self.__chessList.append(chessCtr.getUI());
				# 绑定点击事件
				chessCtr.setClickEvent(self.onClickItem);
				chessCtr.setDClickEvent(self.onDClickItem);
				chessCtr.setRClickEvent(self.onRClickItem);

	def randomChesses(self):
		bitmapList = copy.copy(self.__bitmapList);
		random.shuffle(bitmapList);
		for i,chessView in enumerate(self.__chessList):
			chessView.setChessBitmap(bitmapList[i]);
			self.hideItem(chessView);

	def onClickItem(self, item, event = None):
		if not self.checkOpRight():
			return;
		# 判断移动棋子，移动成功后，转换操作对象
		if self.moveItemByTips(item):
			self.turn();
		# 重置提示
		self.resetTipsItems();
		# 设置点击选中的item
		if item == self.__curItem:
			return;
		if self.__curItem:
			# 更新取消选中Item的颜色
			color = self.__params["blurColour"];
			if self.__curItem.getChessBitmap().val() == ChessConst.Empty or self.__curItem.isShownBitmap():
				color = self.__params["emptyColour"];
			self.__curItem.SetBackgroundColour(color);
			self.__curItem.Refresh();
		# 更新选中Item的颜色
		color = self.__params["focusColour"];
		if item.getChessBitmap().val() == ChessConst.Empty or item.isShownBitmap():
			color = self.__params["emptyFocusColour"];
		item.SetBackgroundColour(color);
		item.Refresh();
		self.__curItem = item;
		pass;

	def onDClickItem(self, item, event = None):
		if not self.checkOpRight():
			return;
		self.onClickItem(item, event);
		# 判断显示棋子，显示后，转换操作对象
		if not item.isShownBitmap():
			self.showItem(item);
			self.turn();
		pass;

	def onRClickItem(self, item, event = None):
		if not self.checkOpRight():
			return;
		self.resetTipsItems();
		self.onClickItem(item, event);
		if self.__curItem and self.__curItem.getChessBitmap().color() == self.__turn:
			self.checkTipsItems();
		pass;

	def clearChessBitmap(self, item):
		item.setChessBitmap(self.__emptyBitmap);
		item.SetBackgroundColour(self.__params["emptyColour"]);
		item.Refresh();

	def resetChesses(self):
		for i,chessView in enumerate(self.__chessList):
			chessView.setChessBitmap(self.__bitmapList[i]);
			self.showItem(chessView);

	def showChesses(self):
		for chessView in self.__chessList:
			self.showItem(chessView);

	def getMatrix(self):
		return self.__params["matrix"][0], self.__params["matrix"][1];

	def showItem(self, item):
		item.showBitmap();
		color = self.__params["emptyColour"];
		if item == self.__curItem:
			color = self.__params["emptyFocusColour"];
		item.SetBackgroundColour(color);
		item.Refresh();

	def hideItem(self, item):
		item.hideBitmap();
		color = self.__params["blurColour"];
		if item == self.__curItem:
			color = self.__params["focusColour"];
		item.SetBackgroundColour(color);
		item.Refresh();

	def getItem(self, row, col):
		rows, cols = self.getMatrix();
		if row < 0 or col < 0 or row >= rows or col >= cols:
			return None;
		index = row*cols + col;
		if index >= len(self.__chessList):
			return None;
		return self.__chessList[index];

	def getItemIdx(self, item):
		for i, v in enumerate(self.__chessList):
			if v == item:
				return i;
		return -1;

	def getItemMt(self, item):
		idx = self.getItemIdx(item);
		if idx >= 0:
			rows, cols = self.getMatrix();
			return math.floor(idx/cols), idx%cols;
		return -1, -1;

	def resetTipsItems(self):
		for _,info in self.__tipsInfoMap.items():
			info["item"].SetBackgroundColour(info["color"]);
			info["item"].Refresh();
		self.__tipsInfoMap = {};

	def checkTipsItems(self):
		if not self.__curItem:
			return;
		items = self.getTipsItems(self.__curItem);
		for item in items:
			if self.checkItem(item):
				self.__tipsInfoMap[item] = {"item" : item, "color" : item.GetBackgroundColour()};
				item.SetBackgroundColour(self.__params["tipsColour"]);
				item.Refresh();

	def checkItem(self, item, curItem = None):
		if not curItem:
			curItem = self.__curItem;
		if not curItem or not curItem.isShownBitmap():
			return False;
		if curItem.getChessBitmap().val() == ChessConst.Empty:
			return False;
		if not item.isShownBitmap():
			return False;
		if item.getChessBitmap().val() == ChessConst.Empty:
			return True;
		if hasattr(self, "onCheckItem"):
			return self.onCheckItem(curItem, item);
		return False;

	def getTipsItems(self):
		return [];

	def checkGameOver(self):
		# 检测棋盘上是否所有棋子都已显示，且只有一种颜色可移动
		redCnt, blackCnt = 0, 0;
		for chessView in self.__chessList:
			if not chessView.isShownBitmap():
				return False;
			if chessView.getChessBitmap().val() != ChessConst.Empty:
				# 判断可移动的次数
				isContinue = False;
				for item in self.getTipsItems(chessView):
					if self.checkItem(item, curItem = chessView):
						isContinue = True;
						break;
				if not isContinue:
					continue;
				# 获取棋子颜色的数量
				color = chessView.getChessBitmap().color();
				if color == TurnConst.Red.value:
					redCnt += 1;
				elif color == TurnConst.Black.value:
					blackCnt += 1;
		# 判断是否只有一种颜色可移动
		if redCnt * blackCnt != 0:
			return False;
		callback = self.__params["onGameOver"];
		if callable(callback):
			callback(self.__turn);
		return True;

	def turn(self, isReset = False):
		# 检测游戏是否结束
		if self.checkGameOver():
			return;
		# 更换操作对象
		firstTurn = -1;
		if isReset:
			self.__turn = -1;
			self.__firstTurn = -1;
		elif self.__turn == -1 and self.__curItem:
			firstTurn = self.__curItem.getChessBitmap().color();
			self.toggleTurn(firstTurn);
			self.__firstTurn = firstTurn;
		else:
			self.toggleTurn();
		self.onTurn(self.__params["onTurn"], firstTurn);

	def onTurn(self, callback, firstTurn):
		if callable(callback):
			if not self.checkSinglePattern():
				firstTurn = -1;
			callback(self.__turn, firstTurn);

	def toggleTurn(self, curTurn = -1):
		if curTurn == -1:
			curTurn = self.__turn;
		if curTurn == TurnConst.Black.value:
			self.__turn = TurnConst.Red.value;
		else:
			self.__turn = TurnConst.Black.value;

	def moveItemByTips(self, item):
		if item == self.__curItem:
			return False;
		if self.__curItem in self.__tipsInfoMap:
			return False;
		if item in self.__tipsInfoMap:
			bitmap = self.__curItem.getChessBitmap();
			item.setChessBitmap(bitmap);
			self.__curItem.setChessBitmap(self.__emptyBitmap);
			return True;
		return False;

	def checkOpRight(self):
		if self.checkSinglePattern():
			if self.__turn in [TurnConst.Black.value, TurnConst.Red.value]:
				if not self.checkFirstTurn():
					self.showDisableTipWin(self.__params["disableTips"]);
					return False;
		return True;

	def showDisableTipWin(self, tips):
		wx.TipWindow(self, tips);

	def checkSinglePattern(self):
		return self.__pattern == GamePattern.Single.value;

	def checkFirstTurn(self):
		return self.__turn == self.__firstTurn;

	def checkFirstColor(self, color):
		return self.__firstTurn == color;

	def getChessList(self):
		return self.__chessList;