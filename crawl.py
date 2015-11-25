#coding: utf-8
import urllib
import urllib2
import re
import os, errno

baseUrl = 'http://www.xjtu.edu.cn'
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
		if item.find("..") != -1:
			continue
		if item.find("xjtu") != -1:
			if item.find("http://") != -1:
				tempList.append(item)
			else:
				tempUrl = baseUrl + str(item)
				tempList.append(tempUrl)
	return tempList

def writeData(url):
	file = None;
	file = open(getFilePath(url), "w+")
	page = getPage(url)
	if(page == None):
		return 
	else:
		file.write(page)

def getFilePath(url):
	url = url.replace('http:/','data')
	dir = os.path.split(url)
	if(dir[0] == 'data' or dir[1] == ''):
		if(not os.path.exists(url)):
			os.makedirs(url)
		return url + '/origin.htm'
	else:
		if(not os.path.exists(dir[0])):
			os.makedirs(dir[0])
		return url

def startCrawl(urlList):
	temp = []
	for url in urlList:
		urlList.remove(url)
		if url in crawledUrls:
			continue
		writeData(url)
		crawledUrls.append(url)
		print url,len(urlList)
		temp = getURL(getPage(url))
		temp.extend(urlList)
		temp1 = list(set(temp))
		startCrawl(temp1)

startCrawl(urlList)
#writeData('http://www.xjtu.edu.cn')
