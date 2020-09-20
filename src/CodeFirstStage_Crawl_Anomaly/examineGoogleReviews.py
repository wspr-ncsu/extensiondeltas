import re
import numpy as np

def search12Names():
	namesFile = open('./googleExtensions/names_with_anomalies.txt', 'r').readlines()
	filename = "./crawled/concatScores.txt"
	allScores = open(filename, 'r').read()
	googleCounter = 0     
	blocks = re.split('-{40,}', allScores)
	googleBlocks = []
	for block in blocks:
		block = block.split('\n')
		googleNameFile = namesFile
		for googleName in googleNameFile:
			if( ( block[1].split('/')[-1] in googleName.split('/')[-1] ) & (len(block[1]) > 0)):
				googleCounter +=1
				googleBlocks.append(block)
	# GET ALSO FROM REVIEWS
	filename = "./crawled/concatReviews.txt"
	allScores = open(filename, 'r').read()
	googleCounterR = 0     
	blocks = re.split('-{41,}', allScores)
	googleBlocksR = []
	print(len(blocks))
	for block in blocks[1:]:
		block = block.split('\n')
		googleNameFile = namesFile
		for googleName in googleNameFile:
			if(len(block) > 1):
				if( ( block[1].split('/')[-1] in googleName.split('/')[-1] )  & (len(block[1]) > 0)):
					googleCounterR +=1
					googleBlocksR.append(block)
	oneReviews = 0
	ones = 0
	oneReviewFile = open('./googleExtensions/oneReviewsComments.txt', 'w')
	for (ext1,ext2) in zip(googleBlocks,googleBlocksR):
		for eachScore in ext1:
			scoreLine = eachScore.split('\t')[0]
			if(str(scoreLine) == '1'):	
				ones +=1
				dateLine = eachScore.split('\t')[1]	
				for review in ext2:
					if(str(review.split('\t')[-1]) == str(dateLine)):
						oneReviews += 1
						oneReviewFile.write(review + ext2[1] + '\n')
	print(ones)
	print(oneReviews)

if __name__ == '__main__':
	search12Names()