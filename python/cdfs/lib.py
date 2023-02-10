from typing import List, Dict, Tuple, Any
import pandas as pd
import matplotlib.pyplot as plt

from ofiscal_utils.draw.draw import cdf


def draw_cdf_of_money (
    colname         : str,
    df              : pd.DataFrame,
    ct              : Dict[ str, Any ],
    output_filename : str,
): # pure IO [writes a file]
  cdf( df[colname],
       logx = True,
       sample_size = len (df_subset),
       xmin = 1e3 ) # xmin must be > 0 for the log scale to work
  plt.title("CDF of " + colname)
  plt.xlabel("COP")
  plt.ylabel("Probability mass")
  plt.savefig( output_filename )
  plt.close()

readme_string = """# What this is

The filenames indicate what each is CDF is. "area" means rural and "cabecera" means urban. (That's GEIH language, not my own.)

The file "MISSING-CDFS.txt" that indicates which files you won't find, because no data satisfies the necessary constraints.

# How many files you should find here.

There are four potential constraints (female, indep, formal and rural/urban), each with 3 potential values (one value, the other value, and "not specified"), which means there are 3**4 = 81 total constraint sets. Since labor income and pension income are both drawn, there would be 81*2 = 162 CDFs in total, if every constraint was fulfilled. If there are fewer than that, "MISSING-CDFS.txt" explains why.
"""
