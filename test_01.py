#coding: utf-8
import urllib
import urllib2
import re
import os, errno

baseUrl = 'http://www.xjtu.edu.cn/'
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
	return tempList

def writeData(url):
	file = None;
	file = open(getFilePath(url), "w+")
	file.write(getPage(url))

def getFilePath(url):
	dir = os.path.split(url)
	if(dir[0] == 'http:'):
		try:
			os.makedirs(str(dir[1])	
		except OSError as exc:
			if exc.errno == errno.EEXIST and os.path.isdir(path):
				pass
			else: raise	
		return str(dir[1]) + 'origin.htm'
	else:
		return ''




def startCrawl(urlList):
	temp = []
	for url in urlList:
		urlList.remove(url)
		if url in crawledUrls:
			continue
		crawledUrls.append(url)
		print url,len(urlList)
		temp = getURL(getPage(url))
		temp.extend(urlList)
		temp1 = list(set(temp))
		startCrawl(temp1)

#startCrawl(urlList)
writeData('http://www.xjtu.edu.cn/')
