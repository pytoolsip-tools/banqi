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
		self.__turn = None;
		self.__curItem = None;
		self.__emptyBitmap = None;
		self.__tipsInfoMap = {};

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
			"emptyFocusColour" : wx.Colour(230,230,230),
			"tipsColour" : wx.Colour(210,60,60),
			"turnCallback" : None,
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
				chessCtr.getUI().SetBackgroundColour(self.__params["blurColour"]);
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
			chessView.hideBitmap();

	def onClickItem(self, item, event):
		self.resetTipsItems();
		# 设置点击选中的item
		if item == self.__curItem:
			return;
		if self.__curItem:
			# 更新取消选中Item的颜色
			color = self.__params["blurColour"];
			if self.__curItem.getChessBitmap().val() == ChessConst.Empty:
				color = self.__params["emptyColour"];
			self.__curItem.SetBackgroundColour(color);
			self.__curItem.Refresh();
		# 更新选中Item的颜色
		color = self.__params["focusColour"];
		if item.getChessBitmap().val() == ChessConst.Empty:
			color = self.__params["emptyFocusColour"];
		item.SetBackgroundColour(color);
		item.Refresh();
		self.__curItem = item;
		pass;

	def onDClickItem(self, item, event):
		self.onClickItem(item, event);
		item.showBitmap();
		pass;

	def onRClickItem(self, item, event):
		self.onClickItem(item, event);
		self.checkTipsItems();
		pass;

	def clearChessBitmap(self, item):
		item.setChessBitmap(self.__emptyBitmap);
		item.SetBackgroundColour(self.__params["emptyColour"]);
		item.Refresh();

	def resetChesses(self):
		for i,chessView in enumerate(self.__chessList):
			chessView.setChessBitmap(self.__bitmapList[i]);
			chessView.showBitmap();

	def getMatrix(self):
		return self.__params["matrix"][0], self.__params["matrix"][1];

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
		if hasattr(self, "getTipsItems"):
			items = self.getTipsItems(self.__curItem);
			for item in items:
				if self.checkItem(item):
					self.__tipsInfoMap[item] = {"item" : item, "color" : item.GetBackgroundColour()};
					item.SetBackgroundColour(self.__params["tipsColour"]);
					item.Refresh();

	def checkItem(self, item):
		if not self.__curItem or not self.__curItem.isShownBitmap():
			return False;
		if self.__curItem.getChessBitmap().val() == ChessConst.Empty:
			return False;
		if not item.isShownBitmap():
			return False;
		if item.getChessBitmap().val() == ChessConst.Empty:
			return True;
		if hasattr(self, "onCheckItem"):
			return self.onCheckItem(self.__curItem, item);
		return False;

	def getTipsItems(self):
		return [];

	def turn(self, isRandom = False):
		turnList = [TurnConst.Black, TurnConst.Red];
		if self.__turn not in turnList or isRandom:
			self.__turn = random.choice(turnList);
		else:
			if self.__turn == TurnConst.Black:
				self.__turn = TurnConst.Red;
			else:
				self.__turn = TurnConst.Black;
		callback = self.__params["turnCallback"];
		if callable(callback):
			callback(self.__turn);