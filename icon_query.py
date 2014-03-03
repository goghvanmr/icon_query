# -*- coding: utf-8 -*-

import urllib
import re
import xlrd
import xlwt

from xlutils.copy import copy

def parse_search_page(app_name):
	url = 'http://www.wandoujia.com/search?key=%s&source=apps' %app_name

	html_file = urllib.urlopen(url).read()

	pattern_string = '<a href="([\S]*?)" title="%s"[\s\S]*?<span class="install-count">([\s\S]*?)</span>' %app_name

	pattern = re.compile(pattern_string, re.DOTALL)
	
	return pattern.search(html_file)

def get_app_icon_url(app_url):
	html_file = urllib.urlopen(app_url).read()

	pattern_string = '<div class="app-icon">[\s]*?<img src="([\S]*?)"'
	pattern = re.compile(pattern_string)

	result = pattern.search(html_file)

	if result is not None:
		return result.group(1)
	else:
		return "没图，或者没找到"

def main():
	app_name = raw_input('App Name:(end with an enter)')

	parse_result = parse_search_page(app_name)

	if parse_result is not None:
		app_url = parse_result.group(1)
		downloads = parse_result.group(2)
		app_icon = get_app_icon_url(app_url)

		wb_read = xlrd.open_workbook('交付设计师的图标列表.xlsx')
		sh_read = wb_read.sheet_by_index(0)
		first_column_read = sh_read.col_values(0)

		app_name_utf8 = unicode(app_name, "UTF-8")

		if app_name_utf8 in first_column_read:
			print '已经在表里面啦'
		else:
			wb_write = copy(wb_read) 

			sh_write = wb_write.get_sheet(0)
			sh_write.write(len(first_column_read), 0, app_name_utf8)
			sh_write.write(len(first_column_read), 1, app_url)
			sh_write.write(len(first_column_read), 2, app_icon)

			wb_write.save('交付设计师的图标列表.xlsx')
			print '添加成功'

	else:
		print '没这应用，或者没找到'
		return

if __name__ == '__main__':
	main()

