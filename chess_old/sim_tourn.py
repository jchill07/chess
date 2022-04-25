import os, sys, shutil, random, string, chess_tourn, rand_round


def gen_rand_tourn(playerfile):
    path = "rand_tourn_" + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
    os.mkdir(path)
    shutil.copyfile(playerfile, os.path.join(path, "players.csv"))
    return path

def check_tourn(tourn_path, roundcnt):

    print "checking tourn: ", tourn_path
    files = chess_tourn.check_params(tourn_path, "players.csv")
    players, schools = chess_tourn.read_players(tourn_path, "players.csv")
    last_round, roundcnt, players = chess_tourn.read_rounds(tourn_path, files, roundcnt, players)
    sameschool = 0
    for pp in players:
        if len(pp) == 0: continue
        if pp['record']['bye'] > 1:
            print "player has too many byes: ", pp
            print "tourn: ", tourn_path
            sys.exit()

        opps = []
        for mm in pp['matches']:
            if mm['opponent'] in opps:
                print "players played twice:", pp, mm['opponent']
                print "tourn: ", tourn_path
                sys.exit()
            if players[mm['opponent']]['school'] == pp['school']:
                sameschool += 1
            opps.append(mm['opponent'])
    return sameschool

def run(playerfile, tourns, rounds):
    sameschool = 0
    for ii in xrange(tourns):
        tourn_path = gen_rand_tourn(playerfile)
        for jj in xrange(rounds):
            chess_tourn.run(tourn_path, check=False, roundcnt=rounds)
            rand_round.rand_round(os.path.join(tourn_path, "round"+str(jj+1)+".csv"))
        sameschool += check_tourn(tourn_path, rounds)
    print "Sameschool: ", sameschool/2.0/float(tourns), " per trounament"
if len(sys.argv) < 4:
    print "python sim_tourn.py player_file sim_tourn rounds"
    sys.exit()


playerfile = sys.argv[1]
tourns = int(sys.argv[2])
rounds = int(sys.argv[3])

run(playerfile, tourns, rounds)

