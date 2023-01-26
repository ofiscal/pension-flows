from typing import List, Dict, Tuple
import pandas as pd

from python.get_data import fetch_all


# Type signature pitfall: Python (3.9, at least)
# can't handle a type signatures here --
# neither inside the tuple, nor of it.
( area, cabecera, resto ) = fetch_all ()
