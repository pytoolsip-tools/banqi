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
GamePattern = require(CURRENT_PATH + "../../config", "chess_config", "GamePattern");
RuleCost = require(CURRENT_PATH + "../../config", "chess_config", "RuleCost");

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
					{"key" : "通用规则", "value" : RuleCost.Normal.value, "description" : """
  通用翻棋规则。

  棋子大小排序为【帥 = 將 > 仕 = 士 > 相 = 象 > 俥 = 車 > 傌 = 馬 > 炮 = 砲 > 兵 = 卒】，大棋子可以吃小棋子；特殊的是，【兵】可以吃【將】，【卒】可以吃【帥】。

  玩家每次只能操作一步，如翻开棋子或移动棋子或吃对方的棋子。""",
					},
				],
				"pattern" : [
					{"key" : "单人模式", "value" : GamePattern.Single.value},
					{"key" : "多人模式", "value" : GamePattern.Multiple.value},
				],
				"callback" : self.onChangeRule,
				"patternCallback" : self.onChangePattern,
			},
		}); # , parent = self, params = {}
		self.getCtr().createCtrByKey("BanQiView", self._curPath + "../view/BanQiView", params = {
			"size" : (600, max(600, self.GetSize().y)),
			"onTurn" : self.onTurn,
			"onGameOver" : self.onGameOver,
			"disableTips" : "您不是当前操作方，不能进行操作！",
		}); # , parent = self, params = {}
		self.getCtr().createCtrByKey("TipsView", self._curPath + "../view/TipsView", params = {
			"size" : (max(200, self.GetSize().x - 750), max(600, self.GetSize().y)),
			"operate" : {
				"title" : "游戏操作提示",
				"value" : """
  左键单击：选中棋子。

  左键双击：翻开棋子。

  右键单击：显示棋子的可移动（红色）区域。
  
  其他：单击棋子的可移动（红色）区域后，可移动选中的棋子到指定区域。""",
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
			_GG("EventDispatcher").dispatch(EVENT_ID.START_GAME_EVENT, {});
		else:
			_GG("EventDispatcher").dispatch(EVENT_ID.PAUSE_GAME_EVENT, {});
		pass;

	def onStopGame(self, btn, event):
		if self.isPlaying():
			messageDialog = wx.MessageDialog(self, "游戏已经开始，是否确认停止游戏？", "停止游戏", style = wx.YES_NO|wx.ICON_QUESTION);
			if messageDialog.ShowModal() == wx.ID_YES:
				_GG("EventDispatcher").dispatch(EVENT_ID.CHANGE_TURN_EVENT, {"isReset" : True});
				_GG("EventDispatcher").dispatch(EVENT_ID.STOP_GAME_EVENT, {});

	def onRestartGame(self, btn, event):
		if self.isPlaying():
			messageDialog = wx.MessageDialog(self, "游戏已经开始，是否确认重新开始？", "重新开始游戏", style = wx.YES_NO|wx.ICON_QUESTION);
			if messageDialog.ShowModal() == wx.ID_YES:
				_GG("EventDispatcher").dispatch(EVENT_ID.CHANGE_TURN_EVENT, {"isReset" : True});
				_GG("EventDispatcher").dispatch(EVENT_ID.RESTART_GAME_EVENT, {});
		pass;

	def onChangeRule(self, rule):
		banQiViewCtr = self.getCtr().getCtrByKey("BanQiView");
		banQiViewCtr.unbindBehaviors();
		if rule["value"] == RuleCost.Normal.value:
			banQiViewCtr.bindBehaviors([
				{"path" : "behavior/NormalRuleBehavior", "basePath" : GetPathByRelativePath("../", self._curPath)},
			]);
			# 判断是否为单人模式
			if banQiViewCtr.getPattern() == GamePattern.Single.value:
				banQiViewCtr.bindBehaviors([
					{"path" : "behavior/NormalAIBehavior", "basePath" : GetPathByRelativePath("../", self._curPath)},
				]);
		pass;

	def onChangePattern(self, pattern):
		self.getCtr().getCtrByKey("BanQiView").setPattern(pattern["value"]);
		pass;

	def getTextColorByTurn(self, turn):
		text, color = "", "";
		if turn == TurnConst.Black.value:
			text, color = "黑方", "black";
		elif turn == TurnConst.Red.value:
			text, color = "红方", "red";
		return text, color;

	def onTurn(self, turn, firstTurn):
		# 更新阵营提示
		if firstTurn in [TurnConst.Black.value, TurnConst.Red.value]:
			yourText, yourColor = self.getTextColorByTurn(firstTurn);
			_GG("EventDispatcher").dispatch(EVENT_ID.CHANGE_TURN_EVENT, {"key" : "updateYourTurn", "text" : yourText, "color" : yourColor});
		# 更新操作方
		text, color = "You First", "black";
		if turn != None:
			if turn == TurnConst.Black.value:
				text, color = "黑方", "black";
			elif turn == TurnConst.Red.value:
				text, color = "红方", "red";
		_GG("EventDispatcher").dispatch(EVENT_ID.CHANGE_TURN_EVENT, {"text" : text, "color" : color});
		pass;

	def onGameOver(self, turn):
		text = "";
		if turn == TurnConst.Black.value:
			text = "黑方";
		elif turn == TurnConst.Red.value:
			text = "红方";
		wx.MessageDialog(self, f"恭喜【{text}】获得了胜利！", "游戏结束", style = wx.YES_NO|wx.ICON_INFORMATION).ShowModal();
		_GG("EventDispatcher").dispatch(EVENT_ID.STOP_GAME_EVENT, {});
		pass;

	def isPlaying(self):
		return self.getCtr().getUIByKey("ControllerView").isPlaying();