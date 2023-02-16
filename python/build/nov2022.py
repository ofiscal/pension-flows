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
