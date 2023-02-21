from typing import List, Dict, Tuple
from os.path import join
import pandas as pd

from python.build.common import (
  primary_keys,
  dicts_to_rename_columns,
  interpret_columns_generales,
  interpret_columns_ocupados,
  deduplicate_rows,
  mk_pension_contribs )


if True: # Add 2021-specific variables to `dicts_to_rename_columns`.
  dicts_to_rename_columns_2021 = dicts_to_rename_columns . copy()
    # PITFALL: This copy is necessary despite appearances,
    # because this module and at least one other
    # both define their own `dicts_to_rename_columns` value.
    # Unless I explicitly copy the dictionary before modifying it,
    # then whichever module was imported most recently
    # will overwrite the value of the other one!
  dicts_to_rename_columns_2021["generales"] = {
    **dicts_to_rename_columns_2021["generales"],
    "P6020" : "female" }
  dicts_to_rename_columns_2021["universal"] = {
    **dicts_to_rename_columns_2021["universal"],
    "fex_c_2011" : "weight" }

def fetch_one ( filename : str,
                nickname : str,
                how_to_rename_columns : Dict [str, str]
               ) -> pd.DataFrame:
  df = (
    pd.read_csv (
      join ( "data/geih/2021-11",
             filename ),
      usecols = how_to_rename_columns.keys(),
      sep = ";" )
    . rename ( columns = how_to_rename_columns ) )
  df [ "source file" ] = nickname
  return df

def fetchSmilarData_renameColumns_and_join (
    filename_tail : str,
    how_to_rename_columns : Dict[str,str]
    ) -> pd.DataFrame:
  (tail,r) = (
    filename_tail,
    how_to_rename_columns )
  return pd.concat (
    [ fetch_one ( "area"     + tail, "area"    , r ),
      fetch_one ( "Cabecera" + tail, "cabecera", r ),
      fetch_one ( "Resto"    + tail, "resto"   , r ) ] )

def raw_ocupados_renamed () -> pd.DataFrame:
  return fetchSmilarData_renameColumns_and_join (
    filename_tail = "_ocupados.csv",
    how_to_rename_columns = {
      **dicts_to_rename_columns_2021["universal"],
      **dicts_to_rename_columns_2021["ocupados"] } )

def raw_generales_renamed () -> pd.DataFrame:
  return fetchSmilarData_renameColumns_and_join (
    filename_tail = "generales.csv",
    how_to_rename_columns = {
      **dicts_to_rename_columns_2021["universal"],
      **dicts_to_rename_columns_2021["generales"] } )

def raw_otros_ingresos_renamed () -> pd.DataFrame:
  return fetchSmilarData_renameColumns_and_join (
    filename_tail = "_Otros-ingresos.csv",
    how_to_rename_columns = {
      **dicts_to_rename_columns_2021["universal"],
      **dicts_to_rename_columns_2021["otros_ingresos"] } )

def interpret_columns_universal_2021 (
    # Make a column numeric.
    df : pd.DataFrame
) -> pd.DataFrame:
  df [ "DIR" ] = (
    df [ "DIR" ]
    . str . replace ( ",", "" )
    . astype ( int ) )
  return df

def interpret_columns_otros_ingresos ( df : pd.DataFrame
                                      ) -> pd.DataFrame:
  # Make two columns numeric.
  df["pension income"] = (
    df ["pension income"]
    . str.replace ( ",", "" )
    . astype ('float') )
  df["rental income"] = (
    df ["rental income"]
    . str.replace ( ",", "" )
    . astype ('float') )
  return df

def mkData () -> pd.DataFrame:
  cg = interpret_columns_generales (
    interpret_columns_universal_2021 (
      deduplicate_rows (
        raw_generales_renamed (),
        primary_keys = primary_keys ) ) )

  otros = interpret_columns_otros_ingresos (
    interpret_columns_universal_2021 (
      deduplicate_rows (
        raw_otros_ingresos_renamed (),
        primary_keys = primary_keys ) ) )
  ocup = mk_pension_contribs ( # This extra step is not present
                               # in the other two tables.
    interpret_columns_ocupados (
      interpret_columns_universal_2021 (
        deduplicate_rows (
          raw_ocupados_renamed (),
          primary_keys = primary_keys ) ) ) )

  m = pd.merge (
    otros.drop ( columns = ["weight"] ),
    pd.merge (
      cg,
      ocup.drop ( columns = ["weight"] ),
      how = "outer",
      on = primary_keys ),
    how = "outer",
    on = primary_keys )
  m["in ocupados"] = m["in ocupados"] . fillna(0)
  m["source file"] = ( # Reduce the three "source file" fields to one.
                       # See https://stackoverflow.com/a/41449714/916142
    m["source file"]
    . fillna ( m["source file_x"] )
    . fillna ( m["source file_y"] ) )

  for c in ["pension income",
            "labor income",
            "rental income",
            "employee contribs",
            "employer contribs",]:
    m[c] = m[c].fillna(0)

  return m . drop ( columns = ["source file_x",
                               "source file_y" ] )
