import pandas as pd
from typing import List, Dict
from python.get_data import mkData


def df_subset_from_constraints (
    df     : pd.DataFrame,
    colname_colval_pairs : Dict,
      # PITFALL: colname_colval_pairs has a dependent type
      # -- specifically Dict[ s : str,
      #                       v : type( df[s] ) ]
) -> pd.DataFrame :
  """Given a dictionary of constraints of the form { column_name : value },returns the subset of `df` satisfying those constraints. If there are no constraints, it returns all of `df`."""
  def subsetter ( df : pd.DataFrame,
                  colname : str,
                  colval # PITFALL: Dependent type.
                         # type(colval) = type( df[colname] )
                 ) -> pd.DataFrame:
    return df[ df[colname] == colval]

  for k,v in colname_colval_pairs.items():
    df = subsetter ( df, k, v )
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
