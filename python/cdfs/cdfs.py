from os.path import join
from typing import List, Dict, Tuple, Any
import pandas as pd

from python.cdfs.lib import draw_cdf_of_money, readme_string
from python.build.nov2021 import mkMonth
from python.lib import ( constraint_string,
                         df_subset_from_constraints,
                         drop_none_values_from_dict, )


df = mkMonth( month = 11 )

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
  df_subset = df_subset_from_constraints ( df, ct )
  for col in [ "labor income", "pension income" ]:
    if len( df_subset[col] .dropna() ) == 0:
      with open(missing_cdfs_path, "a") as missing_cdfs_file:
        missing_cdfs_file.write (
          "None of the " + col + " series satisfies "
          + str(ct) + "\n" )
    else: draw_cdf_of_money (
      colname = col,
      df = df_subset,
      ct = ct,
      output_filename = join (
        output_folder, ( "CDF-of-" + col
                         + constraint_string( ct )
                         + ".png" ) ) )

with open( join ( output_folder, "README.md" ),
           "w" ) as readme:
  readme.write( readme_string )
