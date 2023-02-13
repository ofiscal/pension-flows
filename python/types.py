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
  subsidy_if_broke            : float # COP per month
  when_subsidy_starts_to_wane : float # COP per month
  when_subsidy_disappears     : float # COP per month.
    # Should be bigger than `when_subsidy_starts_to_wane`.
