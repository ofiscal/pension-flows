from typing import List, Dict, Tuple
import pandas as pd

from python.get_data import ( deduplicate_rows,
                              interpret_columns,
                              raw_renamed_data )


ppl = interpret_columns (
  deduplicate_rows (
    raw_renamed_data () ) )
