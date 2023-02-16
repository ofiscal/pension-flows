from typing import List, Dict, Tuple
from os.path import join
from numpy import nan
import pandas as pd

from python.ss_functions import ( mk_pension,
                                  mk_pension_employer, )
from python.build.common import ( primary_keys,
                                  dicts_to_rename_columns )


if True: # Add 2021-specific variables to `dicts_to_rename_columns`.
  dicts_to_rename_columns["caracteristicas_personales"] = {
    **dicts_to_rename_columns["caracteristicas_personales"],
    "P6020" : "female" }
  dicts_to_rename_columns["universal"] = {
    **dicts_to_rename_columns["universal"],
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
    filename_tail = "_Ocupados.csv",
    how_to_rename_columns = {
      **dicts_to_rename_columns["universal"],
      **dicts_to_rename_columns["ocupados"] } )

def raw_caracteristicas_generales_renamed () -> pd.DataFrame:
  return fetchSmilarData_renameColumns_and_join (
    filename_tail = "_Caracteristicas-generales_Personas.csv",
    how_to_rename_columns = {
      **dicts_to_rename_columns["universal"],
      **dicts_to_rename_columns["caracteristicas_personales"] } )

def raw_otros_ingresos_renamed () -> pd.DataFrame:
  return fetchSmilarData_renameColumns_and_join (
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
  df["female"] = df ["female"] - 1
  return interpret_columns_universal ( df )

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
  return interpret_columns_universal ( df )

def interpret_columns_otros_ingresos ( df : pd.DataFrame
                                      ) -> pd.DataFrame:
  df["pension income"] = (
    df ["pension income"]
    . str.replace ( ",", "" )
    . astype ('float') )
  df["rental income"] = (
    df ["rental income"]
    . str.replace ( ",", "" )
    . astype ('float') )
  return interpret_columns_universal ( df )

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

def mkData () -> pd.DataFrame:
  cg = interpret_columns_caracteristicas_personales (
    deduplicate_rows (
      raw_caracteristicas_generales_renamed (),
      primary_keys = primary_keys ) )
  otros = interpret_columns_otros_ingresos (
    deduplicate_rows (
      raw_otros_ingresos_renamed (),
      primary_keys = primary_keys ) )
  ocup = mk_pension_contribs ( # This extra step is not present
                               # in the other two tables.
    interpret_columns_ocupados (
      deduplicate_rows (
        raw_ocupados_renamed (),
        primary_keys = primary_keys ) ) )

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
