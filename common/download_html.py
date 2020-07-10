import urllib.request as urllib2
from bs4 import *
from urllib.parse import urljoin


def crawl(pages: list, depth=None):
    indexed_url = []  # a list for the main and sub-HTML websites in the main website
    for i in range(depth):
        for page in pages:
            if page not in indexed_url:
                indexed_url.append(page)
                try:
                    c = urllib2.urlopen(page)
                except:
                    print("Could not open %s" % page)
                    continue
                soup = BeautifulSoup(c.read(), features="lxml")
                links = soup('a')  # finding all the sub_links
                for link in links:
                    if 'href' in dict(link.attrs):
                        url = urljoin(page, link['href'])
                        if url.find("'") != -1:
                            continue
                        url = url.split('#')[0]
                        if url[0:4] == 'http' and url!=page:
                            indexed_url.append(url)
        pages = indexed_url
    return indexed_url


pagelist = ["https://docs.spring.io/spring-framework/docs/5.0.x/spring-framework-reference/core.html"]
urls = crawl(pagelist, depth=1)
print(urls)
