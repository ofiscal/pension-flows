from typing import List, Dict, Tuple
import pandas as pd

from python.get_data import (
  deduplicate_rows,
  interpret_columns_caracteristicas_personales,
  interpret_columns_ocupados,
  interpret_columns_otros_ingresos,
  raw_caracteristicas_generales_renamed,
  raw_ocupados_renamed,
  raw_otros_ingresos_renamed, )
from python.ss_functions import ( mk_pension,
                                  mk_pension_employer, )


cg = interpret_columns_caracteristicas_personales (
  deduplicate_rows (
    raw_caracteristicas_generales_renamed () ) )

ocup = interpret_columns_ocupados (
  deduplicate_rows (
    raw_ocupados_renamed () ) )

otros = interpret_columns_otros_ingresos (
  deduplicate_rows (
    raw_otros_ingresos_renamed () ) )


# Compute contributions in "ocup".
for (new_col, function) in [
    ("employee contribs", mk_pension         ),
    ("employer contribs", mk_pension_employer) ]:
  ocup[new_col] = ocup.apply (
    lambda row: function (
      row["independiente"],
      row["labor income"] )
    , axis = "columns" )


allData = otros.merge (
  cg.merge ( ocup,
             how = "outer",
             on = ["DIR","SEC","ORD"] ),
  how = "outer",
  on = ["DIR","SEC","ORD"] )
