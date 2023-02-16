from typing import List, Dict, Tuple
from os.path import join
from numpy import nan
import pandas as pd

from python.ss_functions import ( mk_pension,
                                  mk_pension_employer, )
from python.build.common import ( primary_keys,
                                  dicts_to_rename_columns )


if True: # Add 2022-specific variables to `dicts_to_rename_columns`.
  dicts_to_rename_columns["caracteristicas_personales"] = {
    **dicts_to_rename_columns["caracteristicas_personales"],
    "P3271"      : "female" } # 2022. Init vals: 1=hombre, 2=mujer
  dicts_to_rename_columns["universal"] = {
    **dicts_to_rename_columns["universal"],
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

def raw_caracteristicas_generales_renamed () -> pd.DataFrame:
  return fetch_one (
    filename = \
      "Caracteristicas generales, seguridad social en salud y educacion",
    how_to_rename_columns = {
      ** dicts_to_rename_columns["universal"],
      ** dicts_to_rename_columns["caracteristicas_personales"] } )

def raw_ocupados_renamed () -> pd.DataFrame:
  return fetch_one (
    filename = "Ocupados",
    how_to_rename_columns = {
      ** dicts_to_rename_columns["universal"],
      ** dicts_to_rename_columns["ocupados"] } )

def raw_otros_ingresos_renamed () -> pd.DataFrame:
  return fetch_one (
    filename = "Otros ingresos e impuestos",
    how_to_rename_columns = {
      ** dicts_to_rename_columns["universal"],
      ** dicts_to_rename_columns["otros_ingresos"] } )
