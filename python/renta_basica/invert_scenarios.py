# Earlier versions of this code stated criteria for receiving the basic icnome
# in terms of inclusion, but exclusion proved easier to communicate.
# This code allows conversion of "scenarios.csv"
# from the "inclusion" syntax to the "exclusion" syntax.
# Reversing it, if necessary, should be straightforward.

import pandas as pd

rename_dict = {"pensioners_included" : "pensioners_excluded",
               "homeowners_included" : "homeowners_excluded", }
newNames = rename_dict.values()

scenarios = (
  pd.read_csv ( "python/renta_basica/scenarios.csv" )
  . rename ( columns = rename_dict ) )

original = scenarios.copy()

for c in newNames:
  scenarios[c] = scenarios[c] . apply (
    lambda i :
      int ( not ( bool ( i ) ) ) )
converted = scenarios.copy()

# The change is what I wanted.
assert ( original[newNames]
         . equals (
           (1-converted[newNames] ) ) )

# The rest is unchanged.
assert ( original.drop( columns = newNames )
         . equals(
           converted.drop( columns = newNames ) ) )

converted.to_csv( "python/renta_basica/scenarios.csv" )
