# DEFINED HERE:
#
# def drop_none_values_from_dict ( d : Dict[Any,Any]
#                                 ) -> Dict[Any,Any]:
# def df_name_from_constraints (
#     basename             : str,
#     colname_colval_pairs : Dict[str, Any],
# ) -> str:
#
# def df_subset_from_constraintso (
#     df                   : pd.DataFrame,
#     colname_colval_pairs : Dict, # Dict[ s : str, v : type( df[s] ) ]
# ) -> pd.DataFrame :
#
# and tests for those.

import pandas as pd
from typing import List, Dict, Any
from python.get_data import mkData


def drop_none_values_from_dict ( d : Dict[Any,Any]
                                ) -> Dict[Any,Any]:
  # PITFALL: Keeps pairs for which k is None.
  return { k:v
           for k,v in d.items()
           if v != None }

def test_drop_none_values_from_dict ():
  assert ( drop_none_values_from_dict ( {1:2, 3:None, None:4} )
           == {1:2, None:4} )

def df_name_from_constraints (
    basename             : str,
    colname_colval_pairs : Dict[str, Any],
) -> str:
  name = basename
  for colname,colval in (
      drop_none_values_from_dict ( colname_colval_pairs )
      . items() ):
    name = name + "." + colname + "=" + str(colval)
  return name

def test_df_name_from_constraints ():
  assert (
    df_name_from_constraints (
      "bond",
      { "double-o"  : 7,
        "nemesis" : "Goldfinger" } )
    == "bond.double-o=7.nemesis=Goldfinger" )
  assert df_name_from_constraints("yo",{}) == "yo"

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
