from os.path import join
from typing import List, Dict, Tuple, Any
import pandas as pd
import matplotlib.pyplot as plt

from python.get_data import mkData
from ofiscal_utils.draw.draw import cdf
from python.lib import ( constraint_string,
                         df_subset_from_constraints,
                         drop_none_values_from_dict, )


df = mkData()

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

constraints : List[ Dict[ str, Any ] ] = [
  drop_none_values_from_dict (
    { "female": female,
      "source file" : source,
      "formal" : formal,
      "indep" : indep
     } )
  for source in [None,"area","cabecera"]
  for female in [None,0,1]
  for formal in [None,0,1]
  for indep  in [None,0,1] ]

output_folder = "output/cdfs/"
missing_cdfs_path = join ( output_folder, "MISSING-CDFS.txt" )

with open( missing_cdfs_path, "w" ) as missing_cdfs_file:
  missing_cdfs_file.write( "" ) # Empty the file.

for ct in constraints:
  df_subset = ( df_subset_from_constraints ( df, ct )
                . dropna() )
  if len(df_subset) == 0:
    with open(missing_cdfs_path, "a") as missing_cdfs_file:
      missing_cdfs_file.write ( "No data satisfies "
                                + str(ct) + "\n" )
  else:
    for col in [ "labor income", "pension income" ]:
      draw_cdf_of_money (
        colname = col,
        df = df_subset,
        ct = ct,
        output_filename = join (
          output_folder, ( "CDF-of-" + col
                           + constraint_string( ct )
                           + ".png" ) ) )

with open( join ( output_folder, "README.md" ),
           "w" ) as readme:
  readme.write( """
# What this is

The filenames indicate what each is CDF is. "area" means rural and "cabecera" means urban. (That's GEIH language, not my own.)

The file "MISSING-CDFS.txt" that indicates which files you won't find, because no data satisfies the necessary constraints.

# How many files you should find here.

There are four potential constraints (female, indep, formal and rural/urban), each with 3 potential values (one value, the other value, and "not specified"), which means there are 3**4 = 81 total constraint sets. Since labor income and pension income are both drawn, there would be 81*2 = 162 CDFs in total, if every constraint was fulfilled. If there are fewer than that, "MISSING-CDFS.txt" explains why.
"""
               )
