from typing import List, Dict, Tuple
from os.path import join
import pandas as pd


datapath : str = "data/geih/2021-11/csv"

columns_of_interest_original_names : List [str] = \
    [ "fex_c_2011", "DIRECTORIO", "ORDEN",
      "INGLABO", "P6920", "P6430" ]

rename_columns : Dict [ str, str ] = \
  { "fex_c_2011" : "weight",
    "INGLABO"    : "labor income",
    "P6920"      : "pension contrib",
    "P6430"      : "independiente" }

def fetch_one ( filename : str, nickname : str ) -> pd.DataFrame:
  df = (
    pd.read_csv (
      join ( datapath, filename ),
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
