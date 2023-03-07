import matplotlib.pyplot as plt
import numpy as np
from   os.path import join
import pandas as pd
from   typing import List, Dict, Tuple, Any

import python.build.nov2022 as nov2022
from python.common import min_wage_2022


if True: # make data
  df22 = nov2022.mkData()

df22 = df22.rename ( columns =
  { "labor income is only income for children" : "breadwinner 4 kids" } )

print ( df22
        [ df22["labor income"] > 0 ]
        ["formal"]
        . describe() [["mean"]] )

for c in ["breadwinner 4 kids",
          "female",
          "indep", ]:
  print ( df22
          [ df22["labor income"] > 0 ]
          . groupby ( [c] )
          ["formal"]
        . describe() [["mean"]] )

print ( df22
        [ df22["labor income"] > 0 ]
        . groupby (
          [ "female",
            "indep", ] )
        ["formal"]
        . describe() [["mean"]] )

print ( df22
        [ df22["labor income"] > 0 ]
        . groupby (
          ["breadwinner 4 kids",
           "indep", ] )
        ["formal"]
        . describe() [["mean"]] )

print ( df22
        [ df22["labor income"] > 0 ]
        . groupby (
          ["breadwinner 4 kids",
           "female", ] )
        ["formal"]
        . describe() [["mean"]] )

print ( df22
        [ df22["labor income"] > 0 ]
        . groupby (
          ["breadwinner 4 kids",
           "female",
           "indep", ] )
        ["formal"]
        . describe() [["mean"]] )
