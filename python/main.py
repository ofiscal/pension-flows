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
    ct : Dict[ str, Any ],
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

constraints : List[ Dict[ str, Any ] ] = [
  { "female": female,
    "source file" : source,
    "formal" : formal,
    "indep" : indep
   }
  for source in ["area","cabecera"]
  for female in [0,1]
  for formal in [0,1]
  for indep  in [0,1] ]

for ct in constraints:
  for col in [ "labor income", "pension income" ]:
    df0 = df_subset_from_constraints ( df, ct )
    if len(df0) == 0:
      print( "WARNING: No data satisfies " + str(ct) )
    else:
      draw_cdf_of (
        colname = col,
        df = df0,
        ct = ct )
