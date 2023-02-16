from typing import List, Dict, Tuple


# PITFALL: There is no "ORDEN" (ORD) in the file
# `Datos del hogar y la vivienda.csv` for 2022.
primary_keys : List[str] = \
  ["DIR","SEC","ORD"]

dicts_to_rename_columns : Dict [ str, Dict [ str, str ] ] = {
  # PITFALL: 2021 and 2022 differ slightly.
  # This dictionary is only for variables they define the same way.
  "universal" : { "DIRECTORIO"  : "DIR",
                  "SECUENCIA_P" : "SEC",
                  "ORDEN"       : "ORD" },

  # PITFALL: The RHS of most of the string-string pairs below
  # are LIES, to begin with.
  # Only once the data is processed by some interpret_columns_ function
  # are those column names accurate.

  "caracteristicas_personales" : {
    "P6040" : "age" },

  "ocupados" : {
    "INGLABO" : "labor income",
    "P6920"   : "formal", # <=> Contributes to a pension.
    "P1879"   : "indep" # <=> if non-null, gave reason for working indep
  },

  "otros_ingresos" : { "P7500S2A1" : "pension income",
                       "P7500S1A1" : "rental income", },
}
