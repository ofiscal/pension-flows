from typing import Tuple, List, Dict, Callable


Schedule = Tuple [
  # PITFALL: Mypy does not recognize that typing exports GenericAlias,
  # so to avoid that spurious warning I'm not signing Schedule's type.
  float,                       # minimum income threshold
  Callable [ [float], float ], # computes taxable base from wage
  float ]                      # average (not marginal!) tax rate
