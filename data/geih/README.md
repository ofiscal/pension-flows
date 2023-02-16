# Sanitized filenames

These are what I changed the file names to,
so that my console can display them:

## 2022

```
Caracteristicas generales, seguridad social en salud y educacion.csv
Datos del hogar y la vivienda.csv
 ddi-documentation-spanish-771.pdf
Fuerza de trabajo.csv
 Migracion.csv
No ocupados.csv
 Ocupados.csv
Otras formas de trabajo.csv
Otros ingresos e impuestos.csv
Tipo de investigacion.csv
```

## 2021

```
Cabecera_Otros-ingresos.csv
Resto_Caracteristicas-generales_Personas.csv
Resto_Desocupados.csv
Resto_Fuerza-de-trabajo.csv
Resto_Inactivos.csv
Resto_Ocupados.csv
Resto_Otras-actividades-y-ayudas-en-la-semana.csv
Resto_Otros-ingresos.csv
Resto_Vivienda-y-Hogares.csv
Cabecera_Caracteristicas-generales_Personas.csv
Cabecera_Desocupados.csv
Cabecera_Fuerza-de-trabajo.csv
Cabecera_Inactivos.csv
Cabecera_Ocupados.csv
Cabecera_Otras-actividades-y-ayudas-en-la-semana.csv
Cabecera_Vivienda-y-Hogares.csv
area_Desocupados.csv
area_Fuerza-de-trabajo.csv
area_Inactivos.csv
area_Ocupados.csv
area_Otras-actividades-y-ayudas-en-la-semana.csv
area_Otros-ingresos.csv
area_Caracteristicas-generales_Personas.csv
area_Vivienda-y-Hogares.csv
```

# PITFALL: The meaning of the identifier (primary key) columns

DIRECTORIO is a unique household ID.
It's not clear what ORDEN and SECUENCIA_P are.
It seems that all three variables are required
in order to uniquely identify a person.
To demonstrate that, try running the following code:

```
# DIR and ORD alone aren't enough to uniquely ID someone,
# because this seems to return multiple people.
ppl[ (ppl["DIR"] == 6007382) &
     (ppl["ORD"] == 1) ]

# DIR and SEC alone aren't enough to uniquely ID someone either,
# because this seems to return multiple people.
ppl[ (ppl["DIR"] == 6004277) &
     (ppl["SEC"] == 1 ) ]
```
