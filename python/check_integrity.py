# PURPOSE:
# This is not used by main.py.
# It justifies the deduplication performed in get_data.py

# USAGE:
# Just run the whole program and read the output.
# It includes instructions to a reader.
# To know what those instructions accomplish,
# read the comments below.


from typing import List, Dict, Tuple
import pandas as pd

from python.get_data import (
  dicts_to_rename_columns,
  interpret_columns_caracteristicas_personales,
  interpret_columns_ocupados,
  interpret_columns_otros_ingresos,
  raw_caracteristicas_generales_renamed,
  raw_ocupados_renamed,
  raw_otros_ingresos_renamed,
  )


# Verify there are no duplicates within a given source file,
# and that duplicates across files never disagree
# when they define the same thing.
def analyze_duplicates ( df : pd.DataFrame,
                         columns_to_analyze : List[str]
                        ): # IO : prints to screen
  # TODO : Currently this requires human interpretation.
  # It would be cool if it didn't.
  df["one"] = 1

  # Verify there are no duplicates within a given source file.
  print ( """HEY YOU! In the following printout, the "one" column in each data set should have a min of 1 and a max of 1. Otherwise there are duplicates""" )

  for c in df["source file"] . unique() :
    print ( df [ df [ "source file" ] == c ]
            . groupby ( ["DIR", "SEC", "ORD"] )
            . agg ( "sum" )
            . describe() . transpose() )

  # Verify duplicates are completely duplicate.
  # That is, any two rows with the same IDs [DIR, SEC and ORD]
  # have completely duplicate information
  # (at least in the columns I've kept from the raw data,
  # and excluding the "source file" column).
  # If that were not true, I would have to do some kind of magic
  # to create a single row from the divergent descriptions of a person.

  xmin = ( df
           . groupby ( ["DIR", "SEC", "ORD"] )
           . agg ( "min" )
           . reset_index() )

  xmax = ( df
           . groupby ( ["DIR", "SEC", "ORD"] )
           . agg ( "max" )
           . reset_index() )

  x = ( xmin [ ["DIR", "SEC", "ORD"] ]
        . copy() )

  for c in [ "weight",
             columns_to_analyze ]:
    x[c] = xmax[c] - xmin[c]

  print ( """HEY YOU! In the following printout, every non-ID column should have a standard deviation of zero. Otherwise, duplicates have different non-null values.""" )

  print ( x . describe() . transpose() )

ocup = interpret_columns_ocupados (
  raw_ocupados_renamed () )

cg = interpret_columns_caracteristicas_personales (
  raw_caracteristicas_generales_renamed () )

otros = interpret_columns_otros_ingresos (
  raw_otros_ingresos_renamed () )


for (df, nickname, columns_to_analyze) in [
  ( otros, "otros_ingresos",
    list ( dicts_to_rename_columns ["otros_ingresos"]
           . values() ) ),
  ( ocup, "ocupados",
    list ( dicts_to_rename_columns ["ocupados"]
           . values() ) ),
  ( cg, "caracteristicas_personales",
    list ( dicts_to_rename_columns ["caracteristicas_personales"]
          . values() ) ),
    ]:
  print()
  print("=========== Analyzing " + nickname + " ===========")
  analyze_duplicates(df, columns_to_analyze)
