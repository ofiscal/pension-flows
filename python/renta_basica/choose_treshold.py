# ==============================================================
# === Deciding which pension income values to consider real. ===
# ==============================================================

# Pensions are supposed to be around 1 minimum wage.
# The CDF drawn below shows that filtering anywhere between 1e5 and 7e5
# has about the same effect --
# namely, that it only excludes a few unlikely answers.


from typing import List, Dict, Tuple, Any
import pandas as pd

from python.build.nov2022 import mkData
from python.cdfs.lib import draw_cdf_of_money


df = mkData()

draw_cdf_of_money (
  colname         = "pension income",
  df              = df [ df["age"] >= 65 ],
  ct              = {},
  output_filename = "WUUUU" )
