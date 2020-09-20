from topia.termextract import extract, tag
import re
# from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
# import matplotlib.pyplot as plt


def taggerTest():
	reviews = open("./crawled/concatReviews.txt").readlines()
	# tagger = tag.Tagger()
	# tagger.initialize()
	# for line in reviews:
	# 	if( (line.split('//')[0] != 'https:') & (len(line) > 1) & (line[0] != '-') ):
			# print(tagger.tokenize(line))
			# extractor = extract.TermExtractor(tagger)
			# extractor.filter = extract.permissiveFilter
			# extractor.filter = extract.DefaultFilter(singleStrengthMinOccur=10)
			# extracted = extractor(reviews)
			# printTaggedTerms(extracted)

def extractorTest():
	reviews = open("./crawled/concatReviews.txt").read()
	extractorOut = open("./taggers/extractorOut.txt", 'w+')
	extractor = extract.TermExtractor()
	# print(extractor(reviews))
	for extension in re.split('-{41,}', reviews):
		extractorOut.write(str(extractor(str(extension))) + '\n')

# def wordcloudTest():
# 	reviews = open("./crawled/concatReviews.txt").read()
# 	reviews = removeCertainWords(reviews)
# 	wordcloud = WordCloud().generate(reviews)
# 	# Display the generated image:
# 	plt.imshow(wordcloud, interpolation='bilinear')
# 	plt.axis("off")
# 	plt.show()

# def removeCertainWords(query):
# 	stopwords = ['https','chrome','google']
# 	newQuery = []
# 	print(len(query.split('\n')))
# 	for line in query.split('\n'):
# 		if( (line.split('//')[0] != 'https:') & (len(line) > 1) ):
# 			newQuery.append(line)
# 	return ' '.join(newQuery)

if __name__ == '__main__':
	taggerTest()
	# extractorTest()
	# wordcloudTest()