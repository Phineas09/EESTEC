from Levenshtein import distance as lev
import re
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

def getYear(res):
	r = re.search('[0-9]{3,4}', res).group(0);
	if r is not None:
		return r
	return res
	