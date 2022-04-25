import os, csv, sys, random

#players.csv columns
PLAYER_COLS = 5
PLAYER_INDEX = 0
PLAYER_FIRST = 1
PLAYER_LAST = 2
PLAYER_SCHOOL = 3
PLAYER_RANK = 4

#round.csv columns
MATCH_COLS = 6
MATCH_FIRST = 0
MATCH_LAST = 1
MATCH_INDEX = 2
MATCH_SCHOOL = 3
MATCH_COLOR = 4
MATCH_RESULT = 5

#Make sure there is a parameter on the commandline
if len(sys.argv) < 2:
    print "Need the directory of the tournament:\n"
    print "\t python run_tournament.py [path to tournament files]\n"
    sys.exit()

tourn_path = sys.argv[1]

#make sure the path to the tournament directory is valid
if not os.path.exists(tourn_path):
    print "\nTournament path:\n\t", tourn_path, "\ndoes not exist\n"
    print "Please find valid path\n"
    sys.exit()

files = os.listdir(tourn_path)
files.sort()

#make sure the players.csv files exists
player_file = "players.csv"
if player_file not in files: 
    print "Cannot find:\n\t" + player_file + "\nfiles.\n"
    print "Please put " + player_file + " in the tournament directory"
    sys.exit()

for ff in files:
    if ff[0] == '.': files.remove(ff)

#load the player information
players = [{}]
schools = {}

with open(os.path.join(tourn_path, player_file)) as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if len(row) < 2: continue
        if (row[0][0] == '#'): continue
        if len(row) != PLAYER_COLS:
            print "\nInvalid Player: ", row, "\n"
            res = raw_input("Would you like to exit to fix input file? (y/n)")
            if res.lower().lstrip().rstrip() == 'y':
                sys.exit()
            continue
        player_idx = -1
        try: 
            player_idx = int(row[PLAYER_INDEX])
        except:
            print "\nNot a valid player index: ", row[PLAYER_INDEX], "\n"
            res = raw_input("Would you like to exit to fix input file? (y/n)")
            if res.lower().lstrip().rstrip() == 'y':
                sys.exit()
            continue
        rank = 500
        try: 
            if row[PLAYER_RANK].strip() != '':
                rank = int(row[PLAYER_RANK])
        except:
            print "\nNot a valid player rank: ", row[PLAYER_RANK], "\n"
            res = raw_input("Would you like to exit to fix input file? (y/n)")
            if res.lower().lstrip().rstrip() == 'y':
                sys.exit()
            continue
        players.insert(player_idx, {
            'idx': row[PLAYER_INDEX].lower().lstrip().rstrip(),
            'first': row[PLAYER_FIRST].lower().lstrip().rstrip(),
            'last': row[PLAYER_LAST].lower().lstrip().rstrip(),
            'school': row[PLAYER_SCHOOL].lower().lstrip().rstrip(),
            'rank': rank,
            'matches': [],
            'record': {'win' :0, 'loss': 0, 'bye': 0, 'draw': 0, 'black': 0, 'white': 0}
        })
        if players[-1]['school'] not in schools.keys():
            schools[players[-1]['school']] = []
        schools[players[-1]['school']].append(players[-1])

#on the first time parsing the file, check and make sure things look correct
roundcnt = -1
if len(files) == 1:
    print "\nThe Schools in the tournament are:"
    for ss in schools.keys():
        print "\t", ss

    res = raw_input("There are " + str(len(schools.keys())) +
        " schools in the tournament, is this correct? (y/n)"
    )
    if res.lower().lstrip().rstrip() != 'y':
        print "Please fix ", player_file
        sys.exit()
     
    print "\n"
    res = raw_input("There are " + str(len(players)) + " players in the tournament, is this correct? (y/n)")
    if res.lower().lstrip().rstrip() != 'y':
        print "Please fix ", player_file
        sys.exit()

    print "\n"
    while True:
        roundtmp = raw_input("How many rounds will be played today?")
        try:
            roundcnt = int(roundtmp)
            break
        except:
            print "Invalid number: " + roundtmp + "\n\n"

