from bs4 import BeautifulSoup
import requests
import re
import timestring
import os
import argparse

def main():

	parser = argparse.ArgumentParser(description='You a Gawker author? This will scrape some content for you.')
	parser.add_argument('--user', help='username you want to scrape', required=True)
	parser.add_argument('--notitle', dest='noTitle', type=int)
	parser.add_argument('--nextOne', dest='nextOne')
	parser.set_defaults(noTitle=1)	
	parser.set_defaults(nextOne="")	

	args = parser.parse_args()

	url = "http://kinja.com/" + args.user
	notitle = args.noTitle
	# Leave nextOne blank to start at the beginning of a writer's history. If the script errorred and you want to pick up where you left off, add the most recent ?startswith code that was printed out to the console here.
	nextOne = args.nextOne
	keepGoing = True
	# Change below to the URL of the person's Kinja author profile. NOT their kinja site I.E. name.kinja.com, but their profile I.E. kinja.com/name

	print "Starting download for " % args.user
	
	while keepGoing:
		if nextOne != '':
			print("If the script fails, run this next: python gawker.py --user %s --nextOne %s" % (args.user, nextOne))
		keepGoing = False
		page = requests.get(url + nextOne).text
		soup = BeautifulSoup(page, "html.parser")
		pageLinks = []
		for link in soup.findAll("a", {"class": "js_entry-link"}):
			l = link.get("href")
			if l not in pageLinks:
				pageLinks.append(l)
		for link in soup.findAll("a"):
			if link.get("href") is not None and link.get("href").startswith("?startTime=") == True and link.get("href") != nextOne:
				nextOne = link.get("href")
				keepGoing = True
		for a in pageLinks:
			articlePageRequest = requests.get(a)
			if articlePageRequest.status_code != 200:
				print("Error fetching article: " + a)
				print(articlePageRequest.reason)
				return
			articlePage = requests.get(a).text

			pageSoup = BeautifulSoup(articlePage, "html.parser")
			timeObject = pageSoup.findAll("a", {"class":"js_entry-link js_publish_time"})
			time = timestring.Date(timeObject[0].text)
			filepath = args.user + "/" + str(time.year) + "/" + str(time.month) + "/"
			preTitle = pageSoup.title.text
			if pageSoup.p is not None:
				if preTitle == "Jezebel":
					preTitle = pageSoup.p.text
					if preTitle is None:
						preTitle = "No_title_available" + str(notitle)
						notitle += 1
			if len(preTitle) > 50:
				preTitle = preTitle[:50]
				preTitle = preTitle.replace(" ", "_")
			postTitle = "".join([c for c in preTitle if re.match(r"\w", c)])
			fullTitle = filepath + postTitle
			if not os.path.exists(os.path.dirname(fullTitle)):
				try:
					os.makedirs(os.path.dirname(fullTitle))
				except OSError as exc:
					if exc.errno != errno.EEXIST:
						raise
			if os.path.isfile(fullTitle):
				fullTitle = fullTitle + str(notitle)
				notitle += 1
			with open(fullTitle + ".txt", "w") as f:
				f.write(("HEADLINE: " + pageSoup.title.text + "\n").encode('utf8'))
				f.write(("Published on " + timeObject[0].text + "\n").encode('utf8'))
				f.write(("Original URL : " + a + "\n\n").encode('utf8'))
				for graf in pageSoup.findAll("p"):
					f.write((graf.text + "\n").encode('utf8'))
	print "Completed Successfully!"

if __name__ == "__main__": main()