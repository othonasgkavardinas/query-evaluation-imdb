import time
import sys
from itertools import tee
#
d = {}

def scan(filename):
    global d
    if filename not in d:
        d[filename] = tee(generator(filename))
    return d[filename][0]

def generator(filename):
    file = open(filename, "r")

    file.readline()

    for line in file:
        yield(line)
    file.close()

def mj(iter1, iter2, columns1, columns2):
    try:
        line1 = next(iter1).split("\t")
        line2 = next(iter2).split("\t")
        prev1 = [""]
        prev2 = [""]
    except StopIteration:
        return

    while True:
        try:
            if line1[0] == line2[0]:
                yield(create_output(line1, line2, columns1, columns2))
                prev1 = line1
                prev2 = line2
                line1 = next(iter1).split("\t")
                line2 = next(iter2).split("\t")
            elif line1[0] > line2[0]:
                if prev1[0] == line2[0]:
                    yield(create_output(prev1, line2, columns1, columns2))
                prev2 = line2
                line2 = next(iter2).split("\t")
            else:
                if line1[0] == prev2[0]:
                    yield(create_output(line1, prev2, columns1, columns2))
                prev1 = line1
                line1 = next(iter1).split("\t")
        except StopIteration:
            break 
     
def create_output(line1, line2, columns1, columns2):
    output = line1[0]

    if type(columns1) is int:
        output += "\t" + line1[columns1].strip()
    else:
        for arg in columns1:
            output += "\t" + line1[arg].strip()

    if type(columns2) is int:
        output += "\t" + line2[columns2].strip()
    else:
        for arg in columns2:
            output += "\t" + line2[arg].strip()
    output += "\n" 
    return output 

def main():
    if len(sys.argv) != 5:
        print("Error: Invalid Number of Arguments,")
        print("Please insert: file file (column,...) (column,...)")
        sys.exit(1)

    t1 = tuple([eval(x) for x in sys.argv[3].split(',')])
    t2 = tuple([eval(x) for x in sys.argv[4].split(',')])

    file_output = open("outputX.tsv", "w")
    while True:
        try:
            file_output.write(next(mj(scan(sys.argv[1]), scan(sys.argv[2]), t1, t2)))
        except StopIteration:
            break
    file_output.close() 

def test_main():
    
    file_output1 = open("output_test1.tsv", "w")
    while True:
        try:
            file_output1.write(next(mj(scan('data/title.basics.tsv'),scan('data/title.ratings.tsv'),(2),(1,2))))
        except StopIteration:
            break
    file_output1.close() 
    
    file_output2 = open("output_test2.tsv", "w")
    while True:
        try:
            file_output2.write(next(mj(scan('data/title.basics.tsv'),scan('data/title.principals.tsv'),(2),(2))))
        except StopIteration:
            break
    file_output2.close() 

    file_output3 = open("output_test3.tsv", "w")
    while True:
        try:
            file_output3.write(next(mj(mj(scan('data/title.basics.tsv'),scan('data/title.principals.tsv'),(2),(2)),scan('data/title.ratings.tsv'),(1,2),(1))))
        except StopIteration:
            break
    file_output3.close() 

start_time = time.time()
main()
#test_main()
print("total time: %s" %(time.time() - start_time))
