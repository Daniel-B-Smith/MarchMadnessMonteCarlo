#!/usr/bin/env python
from __future__ import division
import numpy as np
import pylab as pl
from random import choice,shuffle
from numpy.random import random #import only one function from somewhere
from numpy.random import randint
from numpy import exp,array,zeros
import scipy
from time import sleep
from copy import deepcopy
from collections import Counter, OrderedDict

import RankingsAndStrength as RAS

import Brackets
from Brackets import Bracket

def plotone(brackets,label,subplot1,subplot2,values=None,label2=None,values2=None,teamdesc=None):
    ntrials = len(brackets)
    if values is None:
        try:
            values = [getattr(b,label)() for b in brackets]
        except TypeError:
            values = [getattr(b,label) for b in brackets]
    pl.subplot(subplot1)
    pl.plot(range(ntrials),values,'.',label=label)
    pl.ylabel(label.capitalize())
    pl.xlabel('Game')
    if teamdesc is not None:
        pl.title('%s over the trajectory, T=%s, %s'%(label.capitalize(),brackets[0].T,teamdesc))
    else:
        pl.title('%s over the trajectory, T=%s'%(label.capitalize(),brackets[0].T))
    #pl.legend()
    pl.subplot(subplot2)
    if values2 is None:
        if ntrials > 1000:
            nbins = min(int(ntrials/100),200)
        else:
            nbins = 10
        pl.hist(values,bins=nbins)
        pl.title('%s distribution, T=%s'%(label.capitalize(),brackets[0].T))
    else:
        pl.subplot(subplot2)
        pl.plot(range(ntrials),values2,'.',label=label2)
        pl.ylabel(label2.capitalize())
        pl.xlabel('Game')
        pl.title('%s over the trajectory, T=%s'%(label2.capitalize(),brackets[0].T))

    
def showstats(brackets,unique_brackets,lowest_sightings,newfig=False,teamdesc=None):
    if newfig is not False:
        if newfig is True:
            pl.figure()
        else:
            pl.figure(newfig)
    pl.clf()
    plotone(brackets,'energy',231,234,teamdesc=teamdesc)
    plotone(brackets,'upsets',232,235,teamdesc=teamdesc)
    plotone(brackets,'Unique brackets',233,236,values=unique_brackets,label2="Lowest Energy Sightings",values2=lowest_sightings,teamdesc=teamdesc)
    pl.show()

