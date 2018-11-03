#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Rugby Rankings Program

Usage:
    rugby.py [-htpl <number> -m <team1> <score1> <team2> <score2> [-wn] -f FILE -i INPUT -o OUTPUT]

Arguments:
    <team1>
    <score1>
    <team2>
    <score2>

Options:
    -h, --help                      Prints this help message
    -p, --print                     Print rankings
    -l [<num>], --lines [<num>]     Number of lines to print
    -i INPUT                        Input File, rankings as csv
    -o OUTPUT                       Output File, rankings as csv
    -f FILE                         Results file, one result per line
    -t, --test                      Does nothing
    -m, --match                     Match
    -w                              World Cup match (default: False)
    -n                              Neutral ground (default: False)
"""

import csv
import operator
import docopt
import sys


teams = {}
def read_rankings(INFILE):
    try:
        with open(INFILE, 'r') as f:
            reader = csv.reader(f, skipinitialspace=True)
            for row in reader:
                name = row.pop(1)
                teams[name] = float(row[1])
    except IOError:
        print "Must supply a ranking file with '-i' if rankings.txt is missing"
        print "file format:\n"
        print "1,New Zealand,92.01"
        print "...\n"
        sys.exit(0)


def print_rankings(upper):
    rankings = sorted(teams.items(), key=operator.itemgetter(1), reverse=True)
    for i in range(0, upper):
        print i+1, rankings[i][0], rankings[i][1]


class Match(object):

    def __init__(self, teamA, scoreA, teamB, scoreB, neutral=False, wc=False):
        self.teamA = teamA
        self.teamB = teamB
        self.rankA = teams[teamA]
        self.rankB = teams[teamB]
        if not neutral:
            self.rankA += 3
        self.gap = self.rankB - self.rankA # Initial gap in rankings
        self.diff = int(scoreA) - int(scoreB) # Score difference for this match
        self.delta = 0 # The change that will be applied to the ranking values
        self.wc = wc # World cup match flag

    def calc_core(self):
        self.delta = self.alt_calc_match_delta()
        if abs(self.diff) > 15:
            self.delta *= 1.5
        if self.wc is True:
            self.delta *= 2

    def alt_calc_match_delta(self):
    '''
    An alternative way of calculating match deltas

    All possible deltas are fetched from an array,
    idx defaults to win vs poor ranked (large negative gap) team
    First if/elif: idx is increased on lose or draw conditions
    Second if/elif: idx is increase on playing much higher ranked or similarrly ranked team

    Just in as a demo, not a very clear way of doing this.
    '''
        deltas = [0,2,0.1*self.gap+1,-2,0,0.1*self.gap-1,-1,1,0.1*self.gap]
        idx = 0
        if self.diff < 0:
            idx += 3
        elif self.diff == 0:
            idx += 6
        if self.gap >= 10:
            idx += 1
        elif self.gap >= -10:
            idx += 2
        return deltas[idx]


    def calc_match_delta(self):
    '''
    Standard method for calulating match deltas, using nested if statements.
    Ranking gap comparisons in separate functions for readability
    '''
        if self.diff > 0: # Home team wins
            return self.win()
        elif self.diff < 0:
            return self.lose()
        elif self.diff == 0:
            return self.draw()

    def win(self):
        if self.gap <= -10:
            return 0
        if self.gap >= 10:
            return 2
        else:
            return 0.1*self.gap + 1

    def lose(self):
        if self.gap <= -10:
            return -2
        if self.gap >= 10:
            return 0
        else:
            return 0.1*self.gap -1

    def draw(self):
        if self.gap <= -10:
            return -1
        if self.gap >= 10:
            return 1
        else:
            return 0.1*self.gap

    def update_teams(self):
        teams[self.teamA] += self.delta
        teams[self.teamB] -= self.delta


if __name__ == '__main__':
    a = docopt.docopt(__doc__)
    if a['-i']:
        INPUT = a['-i']
    else:
        INPUT = 'rankings.txt'
    read_rankings(INPUT)
    if a['--lines'] is None:
        number = len(teams)
    else:
        number = a['--lines']
    if a['--match']:
        m = Match(a['<team1>'], a['<score1>'], a['<team2>'], a['<score2>'],
                  neutral=a['-n'], wc=a['-w'])
        m.calc_core()
        print "Rankings change:", m.delta
        print
        m.update_teams()
    if a['-f']:
        with open(a['-f'], 'r') as f:
            reader = csv.reader(f, skipinitialspace=True)
            for row in reader:
                m = Match(row[0], row[1], row[2], row[3], neutral=a['-n'],
                          wc=a['-w'])
                m.calc_core()
                m.update_teams()

    if a['-o']:
        OUTPUT = a['-o']
        rankings = sorted(teams.items(), key=operator.itemgetter(1), reverse=True)
        f = open(OUTPUT, 'w')
        for i in range(len(rankings)):
            f.write(str(i+1)+", "+str(rankings[i][0])+", "+str(rankings[i][1])+"\n")
        f.close()

    if a['--print']:
        print_rankings(int(number))
