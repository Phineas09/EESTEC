from Levenshtein import distance as lev
import re
from w2n import word_to_num
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


def getNumberFromWord(word):
	return word_to_num(word)
	