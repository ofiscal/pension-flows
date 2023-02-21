# DEFINED HERE:
#
# def drop_none_values_from_dict ( d : Dict[Any,Any]
#                                 ) -> Dict[Any,Any]:
# def df_name_from_constraints (
#     colname_colval_pairs : Dict[str, Any],
# ) -> str:
#
# def df_subset_from_constraints (
#     df                   : pd.DataFrame,
#     colname_colval_pairs : Dict, # Dict[ s : str, v : type( df[s] ) ]
# ) -> pd.DataFrame :
#
# and tests for those.

import pandas as pd
from typing import List, Dict, Any
from python.build.nov2022 import mkData


def near_nonzero (a : float, b : float) -> bool:
  # TODO: This should be part of ofiscal_utils.
  # tax.co has a similar, better function.
  """Verifies that its two inputs are within 1% of each other."""
  return ( False
           if a < (0.99*b)
           else ( False if b < (0.99*a)
                  else True ) )

def test_near_nonzero ():
  assert near_nonzero(0.5,1) == False
  assert near_nonzero(1,0.5) == False

  assert near_nonzero(1,1.00001) == True
  assert near_nonzero(1.00001,1) == True

def drop_none_values_from_dict ( d : Dict[Any,Any]
                                ) -> Dict[Any,Any]:
  # PITFALL: Keeps pairs for which k is None.
  return { k:v
           for k,v in d.items()
           if v != None }

def test_drop_none_values_from_dict ():
  assert ( drop_none_values_from_dict ( {1:2, 3:None, None:4} )
           == {1:2, None:4} )

def constraint_string (
    colname_colval_pairs : Dict[str, Any],
) -> str:
  name = ""
  for colname,colval in (
      drop_none_values_from_dict ( colname_colval_pairs )
      . items() ):
    name = name + "." + colname + "=" + str(colval)
  return name

def test_constraint_string ():
  assert (
    constraint_string (
      { "double-o"  : 7,
        "nemesis" : "Goldfinger" } )
    == ".double-o=7.nemesis=Goldfinger" )
  assert constraint_string ({}) == ""

def df_subset_from_constraints (
    df                   : pd.DataFrame,
    colname_colval_pairs : Dict,
      # PITFALL: colname_colval_pairs has a dependent type
      # -- specifically Dict[ s : str,
      #                       v : type( df[s] ) ]
) -> pd.DataFrame :
  """Given a dictionary of constraints of the form { column_name : value },returns the subset of `df` satisfying those constraints. If there are no constraints, it returns all of `df`."""
  for colname,colval in (
      drop_none_values_from_dict ( colname_colval_pairs )
      . items() ):
    df = df[ df[colname] == colval]
  return df

def test_df_subset_from_constraints ():
  df = pd.DataFrame (
    { "female"  : [0,0,0,0,1,1,1,1],
      "indep"   : [0,0,1,1,0,0,1,1],
      "beetles" : [0,1,0,1,0,1,0,1] } )
  assert ( df_subset_from_constraints ( df,
                                        { "female" : 1,
                                          "indep" : 0 } )
           . equals ( df[ (df["female"] == 1) &
                          (df["indep"]  == 0) ] ) )
  assert ( df_subset_from_constraints ( df, {} )
           . equals ( df ) )
