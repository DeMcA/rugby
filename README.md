rugby
=====

A simple script for calculating rugby world ranking scores given a set of results.


Calculating rankings
--------------------
Results may be entered manually with `-m` i.e.

`rugby.py -m Scotland 30 Australia 27`

or from a results file with `-f`FILENAME.
The file should have one result per line with the format:

Team1, Score1, Team2, Score2

Team1 is the home team unless the `-n` flag is set. 

