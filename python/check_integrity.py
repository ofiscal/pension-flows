# PURPOSE:
# This is not used by main.py but it's important.
# It verifies that the data makes sense,
# such that I can reasonably do what I'm doing with it.

# USAGE:
# Just run the whole program and read the output.
# It includes instructions to a reader.
# To know what those instructions accomplish,
# read the comments below.


from typing import List, Dict, Tuple
import pandas as pd

from python.get_data import ( interpret_columns_ocupados,
                              raw_ocupados_renamed )


ppl = interpret_columns_ocupados (
  raw_ocupados_renamed () )

ppl["one"] = 1

# Verify there are no duplicates within a given source file.
print ( """HEY YOU! In the following printout, the "one" column in each data set should have a min of 1 and a max of 1.""" )

for c in ppl["source file"] . unique() :
  print ( ppl [ ppl [ "source file" ] == c ]
          . groupby ( ["DIR", "SEC", "ORD"] )
          . agg ( "sum" )
          . describe () )

# Verify duplicates are completely duplicate.
# That is, any two rows with the same IDs [DIR, SEC and ORD]
# have completely duplicate information
# (at least in the columns I've kept from the raw data,
# and excluding the "source file" column).
# If that were not true, I would have to do some kind of magic
# to create a single row from the divergent descriptions of a person.

xmin = ( ppl
         . groupby ( ["DIR", "SEC", "ORD"] )
         . agg ( "min" )
         . reset_index() )

xmax = ( ppl
         . groupby ( ["DIR", "SEC", "ORD"] )
         . agg ( "max" )
         . reset_index() )

x = ( xmin [ ["DIR", "SEC", "ORD"] ]
      . copy() )

for c in [ "weight",
           "labor income", "contributes to pension", "independiente" ]:
  x[c] = xmax[c] - xmin[c]

print ( """HEY YOU! In the following printout, every non-ID column should have a standard deviation of zero.""" )

print ( x.describe() )
