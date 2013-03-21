#!/usr/bin/env python
from __future__ import division
from collections import OrderedDict
import KenPomeroy as KP
import JeffSagarin as JS
from numpy.random import random #import only one function from somewhere


# Could be St. Mary's instead of Middle Tennessee
# Could be Liberty instead of North Carolina A&T.
teams = {}
teams['midwest'] = ['Louisville','North Carolina A&T','Colorado St.','Missouri',
                    'Oklahoma St.','Oregon','St. Louis','New Mexico St.',
                    'Memphis',"St. Mary's",'Michigan St.','Valparaiso',
                    'Creighton','Cincinnati','Duke','Albany']

#Could be La Salle instead of Boise St.
teams['west'] = ['Gonzaga','Southern','Pittsburgh','Wichita St.',
                 'Wisconsin','Mississippi','Kansas St.','La Salle',
                 'Arizona','Belmont','New Mexico','Harvard',
                 'Notre Dame','Iowa St.','Ohio St.','Iona']

teams['south'] = ['Kansas','Western Kentucky','North Carolina','Villanova',
                  'Virginia Commonwealth','Akron','Michigan','South Dakota St.',
                  'UCLA','Minnesota','Florida','Northwestern St.',
                  'San Diego St.','Oklahoma','Georgetown','Florida Gulf Coast']

# Could be Long Island instead of James Madison
teams['east'] = ['Indiana','James Madison','North Carolina St.','Temple',
                 'Nevada Las Vegas','California','Syracuse','Montana',
                 'Butler','Bucknell','Marquette','Davidson',
                 'Illinois','Colorado','Miami FL','Pacific']


# These are all listed in the same order:
_rankings = [1,16,8,9,5,12,4,13,6,11,3,14,7,10,2,15]
regional_rankings = {}
for region in teams:
    for (team,rank) in zip(teams[region],_rankings):
        regional_rankings[team] = rank + random()/10

regions = {}
for region in teams:
    for team in teams[region]:
        regions[team] = region
all_teams = teams['midwest'] + teams['south'] + teams['west'] + teams['east']

kenpom = {}
for strength_type in KP.lineparts:
    kenpom[strength_type] = {}
    for team in all_teams:
        kenpom[strength_type][team] = KP.kpomdata[team][strength_type]

teams['all'] = all_teams

sagarin = {}
sagarin['Rating'] = {}
sagarin['Rank'] = {}
for team in all_teams:
    sagarin['Rating'][team] = JS.sagarindata[team]['Rating']
    sagarin['Rank'][team] = JS.sagarindata[team]['Rank']

