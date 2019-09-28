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
			"turnTitle" : "当前操作方",
			"operate" : {
				"title" : "",
				"value" : "",
			},
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
		self.createOperateTips();
		pass;
		
	def initViewLayout(self):
		box = wx.BoxSizer(wx.VERTICAL);
		box.Add(self.__turnTips, flag = wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border = 10);
		box.Add(self.getCtr().getUIByKey("TimingView"), flag = wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border = 10);
		box.Add(self.__operateTips, flag = wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border = 10);
		self.SetSizer(box);
		totalHeight = self.__turnTips.GetSize().y + self.getCtr().getUIByKey("TimingView").GetSize().y + self.__operateTips.GetSize().y;
		if self.GetSize().y < totalHeight:
			self.Fit();
		pass;

	def updateView(self, data):
		pass;

	def createTurnTips(self):
		self.__turnTips = wx.Panel(self, size = (self.GetSize().x, -1), style = wx.BORDER_THEME);
		title = wx.StaticText(self.__turnTips, label = self.__params["turnTitle"]);
		title.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, underline=True));
		self.__turnObj = wx.StaticText(self.__turnTips, label = "-  -");
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
		self.GetSizer().Layout();
		pass;

	def createOperateTips(self):
		opParams = self.__params["operate"];
		self.__operateTips = wx.Panel(self, size = (self.GetSize().x, -1), style = wx.BORDER_THEME);
		title = wx.StaticText(self.__operateTips, label = opParams.get("title", ""));
		title.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, underline=True));
		textCtrl = wx.TextCtrl(self.__operateTips, size = (self.GetSize().x, 300), value = opParams.get("value", ""), style = wx.TE_MULTILINE|wx.TE_READONLY);
		# 初始化布局
		box = wx.BoxSizer(wx.VERTICAL);
		box.Add(title, flag = wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border = 10);
		box.Add(textCtrl, flag = wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border = 5);
		self.__operateTips.SetSizer(box);
		pass;