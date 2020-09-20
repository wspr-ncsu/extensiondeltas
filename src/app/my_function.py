import mongoExtensionsAST as mongo
import difflib
import logging
import sys

def specialLCS(X, Y, hid1, hid2, nameBoth1, nameBoth2):
    # log = logging.StreamHandler(sys.stdout)
    # log.setLevel(logging.DEBUG)
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    # logging.basicConfig(level=logging.DEBUG)

    # filteredX = filter(lambda a: a != 'a', X)
    # filteredY = filter(lambda a: a != 'a', Y)
    percATotal = 0.0
    percAConseq = 0.0

    # X = X.split(',')
    # Y = Y.split(',')

    logging.info("\nX = ")
    logging.info(X)
    logging.info("\nY = ")
    logging.info(Y)    
    filteredX = list(filter(('a').__ne__, X))
    filteredY = list(filter(('a').__ne__, Y))
    logging.info("\nFiltered X = ")
    logging.info(filteredX)
    logging.info("\nFiltered Y = ")
    logging.info(filteredY)      
    (commonLengthTotal, commonAPITotal) = lcs(X, Y)
    (commonLengthTotalWithoutA, commonAPITotalWithoutA) = lcs(filteredX, filteredY)
    logging.info(commonLengthTotal)
    if(commonLengthTotal > 0):
        counterOfA = 0
        for eachElement in commonAPITotal:
            counterOfA += eachElement.count('a')
        percATotal = counterOfA/commonLengthTotal
    
    (commonLengthConseq, commonAPIConseq) = LCSubStr(X, Y)
    (commonLengthConseqWithoutA, commonAPIConseqWithoutA) = LCSubStr(filteredX, filteredY)
    if(commonLengthConseq > 0):
        counterOfA = 0
        for eachElement in commonAPIConseq:
            counterOfA += eachElement.count('a')        
        percAConseq = counterOfA/commonLengthConseq

    # calculate similarity
    sm=difflib.SequenceMatcher(None,X,Y)
    smWA = difflib.SequenceMatcher(None, filteredX, filteredY)

    # add to database
    dTable = mongo.diffStoreUnobfuscatedNew(
        hid1=hid1, 
        hid2=hid2, 
        nameBoth1=nameBoth1, 
        nameBoth2=nameBoth2, 
        commonLengthTotal=commonLengthTotal, 
        commonLengthConseq=commonLengthConseq, 
        percATotal=percATotal,
        percAConseq=percAConseq,
        similarityRatio=sm.ratio(),
        similarityRatioWithoutA=smWA.ratio()        
        )
    dTable.commonAPITotal.new_file(encoding='utf-8')
    dTable.commonAPITotal.write(",".join(commonAPITotal))
    dTable.commonAPITotal.close()

    dTable.commonAPIConseq.new_file(encoding='utf-8')
    dTable.commonAPIConseq.write(",".join(commonAPIConseq))
    dTable.commonAPIConseq.close()

    dTable.commonAPITotalWithoutA.new_file(encoding='utf-8')
    dTable.commonAPITotalWithoutA.write(",".join(commonAPITotalWithoutA))
    dTable.commonAPITotalWithoutA.close()

    dTable.commonAPIConseqWithoutA.new_file(encoding='utf-8')
    dTable.commonAPIConseqWithoutA.write(",".join(commonAPIConseqWithoutA))
    dTable.commonAPIConseqWithoutA.close()    

    dTable.save()

def lcs(s1, s2):
    matrix = [["" for x in range(len(s2))] for x in range(len(s1))]
    for i in range(len(s1)):
        for j in range(len(s2)):
            if s1[i] == s2[j]:
                if i == 0 or j == 0:
                    matrix[i][j] = s1[i]
                else:
                    matrix[i][j] = matrix[i-1][j-1] + ',' + s1[i]
            else:
                matrix[i][j] = max(matrix[i-1][j], matrix[i][j-1], key=len)

    cs = matrix[-1][-1]

    return (max(0, len(cs.split(',')) -1), cs.split(',')[1:])

