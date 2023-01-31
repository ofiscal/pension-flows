from typing import List, Dict, Tuple
from os.path import join
import pandas as pd


columns_of_interest_original_names_universal : \
  List [str] = \
    [ "DIRECTORIO", "SECUENCIA_P", "ORDEN", "fex_c_2011" ]

columns_of_interest_original_names_ocupados : \
  List [str] = (
    columns_of_interest_original_names_universal +
    [ "INGLABO", "P6920", "P6430" ] )

columns_of_interest_original_names_caracteristicas_personales : \
  List [str] = (
    columns_of_interest_original_names_universal +
    [ "P6020", "P6030S3" ] )

rename_columns_universal : \
  Dict [ str, str ] = \
    { "fex_c_2011"  : "weight",
      "DIRECTORIO"  : "DIR",
      "SECUENCIA_P" : "SEC",
      "ORDEN"       : "ORD" }

rename_columns_ocupados : \
  Dict [ str, str ] = \
    { **rename_columns_universal,
      "INGLABO"     : "labor income",

      # PITFALL: The RHS of the following items
      # are names of what the column *will be*
      # once processed by some interpret_columns_ function.
      # Before that, the names on the RHS below are a lie.
      "P6920"       : "contributes to pension",
      "P6430"       : "independiente" }

rename_columns_caracteristicas_personales : \
  Dict [ str, str ] = \
    { **rename_columns_universal,

      # PITFALL: The RHS of the following items
      # are names of what the column *will be*
      # once processed by some interpret_columns_ function.
      # Before that, the names on the RHS below are a lie.
      "P6020"   : "female",
      "P6030S3" : "age" }

def fetch_one ( filename : str,
                nickname : str,
                columns_of_interest : List [str],
                rename_columns : Dict [str, str]
               ) -> pd.DataFrame:
  df = (
    pd.read_csv (
      join ( "data/geih/2021-11",
             filename ),
      usecols = columns_of_interest,
      sep = ";" )
    . rename ( columns = rename_columns ) )
  df [ "source file" ] = nickname
  return df

# TODO: Factor out the commonalities from the next two functions
# (called raw_*_renamed).

def raw_ocupados_renamed () -> pd.DataFrame:
  tail = "_Ocupados.csv"
  cs = columns_of_interest_original_names_ocupados
  r = rename_columns_ocupados
  return pd.concat (
    [ fetch_one ( "area"     + tail, "area"    , cs, r ),
      fetch_one ( "Cabecera" + tail, "cabecera", cs, r ),
      fetch_one ( "Resto"    + tail, "resto"   , cs, r ) ] )

def raw_caracteristicas_generales_renamed () -> pd.DataFrame:
  tail = "_Caracteristicas-generales_Personas.csv"
  cs = columns_of_interest_original_names_caracteristicas_personales
  r = rename_columns_caracteristicas_personales
  return pd.concat (
    [ fetch_one ( "area"     + tail, "area"    , cs, r ),
      fetch_one ( "Cabecera" + tail, "cabecera", cs, r ),
      fetch_one ( "Resto"    + tail, "resto"   , cs, r ) ] )

def interpret_columns_universal (
    df : pd.DataFrame
) -> pd.DataFrame:
  df [ "DIR" ] = (
    df [ "DIR" ]
    . str . replace ( ",", "" )
    . astype ( int ) )
  return df

def interpret_columns_caracteristicas_personales (
    df : pd.DataFrame
) -> pd.DataFrame:
  df["age"] = 2021 - (
    df ["age"]
    . str.replace ( ",", "" )
    . astype ('float') )
  df["female"] = 2021 - (
    df ["female"] - 1 )
  return interpret_columns_universal ( df )

def interpret_columns_ocupados ( df : pd.DataFrame
                                ) -> pd.DataFrame:
  df [ "contributes to pension" ] = (
    ( df [ "contributes to pension" ] == 1 )
    . astype ( int ) )
  df [ "independiente" ] = (
    df [ "independiente" ]
    . isin ( [1,2,5] )
    . astype ( int ) )
  return interpret_columns_universal ( df )

def deduplicate_rows ( df : pd.DataFrame
                      ) -> pd.DataFrame:
  # See `python.check_integrity.py` for why this is justified.
  return ( df
           . groupby ( ["DIR", "SEC", "ORD"] )
           . agg ( "first" )
           . reset_index() )
