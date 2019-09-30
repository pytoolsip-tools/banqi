# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2019-09-21 21:27:25
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-09-22 23:56:06

from enum import Enum, unique;

@unique
class RuleCost(Enum):
	Normal		= 0; # 通用规则

@unique
class GamePattern(Enum):
	Single		= 0; # 单人模式
	Multiple	= 1; # 多人模式

@unique
class TurnConst(Enum):
	Black	= 0; # 黑方
	Red		= 1; # 红方

@unique
class ChessConst(Enum):
	Empty		= 0x00; # 空
	# 黑色棋子
	B_Soldier	= 0x01; # 卒
	B_Cannon 	= 0x02; # 砲
	B_Horse 	= 0x03; # 馬
	B_Chariot	= 0x04; # 車
	B_Elephant	= 0x05; # 象
	B_Advisor 	= 0x06; # 士
	B_General	= 0x07; # 將
	# 红色棋子
	R_Soldier	= 0x11; # 兵
	R_Cannon	= 0x12; # 炮
	R_Horse 	= 0x13; # 傌
	R_Chariot	= 0x14; # 俥
	R_Elephant	= 0x15; # 相
	R_Advisor 	= 0x16; # 仕
	R_General	= 0x17; # 帥


# 棋子数量配置
ChessCountConfig = {
	ChessConst.B_Soldier	: 5, # 卒
	ChessConst.B_Cannon		: 2, # 砲
	ChessConst.B_Horse		: 2, # 馬
	ChessConst.B_Chariot	: 2, # 車
	ChessConst.B_Elephant	: 2, # 象
	ChessConst.B_Advisor 	: 2, # 士
	ChessConst.B_General	: 1, # 將
	ChessConst.R_Soldier	: 5, # 兵
	ChessConst.R_Cannon		: 2, # 炮
	ChessConst.R_Horse		: 2, # 傌
	ChessConst.R_Chariot	: 2, # 俥
	ChessConst.R_Elephant	: 2, # 相
	ChessConst.R_Advisor 	: 2, # 仕
	ChessConst.R_General	: 1, # 帥
};

# 棋子资源配置
ChessResConfig = {
	ChessConst.B_Soldier.value	: "res/b_soldier.png", # 卒
	ChessConst.B_Cannon.value	: "res/b_cannon.png", # 砲
	ChessConst.B_Horse.value	: "res/b_horse.png", # 馬
	ChessConst.B_Chariot.value	: "res/b_chariot.png", # 車
	ChessConst.B_Elephant.value	: "res/b_elephant.png", # 象
	ChessConst.B_Advisor.value 	: "res/b_advisor.png", # 士
	ChessConst.B_General.value	: "res/b_general.png", # 將
	ChessConst.R_Soldier.value	: "res/r_soldier.png", # 兵
	ChessConst.R_Cannon.value	: "res/r_cannon.png", # 炮
	ChessConst.R_Horse.value	: "res/r_horse.png", # 傌
	ChessConst.R_Chariot.value	: "res/r_chariot.png", # 俥
	ChessConst.R_Elephant.value	: "res/r_elephant.png", # 相
	ChessConst.R_Advisor.value 	: "res/r_advisor.png", # 仕
	ChessConst.R_General.value	: "res/r_general.png", # 帥
};