import bs4 as bs
import os
import re, sys
from urllib.request import Request, urlopen

class Crawler:
    def __init__(self, domain):
        self.domain = domain


    def get_robots_txt(self):
        req = Request("{0}/robots.txt".format(self.domain), headers = {'User-Agent': 'Mozilla/5.0'})
        response = urlopen(req)
        return bs.BeautifulSoup(response, 'html.parser', from_encoding=response.info().get_param('charset'))


    def get_sitemaps(self, robots):
        """Parse a robots.txt file and return a Python list containing any sitemap URLs found.

        Args:
            robots (string): Contents of robots.txt file.
        
        Returns:
            data (list): List containing each sitemap found.
        """

        data = []
        lines = str(robots).splitlines()

        for line in lines:
            if line.startswith('Sitemap:'):
                split = line.split(':', maxsplit=1)
                data.append(split[1].strip())

        return data

    def get_uniq_links_from_sitemaps(self, sitemaps):
        """Parse a sitemap file and return a Python list containing all uniq URLs found.

        Args:
            sitemaps (list): list of sitemap file urls
        
        Returns:
            data (list): List containing each unique URL found.
        """
        links = set()
        for sitemap in sitemaps:
          req = Request(sitemap, headers = {'User-Agent': 'Mozilla/5.0'})
          response = urlopen(req)
          content = bs.BeautifulSoup(response, 'xml', from_encoding=response.info().get_param('charset'))
          for loc in content.find_all('loc'):
              links.add(loc.get_text(strip=True))
        return links

    def crawl_page(self, link):
        req = Request(link, headers = {'User-Agent': 'Mozilla/5.0'})
        res = urlopen(req)
        soup = bs.BeautifulSoup(res, 'html.parser')

        entry = soup.find(class_='h-entry')
        title=''
        tags=[]
        summary=''
        content=''

        if entry is not None:
            title = entry.find(class_='p-name')
            tags = entry.find_all(class_='p-category')
            summary = entry.find(class_='p-summary')
            content = entry.find(class_='e-content')
        
        return {
            "url": link,
            "title" : self.get_value(title),
            "summary": self.get_value(summary),
            "content": self.get_value(content),
            "tags": self.get_values_as_str(tags)
        }

    def get_values_as_str(self, elements):
       return  ' '.join(list(map(lambda element: self.get_value(element), elements)))

    def get_value(self, element):
        return element.get_text() if element else ''
    
    def start(self):
        robots = self.get_robots_txt()
        sitemaps=self.get_sitemaps(robots)

        data = []
        for link in self.get_uniq_links_from_sitemaps(sitemaps):
            data.append(self.crawl_page(link))
        return data
        
