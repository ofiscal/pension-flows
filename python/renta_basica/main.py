from   datetime import datetime
from   os.path import join
import pandas as pd
from   typing import List, Dict, Tuple, Any

from   python.build.nov2022  import mkData
import python.renta_basica.lib as rb
from   python.types          import ( BasicIncome,
                                      BasicIncome_toDict,
                                      series_toBasicIncome )


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
  acc["yearly cost (billones COP)"] = (
    ( ( df["subsidy"] * df["weight"] )
      . sum() )
    * 12     # make it yearly
    / 1e12 ) # put it in billones
  return pd.Series ( { **BasicIncome_toDict(bi),
                       **acc, } )

scenarios = (
  pd.read_csv(
    "python/renta_basica/scenarios.csv" )
  . drop (
    columns = ["Unnamed: 0",
               "beneficiarios (millones)",
               "costo (billones anuales)"] ) )

acc : List[pd.Series] = []
start_time = datetime.now()
for i in scenarios.index:
  bi = series_toBasicIncome ( scenarios.iloc[i] )
  acc.append(
    describeBasicIncome( bi = bi,
                         df0 = df ) )
print( datetime.now() - start_time )

res = pd.DataFrame( acc )
res.to_excel( "basic_income_simulations.xlsx" )
