
import os, sys, csv, random


def rand_round(filepath):

    if not os.path.exists(filepath):
        print "\n\nERROR: \n"
        print "\tFile: ", filepath, " does not exist"
        sys.exit()

    newout = []
    prev = None
    done = False
    with open(filepath) as ff:
        reader = csv.reader(ff)
        for row in reader:
            if len(row) < 2:
                if len(row) > 0 and 'bye:' in row[0]: done = True
                newout.append(",".join(row))
                prev = None
                continue
                
            if done:
                newout.append(",".join(row))
                prev = None
                continue 

            if row[0][0] == "#" or 'match' in row[0]:
                newout.append(",".join(row))
                prev = None
                continue
            
            if prev == None:
                prev = random.randint(0, 1)
                if prev == 1:
                    row[-1] = "win"
                else:
                    row[-1] = "loss"
            else:
                if prev == 1:
                    row[-1] = "loss"
                else:
                    row[-1] = "win"

            newout.append(",".join(row))
    with open(filepath, 'w') as mfile:
        for row in newout:
            mfile.write(row + "\n")


if __name__ == "__main__":
    if len(sys.argv) < 2: 
        print "Please provide round file."
        sys.exit()

    rand_round(sys.argv[1])
