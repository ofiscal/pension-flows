import matplotlib.pyplot as plt
import numpy as np
from   os.path import join
import pandas as pd
from   typing import List, Dict, Tuple, Any

import python.build.nov2022 as nov2022
from python.common import min_wage_2022


if True: # make data
  df22 = nov2022.mkData()

  df22["total contribs"] = ( df22["employee contribs"] +
                             df22["employer contribs"] )

  df22["young"] = ( ( (df22["age"] < 47) &
                      (df22["female"] == 1) ) |
                    ( (df22["age"] < 52) &
                      (df22["female"] == 0) ) )

  young = df22[   df22["young"] ] . copy()
  old   = df22[ ~ df22["young"] ] . copy()

def young_old_split (): # pure IO (prints to screen)
  contribs       = ( df22 ["total contribs"] * df22 ["weight"] ). sum()
  young_contribs = ( young["total contribs"] * young["weight"] ). sum()
  old_contribs   = ( old  ["total contribs"] * old  ["weight"] ). sum()

  print ( "Total (billones de COP per month) contributions by males age < 52 and females age < 47: ", str( young_contribs / 1e12 ) )
  print ( "Share contributed by males age < 52 and females age < 47: ", str( young_contribs / contribs ) )
  print ( "Total (billones de COP per month) contributions by males age >= 52 and females age >= 47: ", str( old_contribs / 1e12 ) )
  print ( "Share contributed by males age >= 52 and females age >= 47: ", str( old_contribs / contribs ) )

def public_private_split (
    nickname : str,
    min_wages_to_public_fund : float, # The SS contributsions from at most this many minimum wages will go to the public fund. SS contributions pulled from any wages beyond this threshold will go to the private fund.
    df : pd.DataFrame,
): # pure IO (prints to screen)
  # Money contributed to the public pension system.
  df["to public"] = np.minimum (
    # Reasoning:
    # The first 160,000 COP of contributions go to the public system,
    # and the rest to the private one.
    df["total contribs"],
    0.16 * min_wages_to_public_fund * min_wage_2022 )

  # Money contributed to the private pension system.
  df["to private"] = ( df["total contribs"] -
                       df["to public"] )

  all_money     = ( ( df["to public"] +
                      df["to private"] )
                    * df["weight"] ) . sum()
  public_money  = ( df["to public"]  * df["weight"] ) . sum()
  private_money = ( df["to private"] * df["weight"] ) . sum()

  return pd.Series ( {
    "sample" : nickname,
    "threshold" : min_wages_to_public_fund,
    "public billones COP / month" : public_money / 1e12,
    "public share" : public_money / all_money,
    "private billones COP / month" : private_money / 1e12,
    "private share" : private_money / all_money } )

young_old_split()

def table_results ( nRows : int,
                    max_threshold_in_millones = 5) -> pd.DataFrame:
  acc = []
  for (nickname,df) in [
      ("November 2022 (male age < 52) or (female age < 47)", young),
      ("November 2022", df22) ]:
    for threshold in [ 5 * i/max_threshold_in_millones
                       for i in range(1, nRows + 1) ]:
      acc.append (
        public_private_split (
          nickname                 = nickname,
          min_wages_to_public_fund = threshold,
          df                       = df ) )
  return pd.DataFrame ( acc )

for nRows in [5,500]:
  ( table_results ( nRows = nRows )
    . to_excel ( "private public pension splits, " + str(nRows) + " rows.xlsx" ) )
