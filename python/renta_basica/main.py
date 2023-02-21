from os.path import join
from typing import List, Dict, Tuple, Any
import pandas as pd
import matplotlib.pyplot as plt

from   python.build.nov2022  import mkData
from   python.cdfs.lib       import draw_cdf_of_money
import python.renta_basica.lib as rb
from   python.types          import BasicIncome


df = mkData()


# ==============================================
# === Computing the cost of the renta básica ===
# ==============================================

bi_500_0_1 = BasicIncome ( subsidy_if_broke = 1/2,
                           when_subsidy_starts_to_wane = 0,
                           when_subsidy_disappears = 1 )
bi_500_1_2 = BasicIncome ( subsidy_if_broke = 1/2,
                           when_subsidy_starts_to_wane = 1 ,
                           when_subsidy_disappears = 2 )
bi_500_1_3 = BasicIncome ( subsidy_if_broke = 1/2,
                           when_subsidy_starts_to_wane = 1,
                           when_subsidy_disappears = 3 )
bi_500_2_4 = BasicIncome ( subsidy_if_broke = 1/2,
                           when_subsidy_starts_to_wane = 2,
                           when_subsidy_disappears = 4 )

name_subsidy_pairs : List[ Tuple[ str,
                                  BasicIncome ] ] = \
  [("yearly subsidy 500 0 1", bi_500_0_1),
   ("yearly subsidy 500 1 2", bi_500_1_2),
   ("yearly subsidy 500 1 3", bi_500_1_3),
   ("yearly subsidy 500 2 4", bi_500_2_4)]

for name, bi in name_subsidy_pairs:
  df[name] = df.apply (
      lambda row: ( 12 * # yearly
                    rb.subsidy ( bi, row["total-ish income" ] ) ),
      axis = "columns" )

old = df[ df["age"] >= 65 ]
old_no_pension = old[ old["pension income"] < rb.real_pension_threshold ]

def describe_subsidies ( orig : pd.DataFrame
                        ): # pure IO (prints to screen)
  df = orig.copy()
  for name, _ in name_subsidy_pairs:
    # PITFALL: This feels like a hack.
    df[name] = df[name] * df["weight"]
  print ( "People (millions): ", str ( df["weight"] . sum()
                                       / 1e6 ) ) # put it in millions
  print ( "Total cost of each scheme (billones españoles):" )
  print( ( df [ [ name for (name,_) in name_subsidy_pairs ] ]
            / 1e12 ) # put it in billones españoles
         . sum () )

describe_subsidies(old)
describe_subsidies(old_no_pension)
