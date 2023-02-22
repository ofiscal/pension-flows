# main

# contrib-to-pension--even-earning-less-than-the-minimum-wage

The GEIH has a measure of formality (P6920).
Since the ENPH doesn't, the tax.co microsiulation
implicitly imputes formality to anyone earning a minimum wage or more,
by assigning them pension (and other social security) contributions of zero.
That code was copied from tax.co into this repo.
This branch modifies the schedules in it,
such that even people who earn less than the minimum wage
contribute to pensions if they report doing doing so in P6920.

# mauricio-pension-contribs

Includes an alternative pension contribution variable
corresponding more or less to the one Mauricio computes.