#check and see if any rounds have been played
last_round = 0
for ff in files:
    if ff[0] == '.': continue
    if 'round' in ff:
        cur_round = -1
        try:
            idx = ff.find(".csv")
            cur_round = int(ff[5:idx])
            if cur_round > last_round:
                last_round = cur_round 
        except:
            print "\nInvalid round file, skipping " + ff + "\n"
            continue
        #parse the round file
        with open(os.path.join(tourn_path, ff)) as csvfile:
            print "FILE: ", ff
            reader = csv.reader(csvfile)
            matchnum = -1
            match1 = None
            match2 = None
            for row in reader:
                if len(row) == 0: continue
                if row[0][0] == '#': continue
                if 'TOTAL_ROUNDS' in row[0]:
                    try:
                        roundcnt = int(row[0][12:].lstrip().rstrip())
                    except:
                        print "Invalid round count: " + str(row[0][12:]) + "\n\n"
                        sys.exit()
                if "match" in row[0]:
                    try: 
                        matchnum = int(row[0][6:])
                    except:
                        print "Invalid match num: ", row[7:]
                    continue
                if matchnum == -1: continue
                try:
                    idx = int(row[MATCH_INDEX])
                    assert(idx < len(players))
                except:
                    print "Invalid match player index: ", row[MATCH_INDEX]
                    sys.exit()
                if match1 == None:
                    match1 = {
                        'round':cur_round,
                        'match':matchnum,
                        'player':int(row[MATCH_INDEX].lower().lstrip().rstrip()),
                        'opponent':-1,
                        'color':row[MATCH_COLOR].lower().lstrip().rstrip(),
                        'result':row[MATCH_RESULT].lower().lstrip().rstrip()
                    }
                    if players[match1['player']]['first'] != row[MATCH_FIRST].lower().lstrip().rstrip():
                        print ("first names dont match: ",
                            players[match1['player']]['first'],
                            row[MATCH_FIRST].lower().lstrip().rstrip()
                        )
                        break
                    if players[match1['player']]['last'] != row[MATCH_LAST].lower().lstrip().rstrip():
                        print ("last names dont match: ",
                            players[match1['player']]['last'],
                            row[MATCH_LAST].lower().lstrip().rstrip()
                        )
                        break
                    if match1['result'].lower().lstrip().rstrip()[0] == 'w':
                        players[match1['player']]['record']['win'] += 1
                    elif match1['result'].lower().lstrip().rstrip()[0] == 'l':
                        players[match1['player']]['record']['loss'] += 1
                    elif match1['result'].lower().lstrip().rstrip()[0] == 'b':
                        players[match1['player']]['record']['bye'] += 1
                    elif match1['result'].lower().lstrip().rstrip()[0] == 'd':
                        players[match1['player']]['record']['draw'] += 1
                    else:
                        print ("invalid result: ", match1)
                        sys.exit()
                    if match1['color'].lower().lstrip().rstrip()[0] == 'w':
                        players[match1['player']]['record']['white'] += 1
                    elif match1['color'].lower().lstrip().rstrip()[0] == 'b':
                        players[match1['player']]['record']['black'] += 1
                    else:
                        print ("player 1 invalid color: ", match1)
                        sys.exit()
                    continue
                if match2 == None:
                    match2 = {
                        'round':cur_round,
                        'match':matchnum,
                        'player':int(row[MATCH_INDEX].lower().lstrip().rstrip()),
                        'opponent':-1,
                        'color':row[MATCH_COLOR].lower().lstrip().rstrip(),
                        'result':row[MATCH_RESULT].lower().lstrip().rstrip()
                    }
                    if players[match2['player']]['first'] != row[MATCH_FIRST].lower().lstrip().rstrip():
                        print ("first names dont match: ",
                            players[match2['player']]['first'],
                            row[MATCH_FIRST].lower().lstrip().rstrip()
                        )
                        break
                    if players[match2['player']]['last'] != row[MATCH_LAST].lower().lstrip().rstrip():
                        print ("last names dont match: ",
                            players[match2['player']]['last'],
                            row[MATCH_LAST].lower().lstrip().rstrip()
                        )
                        break
                    if match2['result'].lower().lstrip().rstrip()[0] == 'w':
                        players[match2['player']]['record']['win'] += 1
                    elif match2['result'].lower().lstrip().rstrip()[0] == 'l':
                        players[match2['player']]['record']['loss'] += 1
                    elif match2['result'].lower().lstrip().rstrip()[0] == 'b':
                        players[match2['player']]['record']['bye'] += 1
                    elif match2['result'].lower().lstrip().rstrip()[0] == 'd':
                        players[match2['player']]['record']['draw'] += 1
                    else:
                        print ("invalid result: ", match2)
                        sys.exit()
                    if match2['color'].lower().lstrip().rstrip()[0] == 'w':
                        players[match2['player']]['record']['white'] += 1
                    elif match2['color'].lower().lstrip().rstrip()[0] == 'b':
                        players[match2['player']]['record']['black'] += 1
                    else:
                        print ("player 2 invalid color: ", match2)
                        sys.exit()
                if match1 != None and match2 != None:
                    match1['opponent'] = match2['player']
                    match2['opponent'] = match1['player']
                    players[match1['player']]['matches'].append(match1)
                    players[match2['player']]['matches'].append(match2)
                else:
                    print "Invalid match file, exiting"
                    sys.exit()
                match1 = None
                match2 = None

