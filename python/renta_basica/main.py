from os.path import join
from typing import List, Dict, Tuple, Any
import pandas as pd
import matplotlib.pyplot as plt

from python.get_data import mkData
from python.renta_basica.lib import subsidy
import python.renta_basica.lib as rb
from python.cdfs.lib import draw_cdf_of_money


df = mkData()

# If you're old, this is probably close to your total income.
df["total-ish income"] = (
  df[ ["labor income",
       "pension income",
       "rental income", ] ]
  . sum ( axis = "columns" ) )


# =======================================================
# === Deciding which pension income to consider real. ===
# =======================================================

# Pensions are supposed to be around 1 minimum wage.
# This CDF indicates that filtering anywhere between 1e5 and 7e5
# has about the same effect, of only excluding a few unlikely answers.

if False: # I already did it.
  draw_cdf_of_money (
    colname         = "pension income",
    df              = df [ df["age"] >= 65 ],
    ct              = {},
    output_filename = "WUUUU" )


# ==============================================
# === Computing the cost of the renta básica ===
# ==============================================

# So I'll put it at 2e5 COP per month
for real_pension_threshold in [1e5, 7e5]: # COP per month

  df["subsidy"] = df.apply (
      lambda row: (
        0
        if ( (row["age"] < 65) |
             ( row["pension income"] > real_pension_threshold ) )
        else subsidy ( row["total-ish income" ] ) ),
      axis = "columns" )

  assert ( ( df [ df["age"] < 65 ]
             ["subsidy"] . sum() )
           == 0 )

  assert ( ( df [ df["pension income"] > real_pension_threshold ]
             ["subsidy"] . sum() )
           == 0 )

  # This is the cost of a renta basica,
  # under the parameters stated in python.renta_basica.lib,
  # if it goes only to people age 65 or older.

  print ( "threshold to consider reported pension income a real pension: ",
          str(real_pension_threshold),
          "\n",
          "yealy cost in billones de COP: ",
          str ( 12 * # yearly
                ( df["subsidy"] *
                  df["weight"] )
                . sum() / 1e12 ),
          "\n" )



old = df[ df["age"] >= 65 ]

print( "subsidy_if_broke: ",            rb.subsidy_if_broke )
print( "when_subsidy_starts_to_wane: ", rb.when_subsidy_starts_to_wane )
print( "when_subsidy_disappears: ",     rb.when_subsidy_disappears )

print ("Millions of people 65 or over: ",
       str ( old["weight"] . sum() / 1e6 ) )
print ("Millions of people 65 or over excluded from the subsidy (because they have a real-looking pension): ",
       str ( old [ old["pension income"] >
                   real_pension_threshold ]
             ["weight"]
             . sum()
             / 1e6 ) )
