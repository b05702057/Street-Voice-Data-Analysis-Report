#透過Python取得streetvoice排行資料
#使用requests套件的requests.get()方法
import requests
from bs4 import BeautifulSoup
from lxml import etree
import re
# from selenium import webdriver
# import time
import pandas as pd

u_list = []
for i in range(6):
	u = 'https://streetvoice.com/music/charts/' + str(i) + '/'
	u_list.append(u)

def get_html(url):
	#模擬訪問頁面的函數
	try:
		user_agent = 'Mozilla/5.0'
		resp = requests.get(url, headers={'User-Agent': user_agent}, timeout = 30) #回傳為一個request.Response的物件
		resp.endcodding = 'utf8'
		response = resp.content.decode()
		return response 
	except:
		return 'ERROR'

#print(resp.status_code)
#物件的statu_code屬性取得server回覆的狀態碼(200表示正常,404表示找不到網頁,之前一直503???)
#print(resp.text)

def get_url(url):
	#函數用來找出單一網頁的歌手連結
	html = get_html(url)
	singers = []
	tree = etree.HTML(html)
	#result = etree.tostring(tree, pretty_print = True, method = "html")
	for i in tree.xpath('//*[@id="item_box_list"]/table/tbody/tr/td[2]/a'):
		singer = i.xpath('string(.)')
		singer_url = i.xpath('@href')
		for i in singer_url:#處理莫名的[]
			singers.append(i)
	return singers

def singer_list(num):
	#爬取2018所有類型排行榜上所有不重複的歌手連結
	url_list = []
	singer_set = set()
	for j in u_list:
		for i in range(num):
			url = j + '2018/' + str(i+1) + '/'
			k = set(get_url(url)) #各週的排行榜不重複歌手連結
			singer_set.update(k) 
		#print(singer_set)檢查正確
	singer_set = list(singer_set)
	singer_list = []
	for eachsinger in singer_set: #把前面爬的變成網址形式
		eachsinger = 'https://streetvoice.com' + eachsinger + 'songs/'
		singer_list.append(eachsinger)
	return singer_list

def get_content(url):
	#函數用來取得想要的數據
	html = get_html(url)
	tree = etree.HTML(html)
	count_songs = 0
	songs_like_list = []
	new_like_list = []
	#每個歌手的名字
	#//*[@id="inside_box"]/div[2]/div[1]/div/div[2]/div[1]/div[1]/h1
	singer_name = tree.xpath('//*[@id="inside_box"]/div[2]/div[1]/div/div[2]/div[1]/div[1]/h1/text()')[0]

	#//*[@id="countup-follower"]
	#//*[@id="inside_box"]/div[2]/div[1]/div/div[2]/div[3]/div[1]/ul/li[2]/
	#//*[@id="inside_box"]/div[2]/div[1]/div/div[2]/div[3]/div[1]/ul/li[2]
	singer_follower = tree.xpath('//*[@id="pjax-container"]/script/text()')[0].strip() #返回list
	all_imformation = re.findall("\\d+", singer_follower)
	singer_follower_count = int(all_imformation[1])
	count_songs = int(all_imformation[0])
#這邊有問題，一直出現'0'
	#soup = BeautifulSoup(html, 'html.parser')
	#singer_follower = soup#.findall('h2', id = "countup-follower")

#	try:
	#找出每首歌的網址
	page = (count_songs//24) + 1
	lastpage_num = (count_songs % 24)
	if lastpage_num == 0:
		page -= 1
		lastpage_num = 24
	song_url_list = []
	for i in range(page):
		page_url = url + '?page=' + str(i + 1)
		page_html = get_html(page_url)
		page_tree = etree.HTML(page_html)
		num = 24
		if i + 1 == page:
			num = lastpage_num	
		try:
			for j in range(num):
				path = '//*[@id="item_box_list"]/div[' + str(j+1) + ']/div[2]/h4/a'
				for k in page_tree.xpath(path):
					song_partial_url1 = k.xpath('@href')
				song_partial_url = song_partial_url1[0]
				song_url = 'https://streetvoice.com' + song_partial_url
				song_url_list.append(song_url)
		except:
			for j in range(num):
				path = "//div[@id='item_box_list']/div[" + str(j+1) + "]/div[2]/div[1]/h4/a"
				for k in page_tree.xpath(path):
					song_partial_url1 = k.xpath('@href')
				song_partial_url = song_partial_url1[0]
				song_url = 'https://streetvoice.com' + song_partial_url
				song_url_list.append(song_url)
	first_song_url = song_url_list[-1]			

	#取得播放次數、喜歡數跟得獎加權分數
	rankDict = {'播放次數' : 0, '喜歡' : 0}
	play = 0
	like = 0
	for song in song_url_list:
		html = get_html(song)
		tree = etree.HTML(html)
		n = 1
		while True:
			try:
				rank = tree.xpath('//*[@id="inside_box"]/div[2]/div/div[1]/div[2]/ul/li[' + str(n) + ']/h5/text()')
				if rank[0] not in rankDict: 
					rankDict[rank[0]] = 1
					n += 1
				else:
					rankDict[rank[0]] += 1
					n += 1
			except:
				break
		txt = tree.xpath('//*[@id="inside_box"]/div[2]/div/div[1]/script/text()')[0].strip()
		information = re.findall('\\d+', txt)
		play += int(information[0])
		like += int(information[1])
	
	awards = sum(rankDict.values()) - rankDict['播放次數'] - rankDict['喜歡']
	rankDict['播放次數'] = play
	rankDict['喜歡'] = like
	count_play = rankDict['播放次數']
	count_like = rankDict['喜歡']

	#拿到first_song_url，開始訪問並拿發布日期
	first_song_html = get_html(first_song_url)
	first_song_tree = etree.HTML(first_song_html)
	count_tr = 0
	for i in first_song_tree.xpath('//*[@id="inside_box"]/div[1]/div/div/div/div/div[2]/table/tbody/tr/td'):
		count_tr += 1 #檢查count_tr沒錯
	path1 = '//*[@id="inside_box"]/div[1]/div/div/div/div/div[2]/table/tbody/tr[' + str(count_tr) + ']/td/text()'
	first_song_date1 = first_song_tree.xpath(path1)
	#//*[@id="inside_box"]/div[1]/div/div/div/div/div[2]/table/tbody/tr[2]/td
	#上面的date在一個list裡面，要取出來
	first_song_date = str()
	for i in first_song_date1:
		first_song_date += i
		
#	except:
#		first_song_date = 'ERROR'
	return [singer_name, str(singer_follower_count), str(count_songs), str(count_like), str(count_play), str(awards), str(first_song_date)]
	
num = 52 #這裡表示要爬取到2018開始的第幾週
singer_list = singer_list(num)
output = []
song_list = []
for url in singer_list:
	solution = get_content(url)
	output.append(solution)
	print(solution)
# 轉成csv
column_name = ['歌手名', '追蹤數', '歌曲數', '總喜歡數', '總播放次數', '總得獎數','第一首歌發佈日期']
test = pd.DataFrame(columns = column_name, data = output)
test.to_csv('/Users/user/Desktop/result.csv', encoding = 'utf_8_sig') # encoding解決亂碼問題，前面自己設路徑

#solution = get_content('https://streetvoice.com/FrozenStreet/songs/')
#print(solution)









