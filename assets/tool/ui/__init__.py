# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2019-09-21 15:47:54
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-09-22 20:53:33

import os;
import sys;

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__));
sys.path.append(CURRENT_PATH);

__all__ = ["ChessBitmap"]

try:
	from bitmap import ChessBitmap;

except Exception as e:
	raise e;
finally:
	sys.path.remove(CURRENT_PATH);