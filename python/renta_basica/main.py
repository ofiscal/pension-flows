from os.path import join
from typing import List, Dict, Tuple, Any
import pandas as pd
import matplotlib.pyplot as plt

from python.get_data import mkData
from python.renta_basica.lib import subsidy


df = mkData()

df["total-ish income"] = (
  df[ ["labor income",
       "pension income",
       "rental income", ] ]
  . sum ( axis = "columns" ) )

df["subsidy"] = df.apply (
    lambda row: ( 0 if row["age"] < 65
                  else subsidy ( row["total-ish income" ] ) ),
    axis = "columns" )

assert ( ( df [ df["age"] < 65 ]
           ["subsidy"] . sum() )
         == 0 )

# This is the cost of a renta basica,
# under the parameters stated in python.renta_basica.lib,
# if it goes only to people age 65 or older.
print( (df["subsidy"] * df["weight"]).sum() )
