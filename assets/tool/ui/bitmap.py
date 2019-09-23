# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2019-09-22 13:52:59
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-09-23 11:06:06

import wx;

from _Global import _GG;
from function.base import *;

class ChessBitmap(wx.Bitmap):
	"""docstring for ChessBitmap"""
	def __init__(self, value, *argList, **argDict):
		super(ChessBitmap, self).__init__(*argList, **argDict);
		self._className_ = ChessBitmap.__name__;
		self._curPath = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/") + "/";
		self.__val = value;
		self.initBitmap();

	def initBitmap(self):
		ChessResConfig = require(self._curPath + "../config", "chess_config", "ChessResConfig");
		if self.__val in ChessResConfig:
			self.LoadFile(GetPathByRelativePath("../"+ChessResConfig[self.__val], self._curPath), wx.BITMAP_TYPE_ANY);

	def val(self):
		return self.__val;

	def value(self):
		return self.__val.value;

	def color(self):
		return self.__val.value >> 4;

	def point(self):
		return self.__val.value & 0x01;
