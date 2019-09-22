# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2019-09-21 22:49:39
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-09-22 21:37:55
import os;
import wx;

from _Global import _GG;

from ChessViewUI import *;

def getRegisterEventMap(G_EVENT):
	return {
		# G_EVENT.TO_UPDATE_VIEW : "updateView",
	};

class ChessViewCtr(object):
	"""docstring for ChessViewCtr"""
	def __init__(self, parent, params = {}):
		super(ChessViewCtr, self).__init__();
		self._className_ = ChessViewCtr.__name__;
		self._curPath = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/") + "/";
		self.__CtrMap = {}; # 所创建的控制器
		self.initUI(parent, params); # 初始化视图UI
		self.registerEventMap(); # 注册事件
		self.bindBehaviors(); # 绑定组件
		self.initClickEvents(); # 初始化点击事件

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
		self.__ui = ChessViewUI(parent, curPath = self._curPath, viewCtr = self, params = params);
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

	def initClickEvents(self):
		self.__clickEvent = None; # 单击事件
		self.__dClickEvent = None; # 双击事件
		self.__rClickEvent = None; # 右击事件
		# 绑定单击事件
		def onClick(event):
			if callable(self.__clickEvent):
				self.__clickEvent(self, event);
		self.__ui.Bind(wx.EVT_LEFT_DOWN, onClick);
		self.__ui.bitmap().Bind(wx.EVT_LEFT_DOWN, onClick);
		# 绑定双击事件
		def onDClick(event):
			if callable(self.__dClickEvent):
				self.__dClickEvent(self, event);
		self.__ui.Bind(wx.EVT_LEFT_DCLICK, onDClick);
		self.__ui.bitmap().Bind(wx.EVT_LEFT_DCLICK, onDClick);
		# 绑定双击事件
		def onRClick(event):
			if callable(self.__rClickEvent):
				self.__rClickEvent(self, event);
		self.__ui.Bind(wx.EVT_RIGHT_DOWN, onRClick);
		self.__ui.bitmap().Bind(wx.EVT_RIGHT_DOWN, onRClick);

	def setBitmap(self):
		return self.__ui.setBitmap();

	def getBitmap(self):
		return self.__ui.getBitmap();

	def getVal(self):
		return self.__ui.val();

	def getColor(self):
		return self.__ui.val() >> 4;

	def getPoint(self):
		return self.__ui.val() & 0x01;

	def setClickEvent(self, event):
		self.__clickEvent = event;

	def setDClickEvent(self, event):
		self.__dClickEvent = event;

	def setRClickEvent(self, event):
		self.__rClickEvent = event;