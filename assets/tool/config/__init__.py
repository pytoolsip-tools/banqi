import os;
import sys;

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__));
sys.path.append(CURRENT_PATH);

__all__ = ["TOOL_INFO", "ChessConst", "ChessCountConfig", "ChessResConfig"];

try:
	# 工具信息
	TOOL_INFO = {};
	toolPath = os.apth.join(CURRENT_PATH, "../tool.json");
	if os.path.exists(toolPath):
		with open(toolPath, "r") as f:
			TOOL_INFO = json.loads(f.read());

	# 游戏常量
	from config.chess_const import ChessConst;

	# 游戏配置
	from config.chess_config import ChessCountConfig, ChessResConfig;

except Exception as e:
	raise e;
finally:
	sys.path.remove(CURRENT_PATH);