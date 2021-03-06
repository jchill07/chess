import os, csv, sys, random

#{{{players.csv columns
PLAYER_COLS = 5
PLAYER_INDEX = 0
PLAYER_FIRST = 1
PLAYER_LAST = 2
PLAYER_SCHOOL = 3
PLAYER_RANK = 4
#}}}
#{{{round.csv columns
MATCH_COLS = 6
MATCH_FIRST = 0
MATCH_LAST = 1
MATCH_INDEX = 2
MATCH_SCHOOL = 3
MATCH_COLOR = 4
MATCH_RESULT = 5
#}}}

#{{{ check_params
def check_params(tourn_path, player_file):
    #Make sure there is a parameter on the commandline

    #make sure the path to the tournament directory is valid
    if not os.path.exists(tourn_path):
        print "\nTournament path:\n\t", tourn_path, "\ndoes not exist\n"
        print "Please find valid path\n"
        sys.exit()

    files = os.listdir(tourn_path)
    files.sort()

    #make sure the players.csv files exists
    if player_file not in files: 
        print "Cannot find:\n\t" + player_file + "\nfiles.\n"
        print "Please put " + player_file + " in the tournament directory"
        sys.exit()

    for ff in files:
        if ff[0] == '.': files.remove(ff)

    return files
#}}}

#{{{ make_matches
def make_matches(players, players_nums, leftover):
    full_tries = 0
    failed = False
    while True:
        full_tries += 1
        ww = players_nums[:]
        new_matches = []
        repeat_match = False
        ll = leftover
        for ii in xrange(len(ww)/2):
            if ll != None:
                p1idx = ww.index(ll) 
                ll = None
            else:
                p1idx = random.randint(0, len(ww)-1)
            p1 = players[ww[int(p1idx)]]
            ww.remove(int(p1['idx']))
            p2school = p1['school']
            p2idx = None
            p2 = None
            tries = 0
            while p1['school'] == p2school:
                tries += 1
                p2idx = random.randint(0, len(ww)-1)
                p2 = players[ww[int(p2idx)]]
                p2school = p2['school']
                for mm in p1['matches']:
                    if str(mm['opponent']) == str(p2['idx']):
                        p2school = p1['school']
                        repeat_match = True
                if tries > 50:
                    break

                if len(ww) == 1: break
            if (tries > 50 and full_tries < 50) or repeat_match:
                print p1['idx'], ":", ww,
                for pp in p1['matches']:
                    print pp['opponent'],
                print ""
                failed = True
            if failed: break

            ww.remove(int(p2['idx']))
            n1 = int(p1['idx'])
            n2 = int(p2['idx'])
            if p1['record']['white'] > p2['record']['white']:
                tmp = n1
                n1 = n2
                n2 = tmp
            new_matches.append({
                'index1':n1,
                'index2':n2,
                'color1':'white',
                'color2':'black'
            })
        if failed:
            failed = False
            continue
        ll = None
        if len(ww) != 0:
            ll = ww[0]
            if players[ww[0]]['record']['bye'] != 0:
                full_tries -= 1
                continue
        return new_matches, ll
#}}}

#{{{ read_players
def read_players(tourn_path, player_file):
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
    return players, schools

#}}}
#{{{read_rounds
def read_rounds(tourn_path, files, roundcnt, players):
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
                reader = csv.reader(csvfile)
                matchnum = -1
                match1 = None
                match2 = None
                bye = False
                for row in reader:
                    if 'bye:' in row:
                        bye = True
                        continue
                    if bye:
                        match1 = {
                            'round':cur_round,
                            'match':matchnum,
                            'player':int(row[MATCH_INDEX].lower().lstrip().rstrip()),
                            'opponent':-1,
                            'color':'white',
                            'result':'win'
                        }
                        players[match1['player']]['record']['win'] += 1
                        players[match1['player']]['record']['bye'] += 1
                        break
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
                        try:
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
                        except:
                            print "\n\nERROR: "
                            print "\tCould not find result in round file."
                            print "\tPlease make sure all results are entered"
                            print "\tinto the round file and the round file is saved\n\n"
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
    return last_round, roundcnt, players
#}}}

#{{{check_tourn
def check_tourn(players, schools):
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
    res = raw_input("There are " + str(len(players)-1) + " players in the tournament, is this correct? (y/n)")
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
    return roundcnt
