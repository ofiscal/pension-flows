from os.path import join
from typing import List, Dict, Tuple, Any
import pandas as pd
import matplotlib.pyplot as plt

from python.build.nov2021 import mkData
from python.renta_basica.lib import subsidy
import python.renta_basica.lib as rb
from python.cdfs.lib import draw_cdf_of_money
from python.types import BasicIncome


df = mkData()

# =======================================================
# === Deciding which pension income to consider real. ===
# =======================================================

# TODO: Move this section to another file.

# Pensions are supposed to be around 1 minimum wage.
# This CDF indicates that filtering anywhere between 1e5 and 7e5
# has about the same effect, of only excluding a few unlikely answers.

if True: # I already did it.
  draw_cdf_of_money (
    colname         = "pension income",
    df              = df [ df["age"] >= 65 ],
    ct              = {},
    output_filename = "WUUUU" )

# So I'll put it at 5e5 COP per month
real_pension_threshold = 5e5


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
                    subsidy ( bi, row["total-ish income" ] ) ),
      axis = "columns" )

old = df[ df["age"] >= 65 ]
old_no_pension = old[ old["pension income"] < real_pension_threshold ]

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
