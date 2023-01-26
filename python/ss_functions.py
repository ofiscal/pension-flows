# # TODO: Make this into a shared module.
#
# I've copied the functions in this folder from the microsimulation (tax.co).
# That's expedient but inelegant.
# Better to separate these into an independent module that both can import.

from typing import Tuple, List, Dict, Callable
import pandas as pd
from common import min_wage


Schedule = Tuple [ # PITFALL: Mypy does not recognize that typing exports GenericAlias,
                   # so to avoid that spurious warning I'm not signing Schedule's type.
  float,                       # minimum income threshold
  Callable [ [float], float ], # computes taxable base from wage
  float ]                      # average (not marginal!) tax rate

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

def mk_pension ( independiente : int,
                 income : float
                ) -> float:
  if independiente:
    (_, compute_base, rate) = tuple_by_threshold (
      income,
      ss_contrib_schedule_for_contractor["pension"] )
    return compute_base( income ) * rate
  else:
    (_, compute_base, rate) = tuple_by_threshold (
      income,
      ss_contrib_schedule_for_employee["pension"] )
    return compute_base( income ) * rate

def mk_pension_employer ( independiente : int,
                          income : float
                         ) -> float:
  if independiente: return 0
  else:
    (_, compute_base, rate) = tuple_by_threshold (
        income,
      ss_contribs_by_employer["pension"] )
    return compute_base( income ) * rate

ss_contrib_schedule_for_contractor : \
  Dict [ str,
         List [ Schedule ] ] = \
  { "pension" :
    [ ( 0, lambda _: 0, 0.0 )
    , ( min_wage
      , lambda wage: min( max ( 0.4*wage, min_wage ),
                          25*min_wage)
      , 0.16 ) ] }

ss_contrib_schedule_for_employee : \
  Dict [ str,
         List [ Schedule ] ] = \
  { "pension" :
    [ ( 0,           lambda wage: 0                             , 0.0  )
    , ( min_wage,    lambda wage: wage                          , 0.04 )
    , ( 13*min_wage, lambda wage: min ( 0.7*wage, 25*min_wage)  , 0.04 ) ] }

ss_contribs_by_employer : \
  Dict [ str,
         List [ Schedule ] ] = \
  { "pension" :
    [ ( 0,           lambda wage: 0                           , 0.0)
    , ( min_wage,    lambda wage: wage                        , 0.12)
    , ( 13*min_wage, lambda wage: min (0.7*wage, 25*min_wage) , 0.12) ] }
