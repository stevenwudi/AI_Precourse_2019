# -*- coding: utf-8 -*-
import os
from icrawler.builtin import BingImageCrawler
from pypinyin import pinyin, lazy_pinyin
def BingImage(fpath,spath):
	path = r'.\\Star\\'+fpath
	f = open(spath, 'r')
	lines = f.readlines()
	k = 0
	for i, line in enumerate(lines):
	    name = line.strip('\n')
	    En_name = ''.join(lazy_pinyin(name))
	    file_path = os.path.join(path, En_name)
	    if not os.path.exists(file_path):
	        os.makedirs(file_path)
	    bing_storage = {'root_dir': file_path}
	    bing_crawler = BingImageCrawler(parser_threads=2, downloader_threads=4, storage=bing_storage)
	    bing_crawler.crawl(keyword=name, max_num=10)
	    print('第{}位明星：{}'.format(i, name))
	    k+=1
	    if k==50:
	    	break
if __name__ == '__main__':
	fpath = ['maleStar','femaleStar']
	spath = ['maleStarName.txt','femaleStarName.txt']
	for i in range(len(fpath)):
		BingImage(fpath[i],spath[i])