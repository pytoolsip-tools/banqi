import os;

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__));

all = ["TOOL_INFO", "ChessConst", "ChessCountConfig", "ChessResConfig"];

# 工具信息
TOOL_INFO = {};
def initToolInfo():
    toolPath = os.apth.join(CURRENT_PATH, "../tool.json");
    if os.path.exists(toolPath):
        with open(toolPath, "r") as f:
            TOOL_INFO = json.loads(f.read());
initToolInfo();

# 游戏常量
from config.chess_const import ChessConst;

# 游戏配置
from config.chess_config import ChessCountConfig, ChessResConfig;