#generate the next round of matches
#print schools

new_matches = []
#test output
#new_matches = [{
#    'index1':1,
#    'index2':5,
#    'color1':'white',
#    'color2':'black'
#}]

cur_round = last_round + 1

players_nums = list(xrange(len(players)))
school_names = schools.keys()
schoolcnt = len(school_names)
school_nums = []

#first round
#if cur_round == 1: 
if cur_round == -1: 
    #top three students per school get paried to top three students from other schools
    s1 = None
    s2 = None
    x1 = None
    x2 = None
    school1 = None
    school2 = None
    for ii in xrange(3):
        if len(school_nums) == 0:
            school_nums = list(xrange(schoolcnt))
        for jj in xrange((len(school_names) + 1)/2):
            if s1 == None:
                if s2 != None:
                    print "State problem"
                    sys.exit()
                s1idx = random.randint(0, len(school_nums)-1)
                s1 = school_nums[s1idx]
                school_nums.remove(s1)
                x1 = ii
                school1 = school_names[s1]
            if s2 == None:
                if len(school_nums) == 0: break
                s2idx = s1idx
                school2 = school1
                while school1 == school2:
                    s2idx = random.randint(0, len(school_nums)-1)
                    s2 = school_nums[s2idx]
                    school2 = school_names[s2]
                school_nums.remove(s2)
                x2 = ii
            p1 = schools[school1][x1]
            p2 = schools[school2][x2]
            players_nums.remove(int(p1['idx']))
            players_nums.remove(int(p2['idx']))
            c1 = 'white'
            c2 = 'black'
            if p1['record']['white'] > p2['record']['white']:
                c1 = 'black'
                c2 = 'white'
            new_matches.append({
                'index1':int(p1['idx']),
                'index2':int(p2['idx']),
                'color1':c1,
                'color2':c2
            })
            s1 = None
            s2 = None
    #everyone else is random
    while True:
        for ii in xrange(len(players_nums)/2):
            p1idx = random.randint(1, len(players_nums)-1)
            p1 = players[players_nums[p1idx]]
            players_nums.remove(int(p1['idx']))
            p2school = p1['school']
            p2idx = None
            p2 = None
            while p1['school'] == p2school:
                p2idx = random.randint(1, len(players_nums)-1)
                p2 = players[players_nums[p2idx]]
                p2school = p2['school']
                if len(players_nums) == 1: break
            players_nums.remove(int(p2['idx']))
            c1 = 'white'
            c2 = 'black'
            if p1['record']['white'] > p2['record']['white']:
                c1 = 'black'
                c2 = 'white'
            new_matches.append({
                'index1':int(p1['idx']),
                'index2':int(p2['idx']),
                'color1':c1,
                'color2':c2
            })
        break
    if len(players_nums) > 0:
        print "Left over players: ", players_nums
        for pp in players_nums:
            print pp
            
