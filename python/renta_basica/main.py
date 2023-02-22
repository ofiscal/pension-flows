from   python.build.nov2022  import mkData
import python.renta_basica.lib as rb
from   python.types          import ( BasicIncome,
                                      BasicIncome_toDict,
                                      series_toBasicIncome )


if False: # Keeps it from running every time I run pytest
  df = mkData()
  scenarios = readScenarios()
  res = selected_reports( # or all_reports()
    df0       = df,
    scenarios = scenarios )
  res.to_excel ( "basic_income_simulations.xlsx" )
