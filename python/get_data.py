from typing import List, Dict, Tuple
from os.path import join
import pandas as pd


columns_of_interest_original_names : \
  List [str] = \
    [ "fex_c_2011", "DIRECTORIO", "SECUENCIA_P", "ORDEN",
      "INGLABO", "P6920", "P6430" ]

rename_columns : \
  Dict [ str, str ] = \
    { "fex_c_2011"  : "weight",
      "DIRECTORIO"  : "DIR",
      "SECUENCIA_P" : "SEC",
      "ORDEN"       : "ORD",
      "INGLABO"     : "labor income",
      "P6920"       : "pension contrib",
      "P6430"       : "independiente" }

def fetch_one ( filename : str,
                nickname : str
               ) -> pd.DataFrame:
  df = (
    pd.read_csv (
      join ( "data/geih/2021-11/csv",
             filename ),
      usecols = columns_of_interest_original_names,
      sep = ";" )
    . rename ( columns = rename_columns ) )
  df [ "source file" ] = nickname
  return df

def raw_renamed_data () -> pd.DataFrame:
  return pd.concat (
    [ fetch_one ( "area_Ocupados.csv"     , "area"     ),
      fetch_one ( "Cabecera_Ocupados.csv" , "cabecera" ),
      fetch_one ( "Resto_Ocupados.csv"    , "resto"    ) ] )

def interpret_columns ( df : pd.DataFrame
                       ) -> pd.DataFrame:
  df [ "DIR" ] = (
    df [ "DIR" ]
    . str . replace ( ",", "" )
    . astype ( int ) )
  df [ "pension contrib" ] = (
    ( df [ "pension contrib" ] == 1 )
    . astype ( int ) )
  df [ "independiente" ] = (
    df [ "independiente" ]
    . isin ( [1,2,5] )
    . astype ( int ) )
  return df
