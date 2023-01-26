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

def fetch_one ( filename : str ) -> pd.DataFrame:
  return (
    pd.read_csv (
      join ( datapath, filename ),
      usecols = columns_of_interest_original_names,
      sep = ";" )
  . rename ( columns = rename_columns ) )

def fetch_all () -> Tuple [ pd.DataFrame,
                            pd.DataFrame,
                            pd.DataFrame ]:
  return (
    fetch_one ( "area_Ocupados.csv"     ),
    fetch_one ( "Cabecera_Ocupados.csv" ),
    fetch_one (  "Resto_Ocupados.csv"   ) )
