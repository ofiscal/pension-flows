# These are single-key {"pension" : _}dictionaries,
# which is a little silly.
# They are like that because this code was copied,
# only in relevant part, from the tax.co microsimulation,
# where they have other keys too.

from typing import Tuple, List, Dict, Callable

from python.common import min_wage_2022
from python.types import Schedule


min_wage = min_wage_2022

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

ss_contrib_schedule_by_employer : \
  Dict [ str,
         List [ Schedule ] ] = \
  { "pension" :
    [ ( 0,           lambda wage: 0                           , 0.0)
    , ( min_wage,    lambda wage: wage                        , 0.12)
    , ( 13*min_wage, lambda wage: min (0.7*wage, 25*min_wage) , 0.12) ] }
