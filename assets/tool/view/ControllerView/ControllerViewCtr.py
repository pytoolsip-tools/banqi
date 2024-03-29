# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2019-09-21 22:30:18
# @Last Modified by:   JimZhang
# @Last Modified time: 2019-09-21 22:30:18
import os;
import wx;

from _Global import _GG;

from ControllerViewUI import *;

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__)); # 当前文件目录

EVENT_ID = require(GetPathByRelativePath("../../config", CURRENT_PATH), "event_id", "EVENT_ID");

def getRegisterEventMap(G_EVENT):
	return {
		EVENT_ID.START_GAME_EVENT : "startGame",
		EVENT_ID.PAUSE_GAME_EVENT : "pauseGame",
		EVENT_ID.STOP_GAME_EVENT : "stopGame",
		EVENT_ID.RESTART_GAME_EVENT : "restartGame",
	};

class ControllerViewCtr(object):
	"""docstring for ControllerViewCtr"""
	def __init__(self, parent, params = {}):
		super(ControllerViewCtr, self).__init__();
		self._className_ = ControllerViewCtr.__name__;
		self._curPath = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/") + "/";
		self.__CtrMap = {}; # 所创建的控制器
		self.initUI(parent, params); # 初始化视图UI
		self.registerEventMap(); # 注册事件
		self.bindBehaviors(); # 绑定组件

	def __del__(self):
		self.__dest__();

	def __dest__(self):
		if not hasattr(self, "_unloaded_"):
			self._unloaded_ = True;
			self.__unload__();

	def __unload__(self):
		self.unregisterEventMap(); # 注销事件
		self.unbindBehaviors(); # 解绑组件
		self.delCtrMap(); # 銷毀控制器列表

	def delCtrMap(self):
		for key in self.__CtrMap:
			DelCtr(self.__CtrMap[key]);
		self.__CtrMap.clear();

	def initUI(self, parent, params):
		# 创建视图UI类
		self.__ui = ControllerViewUI(parent, curPath = self._curPath, viewCtr = self, params = params);
		self.__ui.initView();

	def getUI(self):
		return self.__ui;

	"""
		key : 索引所创建控制类的key值
		path : 所创建控制类的路径
		parent : 所创建控制类的UI的父节点，默认为本UI
		params : 扩展参数
	"""
	def createCtrByKey(self, key, path, parent = None, params = {}):
		if not parent:
			parent = self.getUI();
		self.__CtrMap[key] = CreateCtr(path, parent, params = params);

	def getCtrByKey(self, key):
		return self.__CtrMap.get(key, None);

	def getUIByKey(self, key):
		ctr = self.getCtrByKey(key);
		if ctr:
			return ctr.getUI();
		return None;
		
	def registerEventMap(self):
		eventMap = getRegisterEventMap(_GG("EVENT_ID"));
		for eventId, callbackName in eventMap.items():
			_GG("EventDispatcher").register(eventId, self, callbackName);

	def unregisterEventMap(self):
		eventMap = getRegisterEventMap(_GG("EVENT_ID"));
		for eventId, callbackName in eventMap.items():
			_GG("EventDispatcher").unregister(eventId, self, callbackName);

	def bindBehaviors(self):
		pass;
		
	def unbindBehaviors(self):
		pass;
			
	def updateView(self, data):
		self.__ui.updateView(data);

	def startGame(self, data):
		self.__ui.play(True);

	def pauseGame(self, data):
		self.__ui.pause();

	def stopGame(self, data):
		self.__ui.play(False);

	def restartGame(self, data):
		self.__ui.play(True);