def main():
	fIn = open("./allURLsCorrect.txt", 'r')
	for count in range(0,6):
		f = open("urls" + str(count) + ".txt", 'w+')
		for i in range(0,25000):
			f.write(fIn.readline())
	theRest = fIn.readlines()
	for rest in theRest:
		f.write(rest)
	f.close()

if __name__ == '__main__':
    main()