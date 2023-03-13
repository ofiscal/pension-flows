import matplotlib.pyplot as plt
import numpy as np
from   os.path import join
import pandas as pd
from   typing import List, Dict, Tuple, Any

import python.build.nov2022_ish as nov2022_ish
from python.common import min_wage_2022


if True: # make data
  df22 = nov2022_ish.mkData()

breadwinner          = "labor income is only income for household"
breadwinner_for_kids = "labor income is only income for children"


#####
##### formality by groups
#####

print ( df22
        [ df22["labor income"] > 0 ]
        ["formal"]
        . describe() [["mean"]] )

for c in [breadwinner_for_kids,
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
          [breadwinner_for_kids,
           "indep", ] )
        ["formal"]
        . describe() [["mean"]] )

print ( df22
        [ df22["labor income"] > 0 ]
        . groupby (
          ["breadwinner for kids",
           "female", ] )
        ["formal"]
        . describe() [["mean"]] )

print ( df22
        [ df22["labor income"] > 0 ]
        . groupby (
          [breadwinner_for_kids,
           "female",
           "indep", ] )
        ["formal"]
        . describe() [["mean"]] )


#####
##### "breadwinner" by groups
#####

print ( df22
        [ df22["labor income"] > 0 ]
        [breadwinner]
        . describe() [["mean"]] )

print ( df22
        [ df22["labor income"] > 0 ]
        [breadwinner_for_kids]
        . describe() [["mean"]] )
