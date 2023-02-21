from typing import Tuple, List, Dict, Callable
from dataclasses import dataclass


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
  pensioners_included               : bool
  homeowners_included               : bool
  homeowners_implicit_income_counts : bool # Whether implicit homeowners income is included in total income when computing the subsidy amount.
