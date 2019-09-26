# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2019-09-21 22:30:18
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-09-24 11:02:05

import wx;

from _Global import _GG;
from function.base import *;

class ControllerViewUI(wx.Panel):
	"""docstring for ControllerViewUI"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None, params = {}):
		self.initParams(params);
		super(ControllerViewUI, self).__init__(parent, id, pos = self.__params["pos"], size = self.__params["size"], style = self.__params["style"]);
		self._className_ = ControllerViewUI.__name__;
		self._curPath = curPath;
		self.__viewCtr = viewCtr;

	def initParams(self, params):
		# 初始化参数
		self.__params = {
			"pos" : (0,0),
			"size" : (-1,-1),
			"style" : wx.BORDER_THEME,
			"startBtn" : {
				"label" : "开始游戏",
			},
			"stopBtn" : {
				"label" : "停止游戏",
			},
			"restartBtn" : {
				"label" : "重新开始",
			},
			"rules" : {
				"list" : [
					{"key" : "normal", "name" : "通用规则", "description" : "通用翻棋规则"},
				],
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
		# self.getCtr().createCtrByKey("key", self._curPath + "***View"); # , parent = self, params = {}
		self.createControlBtns();
		self.createRuleSelector();
		pass;
		
	def initViewLayout(self):
		box = wx.BoxSizer(wx.VERTICAL);
		box.Add(self.__btnPanel, flag = wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border = 10);
		box.Add(self.__ruleSelector, flag = wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border = 10);
		self.SetSizer(box);
		totalHeight = self.__btnPanel.GetSize().y + self.__ruleSelector.GetSize().y;
		if self.GetSize().y < totalHeight:
			self.Fit();
		pass;

	def updateView(self, data):
		pass;

	def createControlBtns(self):
		self.__btnPanel = wx.Panel(self, size = (self.GetSize().x, -1), style = wx.BORDER_THEME);
		staticText = wx.StaticText(self.__btnPanel, label = "游戏控制器");
		staticText.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, underline=True));
		# 开始游戏按钮
		startGameBtn = wx.Button(self.__btnPanel, label = self.__params["startBtn"]["label"]);
		def onStartGame(event):
			callback = self.__params["startBtn"].get("callback", None);
			if callable(callback):
				callback(startGameBtn, event);
		startGameBtn.Bind(wx.EVT_BUTTON, onStartGame);
		# 停止游戏按钮
		stopGameBtn = wx.Button(self.__btnPanel, label = self.__params["stopBtn"]["label"]);
		def onStartGame(event):
			callback = self.__params["stopBtn"].get("callback", None);
			if callable(callback):
				callback(stopGameBtn, event);
		stopGameBtn.Bind(wx.EVT_BUTTON, onStartGame);
		# 重新开始游戏按钮
		restartGameBtn = wx.Button(self.__btnPanel, label = self.__params["restartBtn"]["label"]);
		def onRestartGame(event):
			callback = self.__params["restartBtn"].get("callback", None);
			if callable(callback):
				callback(startGameBtn, restartGameBtn, event);
		restartGameBtn.Bind(wx.EVT_BUTTON, onRestartGame);
		# 初始化布局
		box = wx.BoxSizer(wx.VERTICAL);
		box.Add(staticText, flag = wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border = 10);
		box.Add(startGameBtn, flag = wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border = 5);
		box.Add(stopGameBtn, flag = wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border = 5);
		box.Add(restartGameBtn, flag = wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border = 5);
		self.__btnPanel.SetSizer(box);

	def createRuleSelector(self):
		self.__ruleSelector = wx.Panel(self, size = (self.GetSize().x, -1), style = wx.BORDER_THEME);
		staticText = wx.StaticText(self.__ruleSelector, label = "游戏规则");
		staticText.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, underline=True));
		textCtrl = wx.TextCtrl(self.__ruleSelector, size = (self.GetSize().x, 300), style = wx.TE_MULTILINE|wx.TE_READONLY);
		# 创建选择框
		rulesParams = self.__params["rules"];
		choices = [];
		for rule in rulesParams["list"]:
			choices.append(rule["name"]);
		choiceCtrl = wx.Choice(self.__ruleSelector, choices = choices);
		def onChoice(ctrl):
			selectStr = ctrl.GetStringSelection();
			for rule in rulesParams["list"]:
				if rule["name"] == selectStr:
					textCtrl.SetValue(rule["description"]);
					# 执行回调
					callback = rulesParams.get("callback", None);
					if callable(callback):
						callback(rule);
		if len(choices) > 0:
			choiceCtrl.Selection = 0;
			onChoice(choiceCtrl);
		def onChangeChoice(event):
			onChoice(event.GetEventObject());
			pass;
		choiceCtrl.Bind(wx.EVT_CHOICE, onChangeChoice);
		# 初始化布局
		box = wx.BoxSizer(wx.VERTICAL);
		box.Add(staticText, flag = wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border = 10);
		box.Add(choiceCtrl, flag = wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border = 5);
		box.Add(textCtrl, flag = wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border = 5);
		self.__ruleSelector.SetSizerAndFit(box);
		self.__choiceCtrl = choiceCtrl;

	def enableChoiceCtrl(self, enable=True):
		self.__choiceCtrl.Enable(enable = enable);