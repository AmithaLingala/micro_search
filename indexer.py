from crawler import Crawler

SITES=["https://exeami.com", "https://codingotaku.com"]

if __name__ == '__main__':
    for site in SITES:
      print("crawling {0}".format(site))
      crawler = Crawler(site)
      crawler.start()
