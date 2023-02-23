# PURPOSE:
# These are single-key {"pension" : _}dictionaries,
# which is a little silly.
# They are like that because this code was copied,
# only in relevant part, from the tax.co microsimulation,
# where they have other keys too.
#
# PITFALL:
# Since the GEIH allows us to capture formality directly,
# these schedules apply the same formula
# to people earning less than a minimum wage
# and to people earning slightly more than a minimum wage.
# These schedules therefore differ from those in tax.co,
# which uses the ENPH and therefore can use no direct measure of formality.
# tax.co instead imputes informality
# to anybody making less than a minimum wage,
# assigning them social security (and in particular, pension)
# contributions of zero.

from typing import Tuple, List, Dict, Callable

from python.common import min_wage_2022
from python.types import Schedule


min_wage = min_wage_2022

ss_contrib_schedule_for_contractor : \
  Dict [ str,
         List [ Schedule ] ] = \
  { "pension" :
    [ ( 0
      , lambda wage: min( max ( 0.4*wage, min_wage ),
                          25*min_wage)
      , 0.16 ) ] }

ss_contrib_schedule_for_employee : \
  Dict [ str,
         List [ Schedule ] ] = \
  { "pension" :
    [ ( 0,           lambda wage: wage                          , 0.04 )
    , ( 13*min_wage, lambda wage: min ( 0.7*wage, 25*min_wage)  , 0.04 ) ] }

ss_contrib_schedule_by_employer : \
  Dict [ str,
         List [ Schedule ] ] = \
  { "pension" :
    [ ( 0,           lambda wage: wage                        , 0.12)
    , ( 13*min_wage, lambda wage: min (0.7*wage, 25*min_wage) , 0.12) ] }