# Returns length of longest common  
# substring of X[0..m-1] and Y[0..n-1]  
def LCSubStr(X, Y): 
    # matrix = [["" for x in range(len(s2))] for x in range(len(s1))]
    tempMatrix = []
    resMatrix = []
    position = 0
    # Create a table to store lengths of 
    # longest common suffixes of substrings.  
    # Note that LCSuff[i][j] contains the  
    # length of longest common suffix of  
    # X[0...i-1] and Y[0...j-1]. The first 
    # row and first column entries have no 
    # logical meaning, they are used only 
    # for simplicity of the program. 

    m = len(X) 
    n = len(Y) 
      
    # LCSuff is the table with zero  
    # value initially in each cell 
    position = 0

    LCSuff = [[0 for k in range(n+1)] for l in range(m+1)] 
      
    # To store the length of  
    # longest common substring 
    result = 0 
  
    # Following steps to build 
    # LCSuff[m+1][n+1] in bottom up fashion 
    for i in range(m + 1): 
        for j in range(n + 1): 
            if (i == 0 or j == 0): 
                LCSuff[i][j] = 0
            elif (X[i-1] == Y[j-1]): 
                LCSuff[i][j] = LCSuff[i-1][j-1] + 1
                # print(str(result) + ' ' + str(LCSuff[i][j]))
                if LCSuff[i][j] > result:
                    print(str(i) + ' ' + str(j))
                    position = i
                result = max(result, LCSuff[i][j])
            else: 
                LCSuff[i][j] = 0
    return (result, X[(position-result):position])


# def specialLCS(X , Y, hid1='None', hid2='None', nameBoth1='None', nameBoth2='None'):
# # def specialLCS(X , Y, each1, each2):
#     # connect("extensionsASTnpantel", host="hulk.csc.ncsu.edu", port=27077)
#     # find the length of the strings 
#     m = len(X) 
#     n = len(Y) 
  
#     # declaring the array for storing the dp values 
#     # nice line
#     L = [[None]*(n+1) for i in range(m+1)] 
  
#     """Following steps build L[m+1][n+1] in bottom up fashion 
#     Note: L[i][j] contains length of LCS of X[0..i-1] 
#     and Y[0..j-1]"""
#     for i in range(m+1): 
#         for j in range(n+1): 
#             if i == 0 or j == 0 : 
#                 L[i][j] = 0
#             elif X[i-1] == Y[j-1]: 
#                 L[i][j] = L[i-1][j-1]+1
#             else: 
#                 L[i][j] = max(L[i-1][j] , L[i][j-1]) 
#     # Lists Similarity
#     sm=difflib.SequenceMatcher(None,X,Y)
#     # add to database
#     dTable = mongo.diffStore1(hid1=hid1, hid2=hid2, nameBoth1=nameBoth1, nameBoth2=nameBoth2, commonLength=L[m][n], similarityRatio=sm.ratio())
#     # dTable = mongo.diffStore(hid1='abc', hid2='def', commonLength=L[m][n])
#     dTable.save()
#     print("saved")
#     # L[m][n] contains the length of LCS of X[0..n-1] & Y[0..m-1] 
#     return L[m][n] 
#     #end of function lcs 


# def putInDatabase(inDir):
#     count = 0 
#     for eachFile in os.listdir(inDir):
#         # print(eachFile)
#         hid1 = eachFile.split('-')[0]
#         nameBoth1 = eachFile
#         fileAst1 = open(inDir + '/' + eachFile, 'rb')
#         dbTable = mongo.AstDiffFiles(hid=hid1, nameBoth=nameBoth1)
#         dbTable.fileAst.put(fileAst1)
#         dbTable.save()
#         count += 1
#         print("Progress = %s/330k" % count)