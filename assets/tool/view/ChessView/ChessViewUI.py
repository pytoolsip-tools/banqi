# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2019-09-21 22:49:39
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-09-22 23:54:12

import wx;

from _Global import _GG;
from function.base import *;

class ChessViewUI(wx.Panel):
	"""docstring for ChessViewUI"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None, params = {}):
		self.initParams(params);
		super(ChessViewUI, self).__init__(parent, id, pos = self.__params["pos"], size = self.__params["size"], style = self.__params["style"]);
		self._className_ = ChessViewUI.__name__;
		self._curPath = curPath;
		self.__viewCtr = viewCtr;
		self.__bitmap = None;

	def initParams(self, params):
		# 初始化参数
		self.__params = {
			"pos" : (0,0),
			"size" : (-1,-1),
			"style" : wx.BORDER_THEME,
			"bitmap" : None,
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
		self.createBitmap();
		pass;
		
	def initViewLayout(self):
		box = wx.BoxSizer(wx.VERTICAL);
		box.Add(self.__bitmap);
		self.SetSizerAndFit(box);
		pass;

	def updateView(self, data):
		pass;

	def createBitmap(self):
		self.__bitmap = wx.StaticBitmap(self, bitmap = self.__params["bitmap"]);

	def setBitmap(self, bitmap):
		self.__bitmap.SetBitmap(bitmap);

	def getBitmap(self):
		return self.__bitmap.GetBitmap();

	def bitmap(self):
		return self.__bitmap;

	def getParams(self, key = None):
		if not key:
			return self.__params;
		return self.__params.get(key, None);

	def hideBitmap(self):
		return self.__bitmap.Hide();

	def showBitmap(self):
		return self.__bitmap.Show();