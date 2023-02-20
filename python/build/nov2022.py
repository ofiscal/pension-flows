from typing import List, Dict, Tuple
from os.path import join
from numpy import nan
import pandas as pd

from python.ss_functions import ( mk_pension,
                                  mk_pension_employer, )
from python.build.common import (
  primary_keys,
  dicts_to_rename_columns,
  interpret_columns_caracteristicas_personales,
  interpret_columns_ocupados,
  deduplicate_rows,
  mk_pension_contribs )


if True: # Add 2022-specific variables to `dicts_to_rename_columns`.
  dicts_to_rename_columns_2022 = dicts_to_rename_columns . copy()
    # PITFALL: This copy is necessary despite appearances,
    # because this module and at least one other
    # both define their own `dicts_to_rename_columns` value.
    # Unless I explicitly copy the dictionary before modifying it,
    # then whichever module was imported most recently
    # will overwrite the value of the other one!
  dicts_to_rename_columns_2022["caracteristicas_personales"] = {
    **dicts_to_rename_columns_2022["caracteristicas_personales"],
    "P3271"      : "female" } # 2022. Init vals: 1=hombre, 2=mujer
  dicts_to_rename_columns_2022["universal"] = {
    **dicts_to_rename_columns_2022["universal"],
    "FEX_C18"    : "weight" }

def fetch_one ( filename : str,
                how_to_rename_columns : Dict [str, str]
               ) -> pd.DataFrame:
  df = (
    pd.read_csv (
      join ( "data/geih/2022-11",
             filename + ".csv" ),
      usecols = how_to_rename_columns.keys(),
      encoding = "latin",
      sep = ";" )
    . rename ( columns = how_to_rename_columns ) )
  return df

def raw_hogar_renamed () -> pd.DataFrame:
  how_to_rename_columns : Dict[str,str] = {
    ** dicts_to_rename_columns_2022["universal"],
    ** dicts_to_rename_columns_2022["hogar"] }
  del( how_to_rename_columns["ORDEN"] )
    # Uniquely, the "hogar" file has no such column.
  return fetch_one (
    filename = "Datos del hogar y la vivienda",
    how_to_rename_columns = how_to_rename_columns )

def raw_caracteristicas_generales_renamed () -> pd.DataFrame:
  return fetch_one (
    filename = \
      "Caracteristicas generales, seguridad social en salud y educacion",
    how_to_rename_columns = {
      ** dicts_to_rename_columns_2022["universal"],
      ** dicts_to_rename_columns_2022["caracteristicas_personales"] } )

def raw_ocupados_renamed () -> pd.DataFrame:
  return fetch_one (
    filename = "Ocupados",
    how_to_rename_columns = {
      ** dicts_to_rename_columns_2022["universal"],
      ** dicts_to_rename_columns_2022["ocupados"] } )

def raw_otros_ingresos_renamed () -> pd.DataFrame:
  return fetch_one (
    filename = "Otros ingresos e impuestos",
    how_to_rename_columns = {
      ** dicts_to_rename_columns_2022["universal"],
      ** dicts_to_rename_columns_2022["otros_ingresos"] } )

def mkData () -> pd.DataFrame:
  cg = interpret_columns_caracteristicas_personales (
    deduplicate_rows (
      raw_caracteristicas_generales_renamed (),
      primary_keys = primary_keys ) )
  otros = deduplicate_rows ( # No interpretation needed.
    raw_otros_ingresos_renamed (),
    primary_keys = primary_keys )
  ocup = mk_pension_contribs ( # This extra step is not present
                               # in the other two tables.
    interpret_columns_ocupados (
      deduplicate_rows (
        raw_ocupados_renamed (),
        primary_keys = primary_keys ) ) )
  hogar = deduplicate_rows (
    # Unnecessary, but easier than maintaining a proof that it's unnecessary.
    raw_hogar_renamed (),
    ["DIR","SEC"] ) # Because "hogar" has no "ORDEN" column.

  m = pd.merge (
    otros.drop ( columns = ["weight"] ),
    pd.merge (
      cg.merge (
        hogar.drop ( columns = ["weight"] ),
        how = "outer",
        on = ["DIR","SEC"] # Because "hogar" has no "ORDEN" column.
        ),
      ocup.drop ( columns = ["weight"] ),
      how = "outer",
      on = primary_keys ),
    how = "outer",
    on = primary_keys )

  m["in ocupados"] = m["in ocupados"] . fillna(0)

  for c in ["pension income",
            "labor income",
            "rental income",
            "employee contribs",
            "employer contribs",]:
    m[c] = m[c].fillna(0)

  return m
