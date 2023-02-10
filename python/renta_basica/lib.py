from typing import List, Dict, Tuple, Any
import pandas as pd
import matplotlib.pyplot as plt


def near_nonzero (a : float, b : float) -> bool:
  # TODO: This should be part of ofiscal_utils.
  # tax.co has a similar, better function.
  """Verifies that its two inputs are within 1% of each other."""
  return ( False
           if a < (0.99*b)
           else ( False if b < (0.99*a)
                  else True ) )

def test_near_nonzero ():
  assert near_nonzero(0.5,1) == False
  assert near_nonzero(1,0.5) == False

  assert near_nonzero(1,1.00001) == True
  assert near_nonzero(1.00001,1) == True

subsidy_if_broke            = 500e3 # COP per month
when_subsidy_starts_to_wane = 2e6   # COP per month
when_subsidy_disappears     = 4e6   # COP per month.
  # Should be bigger than `when_subsidy_starts_to_wane`.

negative_dSubsidy_dIncome = ( # PITFALL:
  # Since this is a positive number,
  # it is the *negative* of the derivative dSubsidy / dIncome.
  # I think that makes the definition of `subsidy()` easier to understand.
  subsidy_if_broke
  / (when_subsidy_disappears
     - when_subsidy_starts_to_wane) )

def subsidy ( income : float ) -> float:
  # The easiest way to understand this function
  # is to read the function (next) that tests it.
  return ( subsidy_if_broke
           - max ( 0,
                   ( negative_dSubsidy_dIncome
                     * ( min( income,
                              when_subsidy_disappears)
                         - when_subsidy_starts_to_wane) ) ) )

def test_subsidy ():
  # The subsidy starts at subsidy_if_broke.
  assert near_nonzero ( subsidy(0),
                        subsidy_if_broke )
  assert near_nonzero ( subsidy(when_subsidy_starts_to_wane),
                        subsidy_if_broke )

  # Halfway from when_subsidy_starts_to_wane to when_subsidy_disappears,
  # the subsidy should be at half what it is for someone who's broke.
  assert near_nonzero ( subsidy( 0.5 * ( when_subsidy_starts_to_wane
                                         + when_subsidy_disappears ) ),
                        subsidy_if_broke / 2 )

  # At when_subsidy_disappears at thereafter, the subsidy is 0.
  assert near_nonzero ( subsidy(when_subsidy_disappears), 0 )
  assert near_nonzero ( subsidy(when_subsidy_disappears * 2), 0 )
  assert near_nonzero ( subsidy(when_subsidy_disappears * 3), 0 )
