# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2019-01-23 18:29:12
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-09-23 23:26:42
import os;

from _Global import _GG;
from function.base import *;

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__)); # 当前文件目录

EventId = require(GetPathByRelativePath("config", CURRENT_PATH), "event_id", "EVENT_ID");

# 更新/添加配置
_GG("EventDispatcher").updateEventIds();
