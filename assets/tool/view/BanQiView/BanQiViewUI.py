# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2019-09-21 22:41:03
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-09-22 23:35:27

import wx;
import copy;
import random;

from _Global import _GG;
from function.base import *;

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
		self.__curItem = None;
		self.__emptyBitmap = None;

	def initParams(self, params):
		# 初始化参数
		self.__params = {
			"pos" : (0,0),
			"size" : (-1,-1),
			"style" : wx.BORDER_THEME,
			"matrix" : (4,8),
			"bgColour" : wx.Colour(238,168,37),
			"focusColour" : wx.Colour(240,200,37),
			"emptyColour" : wx.Colour(255,255,255),
		};
		for k,v in params.items():
			self.__params[k] = v;

	def getCtr(self):
		return self.__viewCtr;

	def initView(self):
		self.createControls(); # 创建控件
		self.initViewLayout(); # 初始化布局
		self.randomChess();

	def createControls(self):
		# self.getCtr().createCtrByKey("key", self._curPath + "***View"); # , parent = self, params = {}
		self.createChessViews();
		self.createEmptyBitmap();
		pass;
		
	def initViewLayout(self):
		gridSizer = wx.GridSizer(self.__params["matrix"][0], self.__params["matrix"][1], 0,0);
		for chessView in self.__chessList:
			gridSizer.Add(chessView);
		self.SetSizerAndFit(gridSizer);
		pass;

	def updateView(self, data):
		pass;

	def createEmptyBitmap(self):
		size = wx.Size(-1, -1);
		if len(self.__chessList) > 0:
			size = self.__chessList[0].GetSize();
		self.__emptyBitmap = wx.Bitmap(size);

	def createChessViews(self):
		ChessCountConfig = require(self._curPath + "../../config", "chess_config", "ChessCountConfig");
		ChessBitmap = require(self._curPath + "../../ui", "bitmap", "ChessBitmap");
		for chessKey, count in ChessCountConfig.items():
			for i in range(count):
				# 创建位图
				bitmap = ChessBitmap(chessKey);
				self.__bitmapList.append(bitmap);
				# 创建棋子视图
				chessCtr = CreateCtr(self._curPath + "../ChessView", self, params = {"bitmap" : bitmap});
				chessCtr.getUI().SetBackgroundColour(self.__params["bgColour"]);
				self.__chessList.append(chessCtr.getUI());

	def randomChess(self):
		bitmapList = copy.copy(self.__bitmapList);
		random.shuffle(bitmapList);
		for i,chessView in enumerate(self.__chessList):
				chessView.setBitmap(bitmapList[i]);
