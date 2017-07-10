import sys
import csv
import urllib2
import obo

class Article(object):
	date = ""
	time = ""
	keywords = ""
	frequency = 0
	sourceUrl = ""
	score = 0

	def __init__(self, date, keywords, frequency, sourceUrl, score):
        	self.date = date
		self.keywords = keywords
		self.frequency = frequency
		self.sourceUrl = sourceUrl
		self.score = score

	def get_date(self):
		return self.date;
	def get_time(self):
		return self.time;
	def get_keywords(self):
		return self.keywords;
	def get_sourceUrl(self):
		return self.sourceUrl;


keywords = ["streaming music service", "music royalty", "windfall", "must sell", "must buy", "dispute", "bad" "culture", "for sale", "beyond connectig", "monthly users", "meaningful", "nearing completion", "biggest jump", "fast money", "consumer reports", "boost targets", "stock surge", "exceeded", "dipped", "stock-rating upgrades", "target hike", "streaming","music","service","music","royalty","windfall","must","sell","must","buy","dispute","bad","culture","sale","beyond","connecting","monthly","users","meaningful","nearing","completion","biggest","jump","fast","money","consumer","reports","boost","targets","stock","surge","exceeded","dipped","stock-rating","upgrades","target","hike","penalties","online","hate","punish","poisonous","propaganda","concrete","lose","millions","extremism","growth","prediction","fake","news","global","policy","whitelist","record","breaking","hypermiling","new","record","cash","pile","pretty","powerful","polarized","repatriate","just","plain","weird","clunky","devices","killer","devices","other","competitors","vacuum","over","the","fence","cutting-edge","surface","tension","sparked","fears","builds","trust","big","initiative","devices","infected","fireball","overblown","ransomware","threat","real","fake","pages","bogus","search","number","one","network","speeds","digital","data","mimo","fastest","closures","boutique","equity","struggled","terrified","venturing","off","relationships","breaking","news","niche","leg","up","real","play"]


#Main Method
def main():
	urlList = []
	for arg in sys.argv[1:]:
		urlList.append(str(arg))
	ArrayArticle=[[0 for _ in range(len(keywords)+1)] for _ in range(len(urlList))]
	for i in range(len(urlList)):
		response = urllib2.urlopen(urlList[i])
		html = response.read()
		text = obo.stripTags(html).lower()
		#not required in the sample case
		#dictionary = obo.wordListToFreqDict(wordlist)
		#sorteddict = obo.sortFreqDict(dictionary)
		#Preparing the array of object
		getKeywordHits(text,urlList[i], i, ArrayArticle)



def getKeywordHits(text, url, url_number, tobeModified):
	j = 0
	for i in range(len(keywords)):
		search_word = keywords[i]
		count = text.count(search_word)
		tobeModified[url_number][i] = count
		j=i
	tobeModified[url_number][j+1] = url
	#print ArrayArticle[url_number][j+1]

	# Writing to the file
	with open('TEST.csv', 'w') as outcsv:
		writer = csv.writer(outcsv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')

    		for i in range(len(tobeModified)):
       	#Write item to outcsv
		#with open('output.csv', 'w') as outcsv:
        		writer.writerow(tobeModified[i])


if __name__ == "__main__":
    main()
