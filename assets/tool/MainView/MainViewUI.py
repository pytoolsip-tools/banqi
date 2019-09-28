# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-10-08 21:02:23
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-09-24 11:05:41

import wx;

from _Global import _GG;
from function.base import *;

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__)); # 当前文件目录

EVENT_ID = require(GetPathByRelativePath("../config", CURRENT_PATH), "event_id", "EVENT_ID");
TurnConst = require(CURRENT_PATH + "../../config", "chess_config", "TurnConst");

class MainViewUI(wx.ScrolledWindow):
	"""docstring for MainViewUI"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None, params = {}):
		self.initParams(params);
		super(MainViewUI, self).__init__(parent, id, size = self.__params["size"]);
		self._className_ = MainViewUI.__name__;
		self._curPath = curPath;
		self.__viewCtr = viewCtr;
		self.bindEvents(); # 绑定事件
		self.SetBackgroundColour(self.__params["bgColour"]);
		# 初始化滚动条参数
		self.SetScrollbars(1, 1, *self.__params["size"]);
		# 私有变量
		self.__rule = None;

	def __del__(self):
		self.__dest__();

	def __dest__(self):
		if not hasattr(self, "_unloaded_"):
			self._unloaded_ = True;
			self.__unload__();

	def __unload__(self):
		self.unbindEvents();

	def initParams(self, params):
		# 初始化参数
		self.__params = {
			"size" : _GG("WindowObject").GetToolWinSize(),
			"style" : wx.BORDER_THEME,
			"bgColour" : wx.Colour(255,255,255),
		};
		for k,v in params.items():
			self.__params[k] = v;

	def getCtr(self):
		return self.__viewCtr;

	def bindEvents(self):
		_GG("WindowObject").BindEventToToolWinSize(self, self.onToolWinSize);

	def unbindEvents(self):
		_GG("WindowObject").UnbindEventToToolWinSize(self);

	def initView(self):
		self.createControls(); # 创建控件
		self.initViewLayout(); # 初始化布局
		self.resetScrollbars(); # 重置滚动条

	def createControls(self):
		self.getCtr().createCtrByKey("ControllerView", self._curPath + "../view/ControllerView", params = {
			"size" : (150, max(600, self.GetSize().y)),
			"startBtn" : {
				"label" : "开始游戏",
				"pauseLabel" : "暂停游戏",
				"callback" : self.onStartGame,
			},
			"stopBtn" : {
				"label" : "停止游戏",
				"callback" : self.onStopGame,
			},
			"restartBtn" : {
				"label" : "重新开始",
				"callback" : self.onRestartGame,
			},
			"rules" : {
				"list" : [
					{"key" : "normal", "name" : "通用规则", "description" : "通用翻棋规则"},
				],
				"callback" : self.onChangeRule,
			},
		}); # , parent = self, params = {}
		self.getCtr().createCtrByKey("BanQiView", self._curPath + "../view/BanQiView", params = {
			"size" : (600, max(600, self.GetSize().y)),
			"onTurn" : self.onTurn,
			"onGameOver" : self.onGameOver,
		}); # , parent = self, params = {}
		self.getCtr().createCtrByKey("TipsView", self._curPath + "../view/TipsView", params = {
			"size" : (max(200, self.GetSize().x - 750), max(600, self.GetSize().y)),
			"operate" : {
				"title" : "游戏操作提示",
				"value" : "左键单击：选中棋子。\n左键双击：翻开棋子。\n右键单击：显示棋子的可移动（红色）区域。\n其他：单击棋子的可移动（红色）区域后，可移动选中的棋子到指定区域。",
			},
		}); # , parent = self, params = {}
		pass;
		
	def initViewLayout(self):
		box = wx.BoxSizer(wx.HORIZONTAL);
		box.Add(self.getCtr().getUIByKey("ControllerView"));
		box.Add(self.getCtr().getUIByKey("BanQiView"), flag = wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT, border = 20);
		box.Add(self.getCtr().getUIByKey("TipsView"));
		self.SetSizerAndFit(box);

	def resetScrollbars(self):
		self.SetScrollbars(1, 1, self.GetSizer().GetSize().x, self.GetSizer().GetSize().y);

	def onToolWinSize(self, sizeInfo, event = None):
		self.SetSize(self.GetSize() + sizeInfo["preDiff"]);
		self.Refresh();
		self.Layout();

	def updateView(self, data):
		pass;

	def onStartGame(self, btn, event):
		if not self.isPlaying():
			_GG("EventDispatcher").dispatch(EVENT_ID.CHANGE_TURN_EVENT, {"isReset" : True});
			_GG("EventDispatcher").dispatch(EVENT_ID.START_GAME_EVENT, {"rule" : self.__rule});
		else:
			_GG("EventDispatcher").dispatch(EVENT_ID.PAUSE_GAME_EVENT, {"rule" : self.__rule});
		pass;

	def onStopGame(self, btn, event):
		if self.isPlaying():
			messageDialog = wx.MessageDialog(self, "游戏已经开始，是否确认停止游戏？", "停止游戏", style = wx.YES_NO|wx.ICON_QUESTION);
			if messageDialog.ShowModal() == wx.ID_YES:
				_GG("EventDispatcher").dispatch(EVENT_ID.CHANGE_TURN_EVENT, {"isReset" : True});
				_GG("EventDispatcher").dispatch(EVENT_ID.STOP_GAME_EVENT, {"rule" : self.__rule});

	def onRestartGame(self, btn, event):
		if self.isPlaying():
			messageDialog = wx.MessageDialog(self, "游戏已经开始，是否确认重新开始？", "重新开始游戏", style = wx.YES_NO|wx.ICON_QUESTION);
			if messageDialog.ShowModal() == wx.ID_YES:
				_GG("EventDispatcher").dispatch(EVENT_ID.CHANGE_TURN_EVENT, {"isReset" : True});
				_GG("EventDispatcher").dispatch(EVENT_ID.RESTART_GAME_EVENT, {"rule" : self.__rule});
		pass;

	def onChangeRule(self, rule):
		self.__rule = rule;
		pass;

	def onTurn(self, turn):
		text, color = "", "black";
		if turn.value == TurnConst.Black.value:
			text, color = "黑方", "black";
		elif turn.value == TurnConst.Red.value:
			text, color = "红方", "red";
		_GG("EventDispatcher").dispatch(EVENT_ID.CHANGE_TURN_EVENT, {"text" : text, "color" : color});
		pass;

	def onGameOver(self, turn):
		text = "";
		if turn.value == TurnConst.Black.value:
			text = "黑方";
		elif turn.value == TurnConst.Red.value:
			text = "红方";
		wx.MessageDialog(self, f"恭喜【{text}】获得了胜利！", "游戏结束", style = wx.YES_NO|wx.ICON_INFORMATION).ShowModal();
		_GG("EventDispatcher").dispatch(EVENT_ID.STOP_GAME_EVENT, {"rule" : self.__rule});
		pass;

	def isPlaying(self):
		return self.getCtr().getUIByKey("ControllerView").isPlaying();