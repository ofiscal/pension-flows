from os.path import join
import pandas as pd


datapath = "data/geih/2021-11/csv/"


### ### ### ### ### ###
### read the data   ###
### ### ### ### ### ###

## TODO : This is inefficient -- it reads everything, most of which is unneeded."

area = pd.read_csv(
  join ( datapath, "area_Ocupados.csv" ),
  sep = ";" )

cabecera = pd.read_csv(
  join ( datapath, "Cabecera_Ocupados.csv" ),
  sep = ";" )

resto = pd.read_csv(
  join ( datapath, "Resto_Ocupados.csv" ),
  sep = ";" )


### ### ### ### ### ###
### subset the data ###
### ### ### ### ### ###

area2 = (
  area [[ "fex_c_2011", "DIRECTORIO", "ORDEN",
          "INGLABO", "P6920", "P6430" ]]
  . copy()
  . rename (
    columns = { "fex_c_2011" : "weight",
                "INGLABO"    : "labor income",
                "P6920"      : "pension contrib",
                "P6430"      : "independiente" } ) )

cabecera2 = (
  cabecera [[ "fex_c_2011", "DIRECTORIO", "ORDEN",
              "INGLABO", "P6920", "P6430" ]]
  . copy()
  . rename (
    columns = { "fex_c_2011" : "weight",
                "INGLABO"    : "labor income",
                "P6920"      : "pension contrib",
                "P6430"      : "independiente" } ) )

resto2 = (
  resto [[ "fex_c_2011", "DIRECTORIO", "ORDEN",
           "INGLABO", "P6920", "P6430" ]]
  . copy()
  . rename (
    columns = { "fex_c_2011" : "weight",
                "INGLABO"    : "labor income",
                "P6920"      : "pension contrib",
                "P6430"      : "independiente" } ) )
