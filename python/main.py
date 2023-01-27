from typing import List, Dict, Tuple
import pandas as pd

from python.get_data import ( deduplicate_rows,
                              interpret_columns,
                              raw_renamed_data )
from python.ss_functions import ( mk_pension,
                                  mk_pension_employer )


ppl = interpret_columns (
  deduplicate_rows (
    raw_renamed_data () ) )

for (new_col, function) in [
    ("employee contribs", mk_pension         ),
    ("employer contribs", mk_pension_employer) ]:
  ppl[new_col] = ppl.apply (
    lambda row: function (
      row["independiente"],
      row["labor income"] )
    , axis = "columns" )
