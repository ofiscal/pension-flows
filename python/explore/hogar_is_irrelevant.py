# PURPOSE:
# Show that HOGAR is redundant, everywhere equal to SECUENCIA_P.

# USAGE | PITFALL:
# This requires modifying python.build.nov2021
# by inserting the line
#   "HOGAR" : "HOG",
# into the definition of `dicts_to_rename_columns["universal"]`.
# This makes the (redundant) HOGAR variable available.

cg = interpret_columns_caracteristicas_personales (
  deduplicate_rows (
    raw_caracteristicas_generales_renamed () ) )
otros = interpret_columns_otros_ingresos (
  deduplicate_rows (
    raw_otros_ingresos_renamed () ) )
ocup = mk_pension_contribs (
  interpret_columns_ocupados (
    deduplicate_rows (
      raw_ocupados_renamed () ) ) )

pkh = primary_keys + ["HOG"]
df = pd.concat ( [ cg[pkh],
                   ocup[pkh],
                   otros[pkh], ] )
s = df["SEC"] == df["HOG"]
s.describe()
s.isnull().sum()
