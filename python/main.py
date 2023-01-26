from typing import List, Dict, Tuple
import pandas as pd

from python.get_data import ( interpret_columns,
                              raw_renamed_data )


ppl = interpret_columns (
  raw_renamed_data () )
