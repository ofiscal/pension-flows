import pandas as pd

import python.build.nov2022_ish as n2
from python.common import min_wage_2022


df = n2.read_marchThroughDec()


#####################################
#### Create wage bucket columns. ####
#####################################

min_wage_buckets = [
  # Each of these is a (minimum, supremum) pair.
  ( 0, 1 ),
  ( 1, 1.5 ),
  ( 1.5, 3 ),
  ( 3, 9e300 ) ] # 9e300 min wages is effectively infinity

def rangeString ( iMin : float, iSup : float ) -> str:
  return "in [" + str(iMin) + "," + str(iSup) + ") sm"

# Defines a boolean series.
def labor_income_is_in_range ( a : float, b : float ) -> pd.Series:
  return ( ( df["labor income"] >= a ) &
           ( df["labor income"] < b ) )

df["one"] = 1

for (iMin, iSup) in min_wage_buckets:
  df["earns " + rangeString ( iMin, iSup ) ] = \
    labor_income_is_in_range ( iMin * min_wage_2022,
                               iSup * min_wage_2022 )

# Verify that the boolean "earns*" variables form a partition.
assert ( ( df["one"].sum() ) ==
         ( df[ [ "earns " + rangeString(iMin,iSup)
                 for (iMin,iSup) in min_wage_buckets ] ]
           . sum()
           . sum() ) )
