# PITFALL: There are a couple of important TODO comments below,
# regarding the interpretation (monthly vs. yearly) of income sums.

import pandas as pd
#
import python.build.nov2022_ish as n2
from python.common import min_wage_2022
from python.lib import near_nonzero


df = n2.read_marchThroughDec()


#####################################
#### Create wage bucket columns. ####
#####################################

min_wage_buckets = [
  # Each of these is an (infimum, max) pair.
  ( 0, 1 ), # Income is never negative, so this includes people with 0 income. (If I put 0 instead of -1, those people would be excluded, because these are treated as half-open "(]" intervals, i.e. not including the infimum -- see the definition of `labor_income_is_in_range` below.)
  ( 1, 2 ),
  ( 2, 3 ),
  ( 3, 9e300 ) ] # 9e300 min wages is effectively infinity

def rangeString ( iInf : float, iMax : float ) -> str:
  return "in [" + str(iInf) + "," + str(iMax) + ") sm"

# Defines a boolean series.
def labor_income_is_in_range ( a : float, b : float ) -> pd.Series:
  return ( ( df["labor income"] > a ) &
           ( df["labor income"] <= b ) )

# Defines a float series.
def labor_income_in_range ( a : float, b : float ) -> pd.Series:
  return ( df["labor income"]
           . apply ( lambda i:
                     max ( 0,
                           min ( b-a,
                                 i-a ) ) ) )

for (iInf, iMax) in min_wage_buckets:
  df["earns " + rangeString ( iInf, iMax ) ] = \
    labor_income_is_in_range ( iInf * min_wage_2022,
                               iMax * min_wage_2022 )
  df["earnings " + rangeString ( iInf, iMax ) ] = \
    labor_income_in_range ( iInf * min_wage_2022,
                            iMax * min_wage_2022 )


###################
#### Two tests ####
###################

df["one"] = 1

# Verify that the boolean "earns*" variables partition the observations.

df_nonzero = df[ df["labor income"] > 0 ]
assert ( ( df_nonzero["one"].sum() ) ==
         ( df_nonzero[ [ "earns " + rangeString(iInf,iMax)
                         for (iInf,iMax) in min_wage_buckets ] ]
           . sum()
           . sum() ) )

# Verify that the continuous "earnings*" variables add up to "labor income".

df["earnings sum"] = (
  df[ [ "earnings " + rangeString(iInf,iMax)
        for (iInf,iMax) in min_wage_buckets ] ]
  . sum ( axis = "columns" ) )

df["earnings sum near labor income"] = df.apply (
  lambda row: near_nonzero ( row["labor income"],
                             row["earnings sum"],
                             1),
  axis = "columns" )

assert ( df["earnings sum near labor income"]
         . equals(
           df["one"] . astype(bool) ) )

if False: # optional: clean up temporary variables
  del(df_nonzero)
  df = df.drop( columns = { "one",
                            "earnings sum",
                            "earnings sum near labor income", } )


###################################################################
#### New dataset: Limit to formal workers,
#### compute hypothetical pensions,
###################################################################

## PITFALL: These hypothetical pensions are what these people *would* receive
## in the future. I am computing them for workers,
## not for people currently receiving pensions.

formal = df[ df["formal"] > 0 ]
formal = formal.rename( columns = {"one" : "people"} )
def pension_pilares ( income : float ) -> float:
  return max ( min_wage_2022,
               ( 0.65 * min ( income, 3 * min_wage_2022 ) +
                 0.35 * max ( 0, income - 3 * min_wage_2022 ) ) )

def pension_private_now ( income : float ) -> float:
  return max ( min_wage_2022,
               0.35 * income )

def pension_public_now ( income : float ) -> float:
  return max ( min_wage_2022,
               0.65 * income )

# For manual testing below.
testDf = pd.DataFrame ( {"labor income" :
                         [ n/2 * min_wage_2022
                           for n in range (0,21) ] } )

for (name,func) in [ ("pension, public now", pension_public_now),
                     ("pension, private now", pension_private_now),
                     ("pension, pilares", pension_pilares) ]:
  formal[name] = formal["labor income"].apply(func)
  testDf[name] = testDf["labor income"].apply(func)
    # Manual test: compare testDf to `./pension-examples.xlsx`

formal["subsidy decrease over public pensions"] = (
  formal["pension, public now"] -
  formal["pension, pilares"] )
formal["subsidy increase over private pensions"] = (
  formal["pension, pilares"] -
  formal["pension, private now"] )


################################
#### Weight all relevant columns
################################

## PITFALL: These rows are no longer meaningful on their own --
## only their sums are.
##
## TODO : There's probably a nicer way to do this,
## with a "weight" argument to the sum() function.

for c in [ "people", # PITFALL: Really this is person-months at this point.
           "earns in [0,1) sm",
           "earns in [1,2) sm",
           "earns in [2,3) sm",
           "earns in [3,9e+300) sm",
           "labor income",
           "earnings in [0,1) sm",
           "earnings in [1,2) sm",
           "earnings in [2,3) sm",
           "earnings in [3,9e+300) sm",
           "pension, pilares",
           "pension, private now",
           "pension, public now",
           "subsidy increase over private pensions",
           "subsidy decrease over public pensions",]:
  formal[c] = formal[c] * formal["weight"]


#################
#### Results ####
#################

print ( "People (millions):" )
print ( formal [[ "people",
                  "earns in [0,1) sm",
                  "earns in [1,2) sm",
                  "earns in [2,3) sm",
                  "earns in [3,9e+300) sm", ]]
        . sum()
        / ( 1e6 * # Divide by this to put results in millions.
            10) ) # Divide by this to put results in persons, not person-months. (We only have 10 months; January was weirdly formatted and February had strange wage data, probably because it's the tail of the pandemic.)

print ( "" )
print ( "Money (billones per year)" ) # TODO : Reading the code above, it seems like these figures should be monthly, not yearly. But the numbers look yearly, not monthly.
#
# TODO : Scale the "annual" sums of earnings by 12/10,
# since January and February are omitted.
# (They are omitted on purpose,
# because they were strange in 2022.)

print ( formal [[ "labor income",
                  "earnings in [0,1) sm",
                  "earnings in [1,2) sm",
                  "earnings in [2,3) sm",
                  "earnings in [3,9e+300) sm", ]]
        . sum()
        * (12/10) # Expand these 10 months to be what a year would be.
        / 1e12 ) # Divide by this to put results in billones.

for (who,col) in [
    ("earns in [2,3) sm",   "subsidy increase over private pensions"),
    ("earns in [3,9e+300) sm","subsidy decrease over public pensions"), ]:
  print("")
  print( col + " for people in " + who )
  print ( formal
          [ formal [ who ] > 0 ]
          [col]
          . sum()
          * (12/10) # Expand these 10 months to be what a year would be.
          / 1e12 ) # Divide by this to put results in billones.