else:
    #sort wins and losses
    winlist = []
    for xx in xrange(cur_round):
        winlist.append([])
    for pp in players:
        if len(pp.keys()) == 0: continue
        totwins = pp['record']['win'] + pp['record']['draw']
        winlist[totwins].append(int(pp['idx']))
    #print standings
    print "CURRENT STANDINGS:\n"
    print "\t PLAYERS:"
    schoolpts = {}
    playerpts = {}
    for pp in players:
        if len(pp.keys()) == 0: continue
        if pp['school'] not in schoolpts.keys():
            schoolpts[pp['school']] = 0
        pts = pp['record']['win'] + .5*pp['record']['draw']
        schoolpts[pp['school']] += pts
        if str(pts) not in playerpts.keys():
            playerpts[str(pts)] = []
        playerpts[str(pts)].append(pp['idx'])
    ptkeys = playerpts.keys()
    ptkeys.sort()
    for xx in ptkeys:
        for ii in playerpts[xx]:
            pp = players[int(ii)]
            print "\t\t", pp['first'], " ", pp['last'], ", ", pp['school'], 
            print " (", pp['record']['win'], "-", pp['record']['draw'], "-", pp['record']['loss']
    print "\n\tSCHOOLS:"
    for xx in schools.keys():
        print "\t\t", xx, ":"
        for pp in players:
            if len(pp.keys()) == 0: continue
            if pp['school'] == xx:
                print "\t\t\t",
                print "\t\t", pp['first'], " ", pp['last'], ", ", pp['school'], 
                print " (", pp['record']['win'], "-", pp['record']['draw'], "-", pp['record']['loss']
    #end of tournament?
    if cur_round > roundcnt:
        sys.exit()

    leftover = None
    for xx in xrange(len(winlist)):
        ww = winlist[len(winlist)-xx-1]
        if leftover != None: ww.append(leftover)
        print "WW: ", ww
        while True:
            for ii in xrange(len(ww)/2):
                p1idx = random.randint(0, len(ww)-1)
                p1 = players[ww[int(p1idx)]]
                ww.remove(int(p1['idx']))
                p2school = p1['school']
                p2idx = None
                p2 = None
                while p1['school'] == p2school:
                    p2idx = random.randint(0, len(ww)-1)
                    p2 = players[ww[int(p2idx)]]
                    p2school = p2['school']
                    for mm in p1['matches']:
                        if mm['opponent'] == p2['idx']:
                            p2school = p1['school']
                    if len(ww) == 1: break
                ww.remove(int(p2['idx']))
                c1 = 'white'
                c2 = 'black'
                if p1['record']['white'] > p2['record']['white']:
                    c1 = 'black'
                    c2 = 'white'
                new_matches.append({
                    'index1':int(p1['idx']),
                    'index2':int(p2['idx']),
                    'color1':c1,
                    'color2':c2
                })
                players_nums.remove(int(p1['idx']))
                players_nums.remove(int(p2['idx']))
            if len(ww) != 0:
                leftover = ww[0]
                print "assign leftover: ", leftover
            else:
                leftover = None
                print "no leftover: ", leftover
            break
    if len(players_nums) != 0:
        print "LEFT OVER PLAYER NUMS: ", players_nums


print new_matches
print "LEN: ", len(new_matches)

#dump to file
roundfile = os.path.join(tourn_path, "round" + str(cur_round) + ".csv") 
print roundfile
with open(roundfile, 'w') as mfile:
    mfile.write("#match MATCH_NUM\n")
    mfile.write("#PLAYER_FIRST, PLAYER_LAST, PLAYER_INDEX, ")
    mfile.write("PLAYER_SCHOOL, MATCH_COLOR(black,white), WIN_LOSS(win,loss)\n")
    mfile.write("TOTAL_ROUNDS " + str(roundcnt) + "\n\n")
    matchcnt = 1
    for mm in new_matches:
        mfile.write("match " + str(matchcnt) + "\n")
        mfile.write(",".join([
            players[mm['index1']]['first'],
            players[mm['index1']]['last'],
            str(mm['index1']),
            players[mm['index1']]['school'],
            mm['color1']
        ]) + ',\n')
        mfile.write(",".join([
            players[mm['index2']]['first'],
            players[mm['index2']]['last'],
            str(mm['index2']),
            players[mm['index2']]['school'],
            mm['color2']
        ]) + ',\n\n')
        matchcnt += 1
    mfile.write("Bye:\n")
    mfile.write(",".join([
        players[mm['index2']]['first'],
        players[mm['index2']]['last'],
        str(mm['index2']),
        players[mm['index2']]['school'],
        mm['color2']
    ]) + ',\n\n')
