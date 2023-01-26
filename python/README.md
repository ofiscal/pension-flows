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
