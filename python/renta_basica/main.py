import pandas as pd
from python.build.nov2022_ish import mkMonth
from python.renta_basica.lib  import ( all_reports,
                                       selected_reports )


if False: # Keeps it from running every time I run pytest
  df = mkMonth( month = 11 )
  scenarios = pd.read_csv(
    "python/renta_basica/scenarios.csv" )
  res = selected_reports( # or all_reports()
    df        = df,
    scenarios = scenarios )
  res.to_excel ( "output/basic_income_simulations.selected.xlsx" )
