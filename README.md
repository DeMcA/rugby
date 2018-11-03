rugby
=====

A simple script for calculating rugby world ranking scores given a set of results.


Calculating rankings
--------------------
Results may be entered manually with `-m` i.e.

`rugby.py -m Scotland 30 Australia 27`

or from a results file with `-f FILENAME`.
The file should have one result per line with the format:

Team1, Score1, Team2, Score2

Team1 is the home team unless the `-n` flag is set. 

Notes
-----
I wrote this a while ago when I wanted to see what would happen after a round of matches before the official rankings were updated.
Then I got carried away and added the command line switches, presumably I was playing with docopt at the time. 
Recently I was going back through some old code and did a bit of a cleanup while I was looking at this.
There's a whole load of improvements that could doubtless be made: port to python3, a scraper for nicely formatted, up-to-date rankings, the options should be consistent, etc.
Perhaps when I next feel like brushing up my python. 

There are of course far more complete solutions out there, for example:
https://rawling.github.io/wr-calc/

For the current official rankings:
https://www.world.rugby/rankings/mru
