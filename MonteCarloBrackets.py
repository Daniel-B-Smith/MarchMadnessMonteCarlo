#!/usr/bin/env python
from __future__ import division
import numpy as np
import pylab as pl
from random import choice, shuffle
from numpy.random import random #import only one function from somewhere
from numpy.random import randint
from numpy import exp, array, zeros
import scipy
from time import sleep
from copy import deepcopy
from collections import Counter, OrderedDict

import RankingsAndStrength as RAS
import Visualization

import Brackets
from Brackets import Bracket
import Stats

regional_rankings = RAS.regional_rankings
#strength = RAS.kenpom['Luck']
#strength = RAS.sagarin['Rating']
strength = RAS.kenpom['Pyth']

#T = 0.5 # In units of epsilon/k
#T = 2.5 # In units of epsilon/k

def energy_game(winner, loser):
    """This is where you'll input your own energy functions. Here are
    some of the things we talked about in class. Remember that you
    want the energy of an "expected" outcome to be lower than that of
    an upset.

    """
    result = -(strength[winner] - strength[loser])
    result = regional_rankings[winner] - regional_rankings[loser]
    result = regional_rankings[winner]/regional_rankings[loser]
    result = -(strength[winner]/strength[loser])
    #result = random()
    #result = color of team 1 jersey better than color of team 2 jersey
    #print "energy_game(",winner,loser,")",result
    return result

def energy_of_flipping(current_winner, current_loser):
    """Given the current winner and the current loser, this calculates
    the energy of swapping, i.e. having the current winner lose.
    """
    return (energy_game(current_loser, current_winner) - 
            energy_game(current_winner, current_loser))

#@profile
def simulate(ntrials, region, T, printonswap=False, showvis=True, newfig=False,
             teamdesc=None, printbrackets=True):
    """
    If region is "west" "midwest" "south" or "east" we'll run a bracket based 
    just on those teams.
    If it's "all" we'll run a full bracket.
    If it's a list of teams, we'll run a bracket based just on that list.

    So, one way you might want to do things is to simulate 10000 runs for each 
    of the four brackets,
    then run your final four explicitly, e.g.

    T = 1.5
    simulate(10000,'midwest',T)
    # record results
    simulate(10000,'south',T)
    # record results
    simulate(10000,'west',T)
    # record results
    simulate(10000,'east',T)
    # record results

    simulate(10000,['Louisville','Kansas','Wisconsin','Indiana'],T)
    """

    if type(region)  in (type([]), type(())):
        teams = region[:]
    else:
        teams = RAS.teams[region]
    b = Bracket(teams, T)
    energy = b.energy()
    ng = sum(b.games_in_rounds) # total number of games
    # Let's collect some statistics
    brackets = []
    for trial in xrange(ntrials):
        g = randint(0, ng) #choice(xrange(ng)) # choose a random game to swap
        #print "attempted swap for game",g#,"in round",round[g]
        newbracket = deepcopy(b)
        newbracket.swap(g)
        newenergy = newbracket.energy()
        ediff = newenergy - energy
        if ediff <= 0:
            b = newbracket
            energy = newenergy
            if printonswap:
                print "LOWER"
                print b
        else:
            if random() < exp(-ediff/T):
                b = newbracket
                energy = newenergy
                if printonswap:
                    print "HIGHER"
                    print b
        brackets.append(b)


    lb, mcb, mcb_count, unique_brackets, lowest_sightings = \
        Stats.gather_uniquestats(brackets)
    if showvis:
        Visualization.showstats(brackets, unique_brackets, lowest_sightings, 
                                newfig=newfig, teamdesc=teamdesc)
    if printbrackets:
        print "Lowest energy bracket"
        print lb
        print "Most common bracket (%s)"%mcb_count
        print mcb
    return (lb,mcb)

def runbracket1(ntrials, T):
    simulate(ntrials,'all',T)

def runbracket2(ntrials1, ntrials2, T):
    results = {}
    regions = 'midwest west south east'.split()
    for (i,region) in enumerate(regions):
        results[region] = simulate(ntrials1, region, T, newfig=i, 
                                   teamdesc=region, printbrackets=False)
    # Make a new bracket from our final four
    teams = [results[region][1].bracket[-1][0] for region in regions]
    ff_lb, ff_mcb = simulate(ntrials2, teams, T, newfig=i+1, 
                             teamdesc="Final Four", printbrackets=False)

    print "YOUR LOWEST ENERGY BRACKETS"
    for region in regions:
        print "LOWEST ENERGY BRACKET FOR REGION", region
        print results[region][0]
        print
    print "LOWEST ENERGY BRACKET FOR FINAL FOUR"
    print ff_lb
        
    print "YOUR MOST COMMON BRACKETS"
    for region in regions:
        print "MOST COMMON BRACKET FOR REGION", region
        print results[region][1]
        print
    print "MOST COMMON BRACKET FOR FINAL FOUR"
    print ff_mcb

# now you can call deltaU(current_winner,current_loser) if you'd like.
deltaU = energy_of_flipping
Brackets.deltaU = deltaU
Brackets.energy_game = energy_game
Brackets.energy_of_flipping = energy_of_flipping
