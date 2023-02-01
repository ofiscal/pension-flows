from typing import List, Dict, Tuple
from os.path import join
import pandas as pd


dicts_to_rename_columns : \
  Dict [ str, Dict [ str, str ] ] = \
    { "universal" : { "fex_c_2011"  : "weight",
                      "DIRECTORIO"  : "DIR",
                      "SECUENCIA_P" : "SEC",
                      "ORDEN"       : "ORD" },

      # PITFALL: The RHS of most of the string-string pairs below
      # are LIES, to begin with.
      # Only once the data is processed by some interpret_columns_ function
      # are those column names accurate.

      "caracteristicas_personales" : { "P6020"   : "female",
                                       "P6030S3" : "age" },

      "ocupados" : { "INGLABO"     : "labor income",
                     "P6920"       : "contributes to pension",
                     "P6430"       : "independiente" },

      "otros_ingresos" : { "P7500S2A1" : "pension income" },
     }

def fetch_one ( filename : str,
                nickname : str,
                columns_of_interest : List [str],
                how_to_rename_columns : Dict [str, str]
               ) -> pd.DataFrame:
  df = (
    pd.read_csv (
      join ( "data/geih/2021-11",
             filename ),
      usecols = columns_of_interest,
      sep = ";" )
    . rename ( columns = how_to_rename_columns ) )
  df [ "source file" ] = nickname
  return df

def fetchImilarData_renameColumns_and_join (
    filename_tail : str,
    how_to_rename_columns : Dict[str,str]
    ) -> pd.DataFrame:
  (tail,orig,r) = (
    filename_tail,
    list ( how_to_rename_columns.keys() ), # original names
    how_to_rename_columns )
  return pd.concat (
    [ fetch_one ( "area"     + tail, "area"    , orig, r ),
      fetch_one ( "Cabecera" + tail, "cabecera", orig, r ),
      fetch_one ( "Resto"    + tail, "resto"   , orig, r ) ] )

def raw_ocupados_renamed () -> pd.DataFrame:
  return fetchImilarData_renameColumns_and_join (
    filename_tail = "_Ocupados.csv",
    how_to_rename_columns = {
      **dicts_to_rename_columns["universal"],
      **dicts_to_rename_columns["ocupados"] } )

def raw_caracteristicas_generales_renamed () -> pd.DataFrame:
  return fetchImilarData_renameColumns_and_join (
    filename_tail = "_Caracteristicas-generales_Personas.csv",
    how_to_rename_columns = {
      **dicts_to_rename_columns["universal"],
      **dicts_to_rename_columns["caracteristicas_personales"] } )

def raw_otros_ingresos_renamed () -> pd.DataFrame:
  return fetchImilarData_renameColumns_and_join (
    filename_tail = "_Otros-ingresos.csv",
    how_to_rename_columns = {
      **dicts_to_rename_columns["universal"],
      **dicts_to_rename_columns["otros_ingresos"] } )

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
  df["female"] = df ["female"] - 1
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
  df [ "in ocupados" ] = 1
  return interpret_columns_universal ( df )

def interpret_columns_otros_ingresos ( df : pd.DataFrame
                                      ) -> pd.DataFrame:
  df["pension income"] = (
    df ["pension income"]
    . str.replace ( ",", "" )
    . astype ('float') )
  return interpret_columns_universal ( df )

def deduplicate_rows ( df : pd.DataFrame
                      ) -> pd.DataFrame:
  # See `python.check_integrity.py` for why this is justified.
  return ( df
           . groupby ( ["DIR", "SEC", "ORD"] )
           . agg ( "first" )
           . reset_index() )
