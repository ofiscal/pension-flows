from typing import List, Dict, Tuple
import pandas as pd
import matplotlib.pyplot as plt

from python.get_data import mkData
from ofiscal_utils.draw.draw import cdf


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
  plt.savefig( "CDF-of-" + colname   +
               "-for-"   + subsample +
               ".png" )
  plt.close()

def df_subset ( female   : int = None,
                area     : str = None,
                informal : int = None
               ) -> pd.DataFrame:

  def subsetter ( df : pd.DataFrame,
                  colname : str,
                  colval # Its type depends on colname's type:
                         # int if colname in [female, informal]
                         # str if colname == area
                 ) -> pd.DataFrame:
    return ( df
             if colval is None
             else df[ df["colname"] == colval] )

  return subsetter (
    subsetter (
      subsetter ( df, "female", female ),
      "area", area ),
    "informal", informal )



[ (a,b)
  for a in [0,1,None]
  for b in [0,1] ]

women    = df[ df["female"]        == 1]
men      = df[ df["female"]        == 0]
rural    = df[ df["source file"]   == "area"]
urban    = df[ df["source file"]   == "cabecera"]
informal = df[ df['indep"] == 1]
formal   = df[ df["indep"] == 0]
