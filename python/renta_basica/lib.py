# DEFINES:
#
# def near_nonzero (a : float, b : float) -> bool:
#
# def negative_dSubsidy_dIncome ( bi : BasicIncome ) -> float:
#
# def subsidy ( income : float ) -> float:
#
# and tests for all functions.


import matplotlib.pyplot as plt
import pandas as pd
from   typing import List, Dict, Tuple, Any

from python.common import min_wage
from python.lib    import near_nonzero
from python.types  import BasicIncome


#################################################
#### Disregarding misreported pension income ####
#################################################

# Reported pension income below this threshold is assumed
# not to be a true pension, since small pensions are illegal.
# See python/renta_basica/choose_treshold.py
# for how this was determined.
real_pension_threshold = 5e5

def has_pension ( pension_income = pd.Series
                 ) -> pd.Series:
  return pension_income >= real_pension_threshold


####################################
#### Computing the renta básica ####
####################################

def negative_dSubsidy_dIncome ( bi : BasicIncome ) -> float:
  # PITFALL:
  # Since this is a positive number,
  # it is the *negative* of the derivative dSubsidy / dIncome.
  # I think that makes the definition of `subsidy()` easier to understand.
  # PITFALL:
  # As a slope, this is unaffected by the value of the minimum wage.
  return ( bi . subsidy_if_broke
           / (bi . when_subsidy_disappears
              - bi . when_subsidy_starts_to_wane) )

def subsidy ( bi : BasicIncome,
              income : float,
             ) -> float:
  intercept  = min_wage * bi.subsidy_if_broke
  fade_start = min_wage * bi.when_subsidy_starts_to_wane
  fade_end   = min_wage * bi.when_subsidy_disappears

  # The easiest way to understand this function
  # is to read the function (next) that tests it.
  return intercept - max ( 0, ( negative_dSubsidy_dIncome(bi)
                                * ( min( income, fade_end)
                                   - fade_start) ) )

def test_subsidy ():
  # The subsidy starts at subsidy_if_broke.
  bi = BasicIncome ( subsidy_if_broke = 1/2,
                     when_subsidy_starts_to_wane = 2,
                     when_subsidy_disappears = 4 )

  assert near_nonzero ( subsidy (bi, 0),
                        bi . subsidy_if_broke * min_wage )
  assert near_nonzero ( subsidy( bi,
                                 bi.when_subsidy_starts_to_wane * min_wage ),
                        bi . subsidy_if_broke * min_wage )

  # Halfway from when_subsidy_starts_to_wane to when_subsidy_disappears,
  # the subsidy should be at half what it is for someone who's broke.
  assert near_nonzero (
    subsidy ( bi,
              0.5 * ( bi.when_subsidy_starts_to_wane * min_wage
                      + bi.when_subsidy_disappears * min_wage ) ),
    bi.subsidy_if_broke * min_wage / 2 )

  # At when_subsidy_disappears at thereafter, the subsidy is 0.
  assert near_nonzero ( subsidy( bi,
                                 bi.when_subsidy_disappears * min_wage),
                        0 )
  assert near_nonzero ( subsidy( bi,
                                 bi.when_subsidy_disappears * min_wage * 2),
                        0 )
  assert near_nonzero ( subsidy( bi,
                                 bi.when_subsidy_disappears * min_wage * 3),
                        0 )
