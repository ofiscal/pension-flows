from os.path import join
from typing import List, Dict, Tuple, Any
import pandas as pd
import matplotlib.pyplot as plt

from python.get_data import mkData
from ofiscal_utils.draw.draw import cdf
from python.lib import ( constraint_string,
                         df_subset_from_constraints,
                         drop_none_values_from_dict, )


def near_nonzero (a : float, b : float) -> bool:
  return ( False
           if a < (0.99*b)
           else ( False if b < (0.99*a)
                  else True ) )

def test_near_nonzero ():

  assert near_nonzero(0.5,1) == False
  assert near_nonzero(1,0.5) == False

  assert near_nonzero(1,1.00001) == True
  assert near_nonzero(1.00001,1) == True

# TODO: reify magic numbers like 500e3

def subsidy ( income : float ) -> float:
  return ( 500e3 - max ( 0,
                         0.25 * (min(income,4e6) - 2e6) ) )

def test_subsidy ():
  assert near_nonzero ( subsidy(0)  , 500e3 )
  assert near_nonzero ( subsidy(2e6), 500e3 )
  assert near_nonzero ( subsidy(3e6), 500e3 / 2 )
  assert near_nonzero ( subsidy(4e6), 0 )
  assert near_nonzero ( subsidy(5e6), 0 )


# df = mkData()
