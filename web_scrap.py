'''
Author: <Johnny Hsu, aka. Yu Wei, Hsu>
Date: <09/29/2016>
Version: 0.1
Description: Web Scraping from Trulia.com
'''



import requests
from bs4 import BeautifulSoup
import json
import os     
import argparse


parser = argparse.ArgumentParser(usage='web_scrap.py file [-a] [-j] [-p]')
parser.add_argument("file", type = str, help = "assign txt file includng links separated by newline chracter")
# parser.add_argument("option", type = str, help = " all , photo, json")
parser.add_argument("-a", help = "download the json and photo", action="store_true")
parser.add_argument("-j", help = "download the json only", action="store_true")
parser.add_argument("-p", help = "download the photo only ", action="store_true")


args = parser.parse_args()



def get_soup(url):
 
	if not url:
		raise RuntimeError('url must be specified.')
	else:
		return BeautifulSoup(requests.get(url).content, "lxml")


def get_list(url = None, html_tag = None, css_class = None , data = {} , key = ""):
	
	soup = get_soup(url)
	
	if url not in data:
		data[url] = {}
	if key not in data:
		data[url][key] = []
   
	if css_class:
		uls = soup.find_all(html_tag, class_ = css_class)
	else:         
		uls = soup.find_all(html_tag)

	for ul_top in uls:
		for ul in ul_top.find_all("ul"):
				for li in ul.find_all("li"):
					data[url][key].append(li.get_text())


def get_table(url = None, html_tag = None, css_class= None , data = {} , key = ""):

	soup = get_soup(url)
	if url not in data:
		data[url] = {}
	if key not in data:
		data[url][key] = []

	if css_class:
		tables = soup.find_all(html_tag, class_ = css_class)
	else:         
		tables = soup.find_all(html_tag)

	for table in tables:
		for row in table.find_all("tr"):
				for td in row.find_all("td"):
					if "\xa0" not in td.get_text(): 
						data[url][key].append( " ".join(td.get_text().replace("\n","").split() )) 
 

def get_image(url = None, html_tag = None, css_class = None , attribute = None):

	soup = get_soup(url)
	try:
		if css_class:
			images_element = soup.find_all(html_tag, class_ = css_class)
		else:         
			images_element = soup.find_all(html_tag)
	

		image_urls =[]
		i = 0
		for image_element in images_element:
			image_attr = image_element[attribute]
			
			if attribute == "style":
				image_urls.append("http:" + image_attr[image_attr.find("('")+len("('"): image_attr.find("')")])
			elif attribute == "src":
				image_urls.append("http:" + image_attr)
	
			image = requests.get(image_urls[i]).content
			if len(image_urls) == 1:
				fname = url[url.find("-")+1 :] 
			else:
				fname = url[url.find("-")+1 :] + "_" + repr(i+1)
			
			with open( fname + ".jpg", "wb") as fp:
				fp.write(image)
				i += 1 
	except:
		raise RuntimeError('No Photo found')


def main():
	
	data = {}

	with open(args.file, "r") as f:
		for link in f:
			url = link.strip()

			# if args.option == "json" or args.option == "all":
			if args.j or args.a :
				# Get Features
				html_tag ="ul"
				css_class = "listInline pdpFeatureList"
				key = "Features"
				get_list(url, html_tag, css_class, data, key)
				
				# Get Public Records
				html_tag ="ul"
				css_class = "listInline mbn pdpFeatureList"
				key = "Public Records"
				get_list(url, html_tag, css_class, data, key)
				

				# Get Price History
				html_tag ="table"
				css_class = "table tableRowBorderedTop tableRowBorderedBottom txtL"
				key = "Price History"
				get_table(url, html_tag, css_class, data, key)

				# Get Real Estate Trend
				html_tag ="table"
				css_class = "table tableHover tableRowBorderedTop tableRowBorderedBottom txtR"
				key = "Real Estate Trends"
				get_table(url, html_tag, css_class, data, key)
		
			# if args.option == "photo" or args.option == "all":
			if args.p or args.a :
				html_tag = "div"
				css_class = "photoPlayerCurrentItem txtM"
				attribute = "style"
				get_image(url, html_tag, css_class, attribute)
		
		fname = args.file[0 : args.file.find(".")]
		with open( fname + '.json', 'w') as fp:
			json.dump(data, fp)




if __name__ == '__main__':
	main()