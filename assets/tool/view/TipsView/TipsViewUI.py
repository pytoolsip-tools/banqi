# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2019-09-21 22:34:20
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-09-22 12:24:50

import wx;

from _Global import _GG;
from function.base import *;

class TipsViewUI(wx.Panel):
	"""docstring for TipsViewUI"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None, params = {}):
		self.initParams(params);
		super(TipsViewUI, self).__init__(parent, id, pos = self.__params["pos"], size = self.__params["size"], style = self.__params["style"]);
		self._className_ = TipsViewUI.__name__;
		self._curPath = curPath;
		self.__viewCtr = viewCtr;

	def initParams(self, params):
		# 初始化参数
		self.__params = {
			"pos" : (0,0),
			"size" : (-1,-1),
			"style" : wx.BORDER_THEME,
		};
		for k,v in params.items():
			self.__params[k] = v;

	def getCtr(self):
		return self.__viewCtr;

	def initView(self):
		self.createControls(); # 创建控件
		self.initViewLayout(); # 初始化布局

	def createControls(self):
		self.createTurnTips();
		self.getCtr().createCtrByKey("TimingView", self._curPath + "../TimingView", params = {
			"size" : (self.GetSize().x, -1),
		}); # , parent = self, params = {}
		pass;
		
	def initViewLayout(self):
		box = wx.BoxSizer(wx.VERTICAL);
		box.Add(self.__turnTips, flag = wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border = 10);
		box.Add(self.getCtr().getUIByKey("TimingView"), flag = wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border = 10);
		self.SetSizer(box);
		totalHeight = self.__turnTips.GetSize().y + self.getCtr().getUIByKey("TimingView").GetSize().y;
		if self.GetSize().y < totalHeight:
			self.Fit();
		pass;

	def updateView(self, data):
		pass;

	def createTurnTips(self):
		self.__turnTips = wx.Panel(self, size = (self.GetSize().x, -1), style = wx.BORDER_THEME);
		title = wx.StaticText(self.__turnTips, label = "当前操作方");
		title.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, underline=True));
		self.__turnObj = wx.StaticText(self.__turnTips, label = "黑方");
		self.__turnObj.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD));
		self.__turnObj.SetForegroundColour("black");
		# 初始化布局
		box = wx.BoxSizer(wx.VERTICAL);
		box.Add(title, flag = wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border = 10);
		box.Add(self.__turnObj, flag = wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border = 5);
		self.__turnTips.SetSizer(box);
		pass;

	def changeTurnTips(self, text, color):
		self.__turnObj.SetLabel(f"- {text} -");
		self.__turnObj.SetForegroundColour(color);
		self.__turnObj.Refresh();
		pass;