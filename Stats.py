#!/usr/bin/env python
from __future__ import division
from collections import Counter
from Brackets import Bracket

def gather_uniquestats(brackets):
    lb = Bracket(brackets[0].teams, T=0.0000001) # low bracket
    low_hash = hash(lb)
    cnt = Counter()
    unique_brackets = []
    lowest_sightings = []
    brackets_by_hash = {}
    for b in brackets:
        h = hash(b)
        cnt[h] += 1
        unique_brackets.append(len(cnt))
        lowest_sightings.append(cnt[low_hash])
        brackets_by_hash[h] = b
    h,c = cnt.most_common(1)[0]
    mcb = brackets_by_hash[h] # most comon bracket
    return lb, mcb, c, unique_brackets, lowest_sightings
