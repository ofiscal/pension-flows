from os.path import join
from typing import List, Dict, Tuple, Any
import pandas as pd
import matplotlib.pyplot as plt

from python.get_data import mkData
from ofiscal_utils.draw.draw import cdf
from python.lib import ( constraint_string,
                         df_subset_from_constraints )


df = mkData()

def draw_cdf_of (
    colname         : str,
    df              : pd.DataFrame,
    ct              : Dict[ str, Any ],
    output_filename : str,
): # pure IO [writes a file]
  cdf( df[colname],
       logx = True,
       xmin = 1e3 ) # xmin must be > 0 for the log scale to work
  plt.title("CDF of " + colname)
  plt.xlabel("COP")
  plt.ylabel("Probability mass")
  plt.savefig( output_filename )
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

output_folder = "output/cdfs/"
missing_cdfs_path = join ( output_folder, "MISSING-CDFS.txt" )

with open( missing_cdfs_path, "w" ) as myfile:
  myfile.write( "" ) # Empty the file.

for ct in constraints:
  for col in [ "labor income", "pension income" ]:
    df_subset = ( df_subset_from_constraints ( df, ct )
                  . dropna() )
    if len(df_subset) == 0:
      with open(missing_cdfs_path, "w") as missing_cdfs_file:
        missing_cdfs_file.write ( "WARNING: No data satisfies "
                                  + str(ct) )
    else:
      draw_cdf_of (
        colname = col,
        df = df_subset,
        ct = ct,
        output_filename = join (
          output_folder, ( "CDF-of-" + col
                           + constraint_string( ct )
                           + ".png" ) ) )
