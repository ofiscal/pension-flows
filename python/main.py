from typing import List, Dict, Tuple
import pandas as pd

from python.get_data import ( deduplicate_rows,
                              interpret_columns_caracteristicas_personales,
                              raw_caracteristicas_generales_renamed,
                              interpret_columns_ocupados,
                              raw_ocupados_renamed )

from python.ss_functions import ( mk_pension,
                                  mk_pension_employer )


ocup = interpret_columns_ocupados (
  deduplicate_rows (
    raw_ocupados_renamed () ) )

cg = interpret_columns_caracteristicas_personales (
  deduplicate_rows (
    raw_caracteristicas_generales_renamed () ) )

# Not everyone is in Ocupados.
# The default "both" merge strategy returns the intersection,
# and hence only the Ocupados,
# whereas a left merge should give everyone
# (assuming  Caracteristicas_Personales describes everyone).
allData = cg.merge ( ocup,
                     how = "left",
                     on = ["DIR","SEC","ORD"] )

allOcup = cg.merge ( ocup,
                     on = ["DIR","SEC","ORD"] )

for (new_col, function) in [
    ("employee contribs", mk_pension         ),
    ("employer contribs", mk_pension_employer) ]:
  ocup[new_col] = ocup.apply (
    lambda row: function (
      row["independiente"],
      row["labor income"] )
    , axis = "columns" )