#}}}

#{{{sort_wins
def sort_wins(cur_round, players):
    winlist = []
    for xx in xrange(cur_round):
        winlist.append([])
    for pp in players:
        if len(pp.keys()) == 0: continue
        totwins = pp['record']['win'] + pp['record']['draw']
        winlist[totwins].append(int(pp['idx']))
    return winlist
#}}}

#{{{print_player_standings
def print_player_standings(players):
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
    ptkeys.sort(reverse=True)
    for xx in ptkeys:
        for ii in playerpts[xx]:
            pp = players[int(ii)]
            print "\t\t", pp['first'], " ", pp['last'], ", ", pp['school'], 
            print " (", pp['record']['win'], "-", pp['record']['draw'], "-", pp['record']['loss'],")"

#}}}
#{{{print_school_standings
def print_school_standings(schools, players):
    print "\n\tSCHOOLS:"
    for xx in schools.keys():
        print "\t\t", xx, ":"
        for pp in players:
            if len(pp.keys()) == 0: continue
            if pp['school'] == xx:
                print "\t\t\t",
                print "\t\t", pp['first'], " ", pp['last'], ", ", pp['school'], 
                print " (", pp['record']['win'], "-", pp['record']['draw'], "-", pp['record']['loss'],")"
#}}}

#{{{ write_round_file
def write_round_file(tourn_path, cur_round, roundcnt, new_matches, players, leftover):
    roundfile = os.path.join(tourn_path, "round" + str(cur_round) + ".csv") 
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
        if leftover != None:
            mfile.write("bye:\n")
            mfile.write(",".join([
                players[leftover]['first'],
                players[leftover]['last'],
                str(leftover),
                players[leftover]['school'],
                mm['color2']
            ]) + ',\n\n')
#}}}
#{{{ print_round
def print_round(cur_round, new_matches, players, leftover):
    print "\n\nROUND ", cur_round, "\n"
    matchcnt = 1
    for mm in new_matches:
        print("\tmatch " + str(matchcnt))
        print("\t"+",".join([
            players[mm['index1']]['first'],
            players[mm['index1']]['last'],
            str(mm['index1']),
            players[mm['index1']]['school'],
            mm['color1']
        ]) + ',')
        print("\t"+",".join([
            players[mm['index2']]['first'],
            players[mm['index2']]['last'],
            str(mm['index2']),
            players[mm['index2']]['school'],
            mm['color2']
        ]) + ',\n')

        matchcnt += 1
    if leftover != None:
        print("\tbye:")
        print("\t"+",".join([
            players[leftover]['first'],
            players[leftover]['last'],
            str(leftover),
            players[leftover]['school'],
            mm['color2']
        ]) + ',\n')
#}}}

#{{{run
def run(tourn_path, check=True, roundcnt=-1):
    print "ok"

    player_file = "players.csv"
    files = check_params(tourn_path, player_file)

    #load the player information
    players, schools = read_players(tourn_path, player_file)
    print "ok2"

    #on the first time parsing the file, check and make sure things look correct
    if len(files) == 1 and check:
        roundcnt = check_tourn(players, schools)

    last_round, roundcnt, players = read_rounds(tourn_path, files, roundcnt, players)
    print "ok3"

    cur_round = last_round + 1

    #sort wins and losses
    winlist = sort_wins(cur_round, players)
    print "here"
    #print_standings
    print_player_standings(players)
    print_school_standings(schools, players)
    print "here2"

    #end of tournament?
    if cur_round > roundcnt:
        sys.exit()

    #generate new matches
    leftover = None
    new_matches = []
    for xx in xrange(len(winlist)):
        ww = winlist[len(winlist)-xx-1]
        if leftover != None:
            ww.append(leftover)
        nmatches, leftover = make_matches(players, ww, leftover)
        new_matches = new_matches + nmatches

    write_round_file(tourn_path, cur_round, roundcnt, new_matches, players, leftover)
    print_round(cur_round, new_matches, players, leftover)
#}}}
#{{{ __main__
if __name__ == "__main":
    print ("sup")
    if len(sys.argv) < 2:
        print "Need the directory of the tournament:\n"
        print "\t python run_tournament.py [path to tournament files]\n"
        sys.exit()

    run(sys.argv[1])
#}}}
