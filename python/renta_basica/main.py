from python.build.nov2022    import mkData
from python.renta_basica.lib import ( readScenarios,
                                      all_reports,
                                      selected_reports )


if False: # Keeps it from running every time I run pytest
  df = mkData()
  scenarios = readScenarios()
  res = all_reports( # or selected_reports()
    df        = df,
    scenarios = scenarios )
  res.to_excel ( "basic_income_simulations.all-144.xlsx" )
