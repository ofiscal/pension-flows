from   dataclasses import dataclass
import pandas as pd
from   typing import Tuple, List, Dict, Callable


Schedule = Tuple [
  # PITFALL: Mypy does not recognize that typing exports GenericAlias,
  # so to avoid that spurious warning I'm not signing Schedule's type.
  float,                       # minimum income threshold
  Callable [ [float], float ], # computes taxable base from wage
  float ]                      # average (not marginal!) tax rate

@dataclass
class BasicIncome:
  subsidy_if_broke            : float # minimum wages per month
  when_subsidy_starts_to_wane : float # minimum wages per month
  when_subsidy_disappears     : float # minimum wages per month.
    # Should be bigger than `when_subsidy_starts_to_wane`.
  pensioners_excluded               : bool
  homeowners_excluded               : bool
  homeowners_implicit_income_counts : bool # Whether implicit homeowners income is included in total income when computing the subsidy amount.

def BasicIncome_toDict ( bi : BasicIncome
                        ) -> pd.Series:
  return pd.Series ( {
    "subsidy_if_broke"                  : bi.subsidy_if_broke,
    "when_subsidy_starts_to_wane"       : bi.when_subsidy_starts_to_wane,
    "when_subsidy_disappears"           : bi.when_subsidy_disappears,
    "pensioners_excluded"               : bi.pensioners_excluded,
    "homeowners_excluded"               : bi.homeowners_excluded,
    "homeowners_implicit_income_counts" : bi.homeowners_implicit_income_counts,
  } )

def series_toBasicIncome ( s : pd.Series
                          ) -> BasicIncome:
  return BasicIncome (
    subsidy_if_broke                  = s["subsidy_if_broke"],
    when_subsidy_starts_to_wane       = s["when_subsidy_starts_to_wane"],
    when_subsidy_disappears           = s["when_subsidy_disappears"],
    pensioners_excluded               = bool( s["pensioners_excluded"] ),
    homeowners_excluded               = bool( s["homeowners_excluded"] ),
    homeowners_implicit_income_counts =
      bool( s["homeowners_implicit_income_counts"] ) )
