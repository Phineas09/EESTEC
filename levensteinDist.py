from Levenshtein import distance as lev

def getClosestString(stringList, result):
	if result is None:
		return "ERROR"
	minDist = 100000;
	minString = ""
	for i in stringList:
		if lev(i,result) < minDist:
			minDist = lev(i,result)
			minString = i
	return minString