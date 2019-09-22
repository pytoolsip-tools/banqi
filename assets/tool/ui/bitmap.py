# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2019-09-22 13:52:59
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-09-22 23:55:07

import wx;

from _Global import _GG;
from function.base import *;

class ChessBitmap(wx.Bitmap):
	"""docstring for ChessBitmap"""
	def __init__(self, value, size = wx.Size(-1, -1)):
		super(ChessBitmap, self).__init__(size);
		self._className_ = ChessBitmap.__name__;
		self._curPath = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/") + "/";
		self.__val = value;
		self.initBitmap();

	def initBitmap(self):
		ChessResConfig = require(self._curPath + "../config", "chess_config", "ChessResConfig");
		if self.__val in ChessResConfig:
			self.LoadFile(GetPathByRelativePath("../"+ChessResConfig[self.__val], self._curPath), wx.BITMAP_TYPE_ANY);

	def getVal(self):
		return self.__val.value;

	def getColor(self):
		return self.__val.value >> 4;

	def getPoint(self):
		return self.__val.value & 0x01;
