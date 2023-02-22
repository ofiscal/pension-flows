from   datetime import datetime
from   os.path import join
import pandas as pd
from   typing import List, Dict, Tuple, Any

from   python.build.nov2022  import mkData
import python.renta_basica.lib as rb
from   python.types          import BasicIncome, BasicIncome_toDict


df = mkData()


# ==============================================
# === Computing the cost of the renta básica ===
# ==============================================

def describeBasicIncome ( bi  : BasicIncome,
                          df0 : pd.DataFrame,
                         ) -> pd.Series:
  df = df0.copy()
  acc = dict() # accumulates return values

  df["subsidy"] = df.apply (
    lambda row: rb.subsidy ( bi, row ),
    axis = "columns" )
  df = df[ df["subsidy"] > 0 ]

  acc["people (millions)"] = ( df["weight"] . sum()
                               / 1e6 ) # put it in millions
  acc["cost (billones COP)"] = ( ( ( df["subsidy"] * df["weight"] )
                                   . sum() )
                                 / 1e12 )
  return pd.Series ( { **BasicIncome_toDict(bi),
                       **acc, } )

acc : List[pd.Series] = []
start_time = datetime.now()
for subsidy_if_broke in [0.2,0.35,0.5]:
  for when_subsidy_starts_to_wane in [0,1,2]:
    wssw = when_subsidy_starts_to_wane
    for when_subsidy_disappears in [wssw + 1, wssw + 2]:
      for pensioners_included in [0,1]:
        for homeowners_included in [0,1]:
          for homeowners_implicit_income_counts in [0,1]:
            bi = BasicIncome (
              subsidy_if_broke            = subsidy_if_broke,
              when_subsidy_starts_to_wane = when_subsidy_starts_to_wane,
              when_subsidy_disappears     = when_subsidy_disappears,
              pensioners_included         = pensioners_included,
              homeowners_included         = homeowners_included,
              homeowners_implicit_income_counts = \
                homeowners_implicit_income_counts, )
            acc.append(
              describeBasicIncome( bi = bi,
                                   df0 = df ) )
print( datetime.now() - start_time )

res = pd.DataFrame( acc )

res.to_excel( "basic_income_scenarios.xlsx" )
