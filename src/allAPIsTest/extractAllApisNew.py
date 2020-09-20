""" Extract APIs

Usage: 
    extractAllApisNew.py
    extractAllApisNew.py <csv_file>
"""

import os

import re
from docopt import docopt
import string

def scanFile(inFile):
    fp = open(inFile, 'r').readlines()
    cnt = 0
    # print(len(fp))
    # print(fp[0])
    next = []
    first = []
    second = []
    third = []
    smallOnly = []
    cntSmallOnly = 0
    validSmalls = open("validSmalls.txt", 'r').read().splitlines()
    # print(validSmalls)
    for line in fp:
        flag = True
        api = line.split(',')[0]
        freq = line.split(',')[1]
        freq = freq.split('\n')[0]
        if(len(api.split('.')) == 1 and int(freq) < 1000):
            flag = False
        if(int(freq) < 100):
            flag = False
        split = api.split('.')
        for each in split:
            if('$' in each):
                flag = False
            if(len(each) < 3):
                flag = False
            if(each.isupper()):
                flag = False
            if(bool(re.search(r'\d', each))):
                flag = False
            if 'NaN' in each:
                flag = False
            if '_' in each:
                flag = False
            # Load from file with VALID lengths < 6 and check if it it
            # length < 6 and not in this file (readlines)                
            firstPart = api.split('.')[0]
            # secondPart = api.split('.')[1]
            if( (len(firstPart) < 6) and (firstPart not in validSmalls) ):
                flag = False
            # if(firstPart[0] not in string.ascii_lowercase):
            #     flag = False
            # if(secondPart[0] not in string.ascii_lowercase):
            #     flag = False                
        if flag:
            cnt += 1
            next.append(line)
            check = api.split('.')
            if(len(check[0]) < 6 ):
                smallOnly.append(line)
                cntSmallOnly += 1
            if(len(check) == 3):
                if str(check[0]) != str(check[1]) :
                    first.append(check[0])
                    second.append(check[1])
                    third.append(check[2])
            elif(len(check) == 2):
                if str(check[0]) != str(check[1]) :
                    first.append("''")
                    second.append(check[0])
                    third.append(check[1])
            elif(len(check) == 1):
                first.append("''")
                second.append("''")
                third.append(check[0])
    # print(first[:12])
    # print(second[:12])
    # print(third[:12])
    # print(first[11] + '.' + second[11] + '.' + third[11])
    # print(first[111] + '.' + second[111] + '.' + third[111])
    # print(first[211] + '.' + second[211] + '.' + third[211])
    # print(first[311] + '.' + second[311] + '.' + third[311])
    # print(first[411] + '.' + second[411] + '.' + third[411])
    # return
    # with open("first1.txt", "w") as firstFile:
    #     for f in first:
    #         firstFile.write(f + '\n')
    # with open("second1.txt", "w") as secondFile:
    #     for s in second:
    #         secondFile.write(s + '\n')
    # with open("third1.txt", "w") as thirdFile:
    #     for t in third:
    #         thirdFile.write(t + '\n')                
    print(next)
    print(cnt)
    # for each in sorted(next):
    #     print(each)
    # for smallEach in sorted(smallOnly):
    #     print(smallEach)
    # print(cntSmallOnly)

if __name__=="__main__":
    arguments = docopt(__doc__)
    if arguments["<csv_file>"]:
        scanFile(arguments["<csv_file>"])
