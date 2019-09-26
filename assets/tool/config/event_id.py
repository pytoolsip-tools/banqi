# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2019-01-23 18:27:11
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-09-24 10:45:02

from enum import Enum, unique;

from _Global import _GG;

# 枚举事件Id
@unique
class EVENT_ID(Enum):
	START_GAME_EVENT = _GG("EVENT_ID").getNewId(); # 开始游戏

	PAUSE_GAME_EVENT = _GG("EVENT_ID").getNewId(); # 暂停游戏

	STOP_GAME_EVENT = _GG("EVENT_ID").getNewId(); # 停止游戏

	RESTART_GAME_EVENT = _GG("EVENT_ID").getNewId(); # 重新开始游戏

	CHANGE_TURN_EVENT = _GG("EVENT_ID").getNewId(); # 变更操作方