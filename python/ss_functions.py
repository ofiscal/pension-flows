# # TODO: Make this into a shared (across repos) module.
#
# I've copied the functions in this folder from the microsimulation (tax.co).
# That's expedient but inelegant.
# Better to separate these into an independent module that both can import.

from typing import Tuple, List, Dict
import pandas as pd

from python.ss_schedules import (
  ss_contrib_schedule_for_contractor,
  ss_contrib_schedule_for_employee,
  ss_contrib_schedule_by_employer )
from python.types import Schedule


def tuple_by_threshold (
    income : float,
    schedule : List [ Schedule ]
    ) -> Schedule:
  if (   ( not( schedule[1:] ) ) # [] = False, nonempty list = True
       | (income < schedule[0][0] ) ):
      return schedule[0]
  highEnoughToBeHere = (income >= schedule[0][0])
  lowEnoughToBeHere = (income < schedule[1][0])
  if highEnoughToBeHere & lowEnoughToBeHere:
      return schedule[0]
  if True:
      return tuple_by_threshold( income, schedule[1:] )

def mk_pension ( formal : int,
                 indep  : int,
                 income : float
                ) -> float:
  if (not bool(formal)): return 0
  else:
    if indep:
      (_, compute_base, rate) = tuple_by_threshold (
        income,
        ss_contrib_schedule_for_contractor["pension"] )
      return compute_base( income ) * rate
    else:
      (_, compute_base, rate) = tuple_by_threshold (
        income,
        ss_contrib_schedule_for_employee["pension"] )
      return compute_base( income ) * rate

def mk_pension_employer ( formal : int,
                          indep  : int,
                          income : float
                         ) -> float:
  if bool(indep) | (not bool(formal)): return 0
  else:
    (_, compute_base, rate) = tuple_by_threshold (
      income,
      ss_contrib_schedule_by_employer["pension"] )
    return compute_base( income ) * rate
