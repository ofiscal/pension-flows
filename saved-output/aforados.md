All data here are restricted to observations with positive labor income.

A "breadwinner" is defined as someone whose labor income is greater than 99% of household income. (An equality test would be dangerous for floating point error, but I could tighten that to 99.9 or whatever if needed.)


The unconditional mean value for formality is 41%:
```
mean    0.412056
Name: formal, dtype: float64
```

Here are some conditional means, conditioning on a single variable:

```
                        mean
breadwinner 4 kids
0.0                 0.424340
1.0                 0.355881

            mean
female
0       0.389286
1       0.441127

           mean
indep
0.0    0.650998
1.0    0.138654
```

Here are conditional means, conditioning on two variables:

```
                  mean
female indep
0      0.0    0.652523
       1.0    0.124367
1      0.0    0.649299
       1.0    0.160022

                              mean
breadwinner 4 kids indep
0.0                0.0    0.662146
                   1.0    0.146054
1.0                0.0    0.596893
                   1.0    0.106952

                               mean
breadwinner 4 kids female
0.0                0       0.398653
                   1       0.457175
1.0                0       0.346322
                   1       0.368017
```

Last, here are conditional means, conditioning on all three variables:
```
                                     mean
breadwinner 4 kids female indep
0.0                0      0.0    0.659599
                          1.0    0.133235
                   1      0.0    0.664957
                          1.0    0.165579
1.0                0      0.0    0.619080
                          1.0    0.084868
                   1      0.0    0.570970
                          1.0    0.137523
```
