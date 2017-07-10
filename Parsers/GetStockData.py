import feedparser
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

SourceURL = [[3,'the guardian','https://www.theguardian.com/uk-news/2017/jun/13/google-and-facebook-face-penalties-if-they-dont-stop-online-hate'],
	[1,'the guardian','https://www.theguardian.com/media/2017/jun/22/google-facebook-ads-extremist-content-advertisers-group-m'],
	[9,'futurism','https://futurism.com/a-tesla-just-drove-a-record-breaking-900-kilometers-on-a-single-charge/'],
	[9,'fortune','http://fortune.com/2017/06/22/tech-automation-jobs/'],
	[8,'qz','https://qz.com/1008428/why-apples-next-big-investment-should-be-reshaping-capitalism/'],
	[9,'business insider','http://www.businessinsider.com/microsoft-how-windows-10-pcs-got-cool-2017-6'],
	[2,'cnet','https://www.cnet.com/news/microsoft-250-million-devices-infected-with-fireball-virus-is-overblown/'],
	[7,'telecompetitor','http://www.telecompetitor.com/verizon-wireless-beats-back-t-mobile-for-pc-magazines-fastest-u-s-mobile-network-title/'],
	[7,'bgr','http://bgr.com/2017/06/21/sprint-4g-lte-test-vs-verizon-network-coverage/'],
	[1,'business insider','http://www.businessinsider.com/sears-is-closing-more-stores-2017-6'],
	[7,'cnbc','http://www.cnbc.com/2017/06/21/twitter-report-of-strong-advertiser-outlook.html'],
	[4,'bloomberg','https://www.bloomberg.com/news/articles/2017-06-20/oil-bear-market-to-hit-asia-stocks-china-in-msci-markets-wrap'],
	[8,'reuters','https://www.reuters.com/article/us-usa-banks-stress-idUSKBN19D2OC']]

sourceURL2 = [[3, 'slate', 'http://www.slate.com/articles/news_and_politics/interrogation/2017/06/is_the_mess_at_uber_all_travis_kalanick_s_fault.html'
], 
	[2, 'nasdaq', 'http://www.nasdaq.com/article/sears-closing-dozens-more-stores-20170607-00732'
],
	[3, 'washingtonpost', 'https://www.washingtonpost.com/news/wonk/wp/2017/06/22/trump-visited-this-boeing-factory-to-celebrate-jobs-it-just-announced-layoffs/?utm_term=.3e7adc90a824'],
	[5, 'nasdaq','http://www.nasdaq.com/article/conocophillips-not-a-buy-despite-major-positive-goldman-sachs-says-cm806786'],
	[1, 'reuters','https://www.reuters.com/article/us-usa-brazil-beef-idUSKBN19D2VE'],

	[7, 'investorplace', 'http://investorplace.com/2017/06/why-under-armour-inc-uaa-stock-is-heading-to-25/#.WUy33saZNPM'],
	[7, 'fool', 'https://www.fool.com/investing/2017/06/22/grocery-aisles-and-e-commerce-collide-with-whole-f.aspx']
]

#ArrayArticle=[[0 for _ in range(len(keywords)+2)] for _ in range(21)]
ArrayArticle=[[0 for _ in range(len(keywords)+1)] for _ in range(21)]

def getKeywordHits(text, url, url_number):
	j = 0
	for i in range(len(keywords)):
		search_word = keywords[i]
		count = text.count(search_word)
		ArrayArticle[url_number][i] = count
		j=i
	ArrayArticle[url_number][j+1] = url
	print ArrayArticle[url_number][j+1]


def getScores(text, url, score, url_number):
	j = 0
	for i in range(len(keywords)):
		search_word = keywords[i]
		count = text.count(search_word)
		ArrayArticle[url_number][i] = count
		j=i
	ArrayArticle[url_number][j+1] = url
	ArrayArticle[url_number][j+2] = score

#Main Method
def main():

	for arg in sys.argv[1:]:
		input = str(arg)
		url = "https://feeds.finance.yahoo.com/rss/2.0/headline?s="+input+"&region=US&lang=en-US"
		print url

	d = feedparser.parse(url)
	print d['feed']['title']
	print len(d['entries'])
	
	for entry in d.entries:
		date = entry.published
		#print date
		description = entry.description
		#print description
		url = entry.link
		#print url
		numOfEntries = len(d['entries'])
		getKeywordHits(description.lower(),url,d.entries.index(entry))

	# Writing to the file
	with open('AMZNactualData.csv', 'w') as outcsv:
		writer = csv.writer(outcsv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
    	
    		for i in range(len(ArrayArticle)):
       	#Write item to outcsv
		#with open('output.csv', 'w') as outcsv:
			
        		writer.writerow(ArrayArticle[i])

	#if f != 0:
		#totalHits += f
	
        
if __name__ == "__main__":
    main()



	

