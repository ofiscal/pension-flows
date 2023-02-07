from typing import List, Dict, Tuple
import pandas as pd
import matplotlib.pyplot as plt

from python.get_data import mkData
from ofiscal_utils.draw.draw import cdf


df = mkData()

if True: # draw pension income
  cdf( df["pension income"],
       logx = False )
  plt.title("CDF of pension icnome")
  plt.xlabel("Income")
  plt.ylabel("Probability")
  plt.savefig("test-cdf.png")
  plt.close()
