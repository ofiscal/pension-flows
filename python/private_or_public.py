import matplotlib.pyplot as plt
import numpy as np
from   os.path import join
import pandas as pd
from   typing import List, Dict, Tuple, Any

from python.get_data import mkData
from python.common import min_wage

df = mkData()


# Money contributed to the public pension system.
df["to public"] = np.minimum (
  # Reasoning:
  # The first 160,000 COP of contributions go to the public system,
  # and the rest to the private one.
  df["employee contribs"] + df["employer contribs"],
  0.16 * min_wage )

# Money contributed to the private pension system.
df["to private"] = ( df["employee contribs"] +
                     df["employer contribs"] -
                     df["to public"] )

all_money     = ( ( df["to public"] +
                    df["to private"] )
                  * df["weight"] ) . sum()
public_money  = ( df["to public"]  * df["weight"] ) . sum()
private_money = ( df["to private"] * df["weight"] ) . sum()

print( "Total billones de COP per month to public system: ",
        public_money / 1e12 )
print( "Share going to public system: ",
        public_money / all_money )
print( "Total billones de COP per month to private system: ",
        private_money / 1e12 )
print( "Share going to private system: ",
        private_money / all_money )
