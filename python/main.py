from typing import List, Dict, Tuple
import pandas as pd

from python.get_data import fetch_all


# PITFALL: Mypy can't handle type signatures here --
# neither inside the tuple, nor of it.
( area, cabecera, resto ) = fetch_all ()
