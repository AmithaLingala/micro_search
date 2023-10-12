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
        entries = soup.find_all(class_='h-entry')

        for entry in entries:
            print("Link: {0}\n".format(link))

            title = entry.find(class_='p-name')
            if title is not None:
                print(title.get_text(strip=True))

            tags = entry.find_all(class_='p-category')
            if tags is not None:
                print(list(map(lambda tag: tag.get_text(strip=True), tags)))
            summary = entry.find(class_='p-summary')
            if summary is not None:
                print(summary.get_text(strip=True))

            content = entry.find(class_='e-content')
            if content is not None:
                print(content.get_text(strip=True))
            
            print("\n\n")
        
    def start(self):
        robots = self.get_robots_txt();
        sitemaps=self.get_sitemaps(robots)
        for link in self.get_uniq_links_from_sitemaps(sitemaps):
            self.crawl_page(link)

        
