def main():
	fIn1 = open("./malicious_extension_names.txt", 'r').readlines()
	fOut = open("./nameIdMatchingResultFile.txt", 'w+')

	for each in fIn1:
		fIn2 = open("./testOutput.json", 'r').readlines()
		for line in fIn2:
			# print( "each = " + str(each))
			# print( "line = " + str(line))
			if str(each) in str(line):
				fOut.write(line)
		fIn2.close()
	fIn1.close()
	fOut.close()

if __name__ == '__main__':
    main()