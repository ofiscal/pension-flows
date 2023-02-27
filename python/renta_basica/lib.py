# DEFINES:
#
#     def near_nonzero (a : float, b : float) -> bool:
#
#     def negative_dSubsidy_dIncome ( bi : BasicIncome ) -> float:
#
#     def subsidy ( income : float ) -> float:
#
# and tests for all of them..

from   datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from   typing import List, Dict, Tuple, Any

from python.common import min_wage_2022
from python.lib    import near_nonzero
from python.types  import ( BasicIncome,
                            BasicIncome_toDict,
                            series_toBasicIncome )


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
      (not bi.pensioners_excluded) | (row["pensioner"] == 0),
      (not bi.homeowners_excluded) | (row["homeowner"] == 0) ] )

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
                      pensioners_excluded = 1,
                      homeowners_excluded = 1,
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
                      pensioners_excluded = 0, # changed
                      homeowners_excluded = 1,
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
                      pensioners_excluded = 1, # changed
                      homeowners_excluded = 0, # changed
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
  intercept :  float = min_wage_2022 * bi.subsidy_if_broke
  fade_start : float = min_wage_2022 * bi.when_subsidy_starts_to_wane
  fade_end :   float = min_wage_2022 * bi.when_subsidy_disappears

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
    pensioners_excluded = None,                # irrelevant
    homeowners_excluded = None,                # irrelevant
    homeowners_implicit_income_counts = None ) # irrelevant

  assert near_nonzero ( subsidy_if_qualified (bi, 0),
                        bi . subsidy_if_broke * min_wage_2022 )
  assert near_nonzero (
    subsidy_if_qualified( bi,
                          bi.when_subsidy_starts_to_wane * min_wage_2022 ),
    bi . subsidy_if_broke * min_wage_2022 )

  # Halfway from when_subsidy_starts_to_wane to when_subsidy_disappears,
  # the subsidy should be at half what it is for someone who's broke.
  assert near_nonzero (
    subsidy_if_qualified (
      bi,
      0.5 * ( bi.when_subsidy_starts_to_wane * min_wage_2022
              + bi.when_subsidy_disappears * min_wage_2022 ) ),
    bi.subsidy_if_broke * min_wage_2022 / 2 )

  # At when_subsidy_disappears at thereafter, the subsidy is 0.
  assert near_nonzero (
    subsidy_if_qualified( bi,
                          bi.when_subsidy_disappears * min_wage_2022),
    0 )
  assert near_nonzero (
    subsidy_if_qualified( bi,
                          bi.when_subsidy_disappears * min_wage_2022 * 2),
    0 )
  assert near_nonzero (
    subsidy_if_qualified( bi,
                          bi.when_subsidy_disappears * min_wage_2022 * 3),
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


##########################
#### Building reports ####
##########################

def describeBasicIncome (
    bi        : BasicIncome,
    df0       : pd.DataFrame,
) -> pd.Series:
  df = df0.copy()
  acc = dict() # accumulates return values

  df["subsidy"] = df.apply (
    lambda row: subsidy ( bi, row ),
    axis = "columns" )
  df = df[ df["subsidy"] > 0 ]

  acc["people (millions)"] = ( df["weight"] . sum()
                               / 1e6 ) # put it in millions
  acc["yearly cost (billones COP)"] = (
    ( ( df["subsidy"] * df["weight"] )
      . sum() )
    * 12     # make it yearly
    / 1e12 ) # put it in billones
  return pd.Series ( { **BasicIncome_toDict(bi),
                       **acc, } )

def all_reports(
    df        : pd.DataFrame,
    scenarios : pd.DataFrame,
) -> pd.DataFrame:
  acc : List[pd.Series] = []
  for subsidy_if_broke in [0.2,0.35,0.5]:
    for when_subsidy_starts_to_wane in [0,1,2]:
      for when_subsidy_disappears in [when_subsidy_starts_to_wane + 1,
                                      when_subsidy_starts_to_wane + 2]:
        for pensioners_excluded in [1,0]:
          for homeowners_excluded in [1,0]:
            for homeowners_implicit_income_counts in [0,1]:
              bi = BasicIncome (
                subsidy_if_broke            = subsidy_if_broke,
                when_subsidy_starts_to_wane = when_subsidy_starts_to_wane,
                when_subsidy_disappears     = when_subsidy_disappears,
                pensioners_excluded         = pensioners_excluded,
                homeowners_excluded         = homeowners_excluded,
                homeowners_implicit_income_counts = \
                  homeowners_implicit_income_counts, )
              acc.append(
                describeBasicIncome( bi = bi,
                                     df0 = df ) )
  return pd.DataFrame( acc )

def selected_reports(
    df        : pd.DataFrame,
    scenarios : pd.DataFrame,
) -> pd.DataFrame:
  acc : List[pd.Series] = []
  start_time = datetime.now()
  for i in scenarios.index:
    bi = series_toBasicIncome ( scenarios.iloc[i] )
    acc.append(
      describeBasicIncome( bi = bi,
                           df0 = df ) )
  # print( datetime.now() - start_time )
  return pd.DataFrame( acc )
