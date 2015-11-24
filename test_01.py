#coding: utf-8
import urllib
import urllib2
import re

baseUrl = 'http://www.hao123.com/'
urlList = [baseUrl]
crawledUrls = []

def getPage(url):
	try:
		request = urllib2.Request(url)
		response = urllib2.urlopen(request)
		return response.read()
	except urllib2.URLError, e:
		if hasattr(e, "reason"):
			print u"connection failed caused by",e.reason
			return None

def getURL(page):
	if page == None:
		return []
	pattern = re.compile('<a href="(.*?)".*?>.*?</a>',re.S)
	items = re.findall(pattern,page)
	tempList = []
	for item in items:
		if item.find("mail.xjtu.edu.cn") != -1:
			continue
		if item.find(".jsp") != -1:
			continue
		if item.find("http://") != -1:
			tempList.append(item)
		else:
			tempUrl = baseUrl + str(item)
			tempList.append(tempUrl)
		print tempList
		return tempList


def startCrawl(urlList):
	temp = []
	for url in urlList:
		urlList.remove(url)
		if url in crawledUrls:
			continue
		crawledUrls.append(url)
		print url,len(urlList)
		temp = getURL(getPage(url))
		print temp
		temp.extend(urlList)
		temp1 = list(set(temp))
		startCrawl(temp1)

startCrawl(urlList)