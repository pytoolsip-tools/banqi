# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-12-22 09:09:43
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-09-24 10:53:40

import wx;
import math;
from datetime import datetime;

from _Global import _GG;
from function.base import *;

class TimingViewUI(wx.Panel):
	"""docstring for TimingViewUI"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None, params = {}):
		self.initParams(params);
		super(TimingViewUI, self).__init__(parent, id, pos = self.__params["pos"], size = self.__params["size"], style = self.__params["style"]);
		self._className_ = TimingViewUI.__name__;
		self._curPath = curPath;
		self.__viewCtr = viewCtr;
		self.__startTime = None;
		self.__pauseTime = None;
		self.__timer = None;
		self.createTimer(); # 创建定时器
		self.SetBackgroundColour(self.__params["bgColour"]);

	def __del__(self):
		self.__dest__();

	def __dest__(self):
		if not hasattr(self, "_unloaded_"):
			self._unloaded_ = True;
			self.__unload__();

	def __unload__(self):
		self.stopAllTimer(isDestroy = True); # 停止定时器

	def initParams(self, params):
		# 初始化参数
		self.__params = {
			"pos" : (0,0),
			"size" : (-1,-1),
			"style" : wx.BORDER_THEME,
			"bgColour" : wx.Colour(255,255,255),
			"title" : "时间进度",
			"onTimer" : None,
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
		self.createTitleText();
		self.createTimingText();
		pass;
		
	def initViewLayout(self):
		box = wx.BoxSizer(wx.VERTICAL);
		box.Add(self.__title, flag = wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border = 10);
		box.Add(self.__timingText, flag = wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border = 5);
		self.SetSizer(box);

	def updateView(self, data):
		pass;

	def createTitleText(self):
		self.__title = wx.StaticText(self, label = self.__params["title"]);
		self.__title.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, underline=True));

	def restartTime(self):
		self.__startTime = datetime.now();

	def createTimer(self):
		self.__timer = _GG("TimerManager").createTimer(self, callback = self.onTimerEvent);

	def stopAllTimer(self, isDestroy = False):
		if self.__timer and self.__timer.IsRunning():
			self.__timer.Stop();
			if isDestroy:
				_GG("TimerManager").deleteTimer(self.__timer);

	def onTimerEvent(self, event = None):
		if self.__startTime:
			diffDataTime = datetime.now() - self.__startTime;
			days, diffSeconds = diffDataTime.days, diffDataTime.seconds;
			hours = math.floor(diffSeconds / (60 * 60)) % 24;
			minutes = math.floor(diffSeconds / 60) % 60;
			seconds = diffSeconds % 60;
			if days > 0:
				self.__timingText.SetLabel("{}D ".format(days) + ":".join(["%02d"%hours, "%02d"%minutes, "%02d"%seconds]));
			else:
				self.__timingText.SetLabel(":".join(["%02d"%hours, "%02d"%minutes, "%02d"%seconds]));
			# 回调函数
			if callable(self.__params.get("onTimer", None)):
				self.__params["onTimer"](diffSeconds);

	def createTimingText(self):
		self.__timingText = wx.StaticText(self, label = "--:--:--");

	def resetTimingText(self):
		self.__timingText.SetLabel("--:--:--");

	def startTimer(self, isReset = False):
		if isReset or not self.__startTime:
			self.restartTime();
			self.__pauseTime = None;
		else:
			if self.__pauseTime:
				self.__startTime += datetime.now() - self.__pauseTime;
		self.onTimerEvent();
		if self.__timer and not self.__timer.IsRunning():
			self.__timer.Start(1000);

	def stopTimer(self, isReset = False):
		if self.__timer and self.__timer.IsRunning():
			self.__timer.Stop();
		if not isReset:
			self.__pauseTime = datetime.now();
		else:
			self.__startTime = None;
			self.__pauseTime = None;
			self.resetTimingText();