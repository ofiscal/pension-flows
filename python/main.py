from typing import List, Dict, Tuple, Any
import pandas as pd
import matplotlib.pyplot as plt

from python.get_data import mkData
from ofiscal_utils.draw.draw import cdf
from python.lib import ( constraint_string,
                         df_subset_from_constraints )


df = mkData()

def draw_cdf_of (
    colname : str,
    df : pd.DataFrame,
    subsample : str
): # pure IO [writes a file]
  cdf( df[colname],
       logx = True )
  plt.title("CDF of " + colname)
  plt.xlabel("COP")
  plt.ylabel("Probability mass")
  plt.savefig( "CDF-of-" + colname
               + constraint_string( ct )
               + ".png" )
  plt.close()

[ (a,b)
  for a in [0,1,None]
  for b in [0,1] ]

women    = df[ df["female"]      == 1]
men      = df[ df["female"]      == 0]
rural    = df[ df["source file"] == "area"]
urban    = df[ df["source file"] == "cabecera"]
formal   = df[ df["formal"]      == 1]
informal = df[ df["formal"]      == 0]
