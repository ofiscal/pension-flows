import pandas as pd

import python.build.nov2022_ish as n2
from python.common import min_wage_2022
from python.lib import near_nonzero


df = n2.read_marchThroughDec()


#####################################
#### Create wage bucket columns. ####
#####################################

min_wage_buckets = [
  # Each of these is a (minimum, supremum) pair.
  ( 0, 1 ),
  ( 1, 1.5 ),
  ( 1.5, 3 ),
  ( 3, 9e300 ) ] # 9e300 min wages is effectively infinity

def rangeString ( iMin : float, iSup : float ) -> str:
  return "in [" + str(iMin) + "," + str(iSup) + ") sm"

# Defines a boolean series.
def labor_income_is_in_range ( a : float, b : float ) -> pd.Series:
  return ( ( df["labor income"] >= a ) &
           ( df["labor income"] < b ) )

def labor_income_in_range ( a : float, b : float ) -> pd.Series:
  return ( df["labor income"]
           . apply ( lambda i:
                     max ( 0,
                           min ( b-a,
                                 i-a ) ) ) )

for (iMin, iSup) in min_wage_buckets:
  df["earns " + rangeString ( iMin, iSup ) ] = \
    labor_income_is_in_range ( iMin * min_wage_2022,
                               iSup * min_wage_2022 )
  df["earnings " + rangeString ( iMin, iSup ) ] = \
    labor_income_in_range ( iMin * min_wage_2022,
                            iSup * min_wage_2022 )


###################
#### Two tests ####
###################

df["one"] = 1

# Verify that the boolean "earns*" variables partition the observations.

assert ( ( df["one"].sum() ) ==
         ( df[ [ "earns " + rangeString(iMin,iSup)
                 for (iMin,iSup) in min_wage_buckets ] ]
           . sum()
           . sum() ) )

# Verify that the continuous "earnings*" variables add up to "labor income".

df["earnings sum"] = (
  df[ [ "earnings " + rangeString(iMin,iSup)
        for (iMin,iSup) in min_wage_buckets ] ]
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
  df = df.drop( columns = { "one",
                            "earnings sum",
                            "earnings sum near labor income", } )


###################################################################
#### New dataset: Limit to formal workers, and weight each row ####
###################################################################

formal = df[ df["formal"] > 0 ]
formal = formal.rename( columns = {"one" : "people"} )

for c in [ "people",
           "earns in [0,1) sm",
           "earns in [1,1.5) sm",
           "earns in [1.5,3) sm",
           "earns in [3,9e+300) sm",
           "labor income",
           "earnings in [0,1) sm",
           "earnings in [1,1.5) sm",
           "earnings in [1.5,3) sm",
           "earnings in [3,9e+300) sm",]:
  formal[c] = formal[c] * formal["weight"]


#################
#### Results ####
#################

print ( "People (millions):" )
print ( formal [[ "people",
                  "earns in [0,1) sm",
                  "earns in [1,1.5) sm",
                  "earns in [1.5,3) sm",
                  "earns in [3,9e+300) sm", ]]
        . sum()
        / (1e6 * 10) ) # These observations are person-months, so this division results in a number of millions of people. (Divide by 10, not 12, because we only have 10 months -- Jan and Feb were omitted because Jan is ugly and Feb seems like an outlier, the pandemic was ending and wages were very different.)

print ( "" )
print ( "Money (billones per year)" )
print ( formal [[ "labor income",
                "earnings in [0,1) sm",
                 "earnings in [1,1.5) sm",
                 "earnings in [1.5,3) sm",
                 "earnings in [3,9e+300) sm", ]]
       . sum()
       / 1e12 )
