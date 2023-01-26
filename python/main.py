from typing import List, Dict
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

area = (
  pd.read_csv (
    join ( datapath, "area_Ocupados.csv" ),
    usecols = columns_of_interest_original_names,
    sep = ";" )
  . rename ( columns = rename_columns ) )

cabecera = (
  pd.read_csv(
    join ( datapath, "Cabecera_Ocupados.csv" ),
    usecols = columns_of_interest_original_names,
    sep = ";" )
  . rename ( columns = rename_columns ) )

resto = (
  pd.read_csv(
    join ( datapath, "Resto_Ocupados.csv" ),
    usecols = columns_of_interest_original_names,
    sep = ";" )
  . rename ( columns = rename_columns ) )
