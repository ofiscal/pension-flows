from typing import List, Dict, Tuple
from os.path import join
from numpy import nan
import pandas as pd

from python.ss_functions import ( mk_pension,
                                  mk_pension_employer, )


year_month = "data/geih/2022-11"

# PITFALL: There is no "ORDEN" (ORD) in the file
# `Datos del hogar y la vivienda.csv` for 2022.
primary_keys : List[str] = \
  ["DIR","SEC","ORD"]

dicts_to_rename_columns : Dict [ str, Dict [ str, str ] ] = {
  # PITFALL: 2021 and 2022 differ slightly.
  # This dictionary is only for variables they define the same way.
  "universal" : { "DIRECTORIO"  : "DIR",
                  "SECUENCIA_P" : "SEC",
                  "ORDEN"       : "ORD" },

  # PITFALL: The RHS of most of the string-string pairs below
  # are LIES, to begin with.
  # Only once the data is processed by some interpret_columns_ function
  # are those column names accurate.

  "generales" : {
    "P6040" : "age" },

  "ocupados" : {
    "INGLABO" : "labor income",
    "P6920"   : "formal", # <=> Contributes to a pension.
    "P1879"   : "indep" # <=> if non-null, gave reason for working indep
  },

  "otros_ingresos" : { "P7500S2A1" : "pension income",
                       "P7500S1A1" : "rental income", },

  "hogar" : { "P5130" : "implicit homeowner income",
              "P5090" : "homeowner", },
    # PITFALL: This includes values 98 and 99, which are error codes
    # ("doesn't know" and "won't say", maybe not in that order).
    # However, since we are only interested in whether this is > 0,
    # those values should not be set to 0 -- or if they are,
    # a new columnn should be created to preserve the information
    # that the household does not pay rent.
}

def interpret_columns_generales (
    df : pd.DataFrame
) -> pd.DataFrame:
  df["female"] = df ["female"] - 1
  return df

def interpret_columns_ocupados ( df : pd.DataFrame
                                ) -> pd.DataFrame:
  df [ "formal" ] = (
    ( df [ "formal" ] == 1 )
    . astype ( int ) )
  df [ "indep" ] = (
    ( ~ ( df [ "indep" ]
          . isnull() ) )
    . astype("int") )
  df [ "in ocupados" ] = 1
  return df

def interpret_columns_hogares ( df : pd.DataFrame
                               ) -> pd.DataFrame:
  df["homeowner"] = ( df["homeowner"]
                      # 1 = owns hogar outright. 2 = paying down mortgage.
                      . isin ( [1,2] ) )
  return df

def deduplicate_rows (
    df : pd.DataFrame,
    primary_keys = List[str], # PITFALL: Argument needed for testing.
) -> pd.DataFrame:
  # See `python.check_integrity.py` for why this is justified.
  return ( df
           . groupby ( primary_keys )
           . agg ( "first" ) # gives the first non-null, not just the first
           . reset_index() )

def test_deduplicate_rows ():
  assert (
    deduplicate_rows (
      pd.DataFrame ( { "id" : [1  ,   1,  2],
                       "a"  : [nan,  11, 12],
                       "b"  : [21 , nan, 22], } ),
      primary_keys = ["id"] )
    . equals (
      pd.DataFrame ( { "id" : pd.Series( [1 ,  2] ),
                       "a"  : pd.Series( [11, 12], dtype = float),
                       "b"  : pd.Series( [21, 22], dtype = float), } ) ) )

def mk_pension_contribs ( df : pd.DataFrame
                         ) -> pd.DataFrame:
  for (new_col, function) in [
      ("employee contribs", mk_pension         ),
      ("employer contribs", mk_pension_employer) ]:
    df[new_col] = df.apply (
      lambda row: function (
        row["indep"],
        row["labor income"] )
      , axis = "columns" )
  return df

def mk_total_income ( df : pd.DataFrame
                      ) -> pd.DataFrame:
  df["total-ish income"] = (
    # If you're old, this is probably close to your total income.
    # TODO ? Add more kinds of income.
    df[ ["labor income",
         "pension income",
         "rental income", ] ]
    . sum ( axis = "columns" ) )
  df["total-ish + homeowner income"] = (
    df[ ["total-ish income",
         "implicit homeowner income", ] ]
    . sum ( axis = "columns" ) )
  return df
