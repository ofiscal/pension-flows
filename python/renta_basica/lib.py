# DEFINES:
#
#     def near_nonzero (a : float, b : float) -> bool:
#
#     def negative_dSubsidy_dIncome ( bi : BasicIncome ) -> float:
#
#     def subsidy ( income : float ) -> float:
#
# and tests for all of them..

import matplotlib.pyplot as plt
import pandas as pd
from   typing import List, Dict, Tuple, Any

from python.common import min_wage
from python.lib    import near_nonzero
from python.types  import BasicIncome


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

def qualifies_for_subsidy ( bi : BasicIncome,
                            row : pd.Series,
                           ) -> bool:
    return all ( [
      row["age"] >= 65,
      bi.pensioners_included | (row["pensioner"] == 0),
      bi.homeowners_included | (row["homeowner"] == 0) ] )

def test_qualifies_for_subsidy():
  p = pd.DataFrame ( { "age" : [60,60,60,60, 70,70,70,70],
                       "pensioner" : [0,0,1,1, 0,0,1,1],
                       "homeowner" : [0,1,0,1, 0,1,0,1], } )
  assert (
    p.apply (
      lambda row: qualifies_for_subsidy (
        BasicIncome ( subsidy_if_broke = 1/2,
                      when_subsidy_starts_to_wane = 2,
                      when_subsidy_disappears = 4,
                      pensioners_included = 0,
                      homeowners_included = 0,
                      homeowners_implicit_income_counts = 0 ),
        row ),
      axis = "columns" )
    . astype ( int )
    . equals (
      pd.Series ( [ 0,0,0,0, 1,0,0,0 ] ) ) )

  assert (
    p.apply (
      lambda row: qualifies_for_subsidy (
        BasicIncome ( subsidy_if_broke = 1/2,
                      when_subsidy_starts_to_wane = 2,
                      when_subsidy_disappears = 4,
                      pensioners_included = 1, # changed
                      homeowners_included = 0,
                      homeowners_implicit_income_counts = 0 ),
        row ),
      axis = "columns" )
    . astype ( int )
    . equals (
      pd.Series ( [ 0,0,0,0, 1,0,1,0 ] ) ) )

  assert (
    p.apply (
      lambda row: qualifies_for_subsidy (
        BasicIncome ( subsidy_if_broke = 1/2,
                      when_subsidy_starts_to_wane = 2,
                      when_subsidy_disappears = 4,
                      pensioners_included = 0, # changed
                      homeowners_included = 1, # changed
                      homeowners_implicit_income_counts = 0 ),
        row ),
      axis = "columns" )
    . astype ( int )
    . equals (
      pd.Series ( [ 0,0,0,0, 1,1,0,0 ] ) ) )

def income_for_subsidy_purposes ( homeowners_implicit_income_counts,
                                  row : pd.Series,
                                 ) -> float:
  return row[ "total-ish + homeowner income"
              if homeowners_implicit_income_counts
              else "total-ish income" ]

def test_income_for_subsidy_purposes():
  r = pd.Series ( { "total-ish + homeowner income" : 1,
                    "total-ish income" : 2, } )
  assert (
    income_for_subsidy_purposes (
      homeowners_implicit_income_counts = True,
      row = r )
    == r["total-ish + homeowner income"] )
  assert (
    income_for_subsidy_purposes (
      homeowners_implicit_income_counts = False,
      row = r )
    == r["total-ish income"] )

def subsidy_if_qualified ( bi : BasicIncome,
                           relevant_income : float
                          ) -> float:
  intercept :  float = min_wage * bi.subsidy_if_broke
  fade_start : float = min_wage * bi.when_subsidy_starts_to_wane
  fade_end :   float = min_wage * bi.when_subsidy_disappears

  # The easiest way to understand this expression
  # might be to read the function (next) that tests it.
  return intercept - max ( 0, ( negative_dSubsidy_dIncome(bi)
                                * ( min( relevant_income, fade_end)
                                    - fade_start) ) )

def test_subsidy_if_qualified ():
  # The subsidy starts at subsidy_if_broke.
  bi = BasicIncome (
    subsidy_if_broke = 1/2,
    when_subsidy_starts_to_wane = 2,
    when_subsidy_disappears = 4,
    pensioners_included = None,                # irrelevant
    homeowners_included = None,                # irrelevant
    homeowners_implicit_income_counts = None ) # irrelevant

  assert near_nonzero ( subsidy_if_qualified (bi, 0),
                        bi . subsidy_if_broke * min_wage )
  assert near_nonzero (
    subsidy_if_qualified( bi,
                          bi.when_subsidy_starts_to_wane * min_wage ),
    bi . subsidy_if_broke * min_wage )

  # Halfway from when_subsidy_starts_to_wane to when_subsidy_disappears,
  # the subsidy should be at half what it is for someone who's broke.
  assert near_nonzero (
    subsidy_if_qualified (
      bi,
      0.5 * ( bi.when_subsidy_starts_to_wane * min_wage
              + bi.when_subsidy_disappears * min_wage ) ),
    bi.subsidy_if_broke * min_wage / 2 )

  # At when_subsidy_disappears at thereafter, the subsidy is 0.
  assert near_nonzero (
    subsidy_if_qualified( bi,
                          bi.when_subsidy_disappears * min_wage),
    0 )
  assert near_nonzero (
    subsidy_if_qualified( bi,
                          bi.when_subsidy_disappears * min_wage * 2),
    0 )
  assert near_nonzero (
    subsidy_if_qualified( bi,
                          bi.when_subsidy_disappears * min_wage * 3),
    0 )

def subsidy ( bi : BasicIncome,
              row : pd.Series,
             ) -> float:
  # This is essentially untestable,
  # but all of its component functions are tested.
  if not qualifies_for_subsidy ( bi = bi,
                                 row = row ):
    return 0
  return subsidy_if_qualified (
    bi = bi,
    relevant_income = income_for_subsidy_purposes (
      homeowners_implicit_income_counts = (
        bi.homeowners_implicit_income_counts ),
      row = row ) )
