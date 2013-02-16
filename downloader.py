import requests
import time
import os
import sys
from pyquery import PyQuery as pq
from lxml import etree

def downloadImages():
	'''
		The script will loop over a list of subreddits and then download
		any images that were uploaded to imgur.

		All pics downloaded are stored in a pics folder in the current directory
		and then in a subdir within that.

		The script will also loop over 20 pages based on the top monthly posts.
		You can set maxPageToGrab to 1 if you want to only grab the latest images.
	
		The script will only images that have not been downloaded before.
		
	'''
	groups = ['wallpapers']
	maxPagesToGrab = 20
	if not os.path.exists('./pics/'):
		os.mkdir('./pics/')
	for page in range(maxPagesToGrab):
		for group in groups:
			subgroup = group
			if not os.path.exists('./pics/%s'%subgroup):
				os.mkdir('./pics/%s/'%subgroup)

			folder = requests.get('http://imgur.com/r/%s/new/month/page/%d'%(subgroup,page))
			d = pq(folder.content.decode('utf-8'))
			links = d("a")
			for link in links:
				if len(link):
					url = (link.attrib['href'])
					if not url.startswith('http') and not (url.find('rss') != -1 or url.find('javascript') != -1):
						print(url)
						r = requests.get('http://imgur.com%s'%url)
						if r.status_code == requests.codes.ok:
							directImage = pq(r.content.decode('utf-8'))
							directUrl = directImage('link[rel="image_src"]')
							directUrl = directUrl[0].attrib['href']
							finalImage = requests.get(directUrl)

							if finalImage.status_code == requests.codes.ok:
								downloadedFileName = directUrl.split('/')[-1]
								if not os.path.exists('./pics/%s/%s'%(subgroup,downloadedFileName)):
									dumper = open('./pics/%s/%s'%(subgroup,downloadedFileName),'wb')
									dumper.write(finalImage.content)
									dumper.close()
								else:
									print('skipping')
							#Sleep is to prevent hitting any limits per ip
							time.sleep(1)

if __name__ == '__main__':
	downloadImages()
