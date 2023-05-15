# PURPOSE:
# Angie needs to know, for N in [1,2,3,infinity] (4 values),
# how many people earn up to N minimum wages,
# and what their total earnings are.

import pandas as pd

import python.build.nov2022_ish as n2
from python.common import min_wage_2022
from python.lib import near_nonzero


df0 = n2.read_marchThroughDec()

df1 = ( df0
        [[ "DIR", # household
           "ORD", # member of household
           "SEC",
           "month", # ANGIE: These data are person-month, not person. And it's not a panel; there are different people for each month. I am just taking the average over all observations, which means it's the average person-month. That is, I'm giving you a monthly figure. Moreover it only uses months March through Dec of 2022, because January and February were weird. It's possible that inflation causes weird effects -- wages might have risen over the year while the minimum wage stayed the same way. I see no way to control for that, so I won't.
           "weight",
           "labor income"]]
        . copy() )

# laborers with positive earnings
lpe = df1 [ df1["labor income"] > 0 ] . copy()
lpe [ "labor income, weighted" ] = ( lpe [ "labor income" ]
                                     * lpe [ "weight" ] )

report = pd.DataFrame()
for n in [1,2,3,9e99]:
  lpe_lim = ( lpe [ lpe ["labor income"]
                    <= n * min_wage_2022 ] )
  s = pd.Series ( lpe_lim.sum() )
  s["min wage threshold"] = ( str(n) if n < 9e9
                              else "infinity" )
  report = pd.concat ( [ report,
                         pd.DataFrame ( s ) . transpose() ],
                      axis = "rows" )

report = report [[ "weight",
                   "labor income, weighted",
                   "min wage threshold" ]]

if True: # reformat, and rename the reformatted things
  report = report.rename (
    columns = {"weight" : "n people",
               "labor income, weighted" : "labor income (billones)" } )
  report["n people"] = report["n people"] / 10
    # Because these are person-months, and from only have 10 months.
  report["labor income (billones)"] = ( # put it in billones COP
    report["labor income (billones)"] / 1e12 )

report
