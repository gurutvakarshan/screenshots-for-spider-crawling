from GoogleScraper import scrape_with_config, GoogleSearchError
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re

class Scrap():
    def ScrapLinksFromBrowser(self):
    # See in the config.cfg file for possible values
        listoflink=[]
        domain=[]
        menubar_links=[]
        dropdown_links=[]
        config = {
            'use_own_ip': True,
            'keyword': 'security brigade',
            'search_engines': [
                        'Google',
                        'Bing',
                        'Yahoo',
                        'Yandex',
                        'Baidu',
                        'Duckduckgo'
            ],
            'num_pages_for_keyword': 2,
            'scrape_method': 'selenium',
            'sel_browser': 'chrome',
        }

        try:
            search = scrape_with_config(config)
        except GoogleSearchError as e:
            print(e)

        # let's inspect what we got
        for serp in search.serps:
            # print(serp)
            # print(serp.search_engine_name)
            # print(serp.scrape_method)
            # print(serp.page_number)
            # print(serp.requested_at)
            # print(serp.num_results)
            # ... more attributes ...
            for link in serp.links:
                listoflink.append(link)
        for each in listoflink:
            findlinks=re.findall('\w+\.\w+\.\w+',str(each))
            domain.append(findlinks)
        flat_list = [item for sublist in domain for item in sublist]
        sum_of_set = set(flat_list)
        con_value = config.get('keyword')
        single_word = "".join(con_value.split())
        data  = "www."+str(single_word)+".com"        
        if data in sum_of_set:
            site_url = Request('http://'+data,headers={'User-Agent': 'Mozilla/5.0'})
            read_site_url = urlopen(site_url).read()
            soup = BeautifulSoup(read_site_url,'lxml')
            iter = soup.find_all("div",{"class":"collapse navbar-collapse navbar-ex1-collapse"})        
            for each in iter:
                find_a = each.find_all("a")
                for each in find_a:
                    menu_bar_links_level1 = each.get("href")
                    menubar_links.append(menu_bar_links_level1)
                    for each in menubar_links:
                        if each =="/" or each ==" ":
                            pass
                        else: 
                            site_url = Request('http://'+data+each,headers={'User-Agent': 'Mozilla/5.0'})
                            read_site_url = urlopen(site_url).read()
                            soup = BeautifulSoup(read_site_url,'lxml')
                            iter = soup.find_all("ul",{"class":"dropdown-menu"})
                            for each in iter:
                                find_a = each.find_all("a")
                                for each in find_a:
                                    menu_bar_links_level2 = each.get("href")
                                    dropdown_links.append(menu_bar_links_level2)
                                    
                                    sumof_menubar_links = menubar_links + dropdown_links
                                    print(set(sumof_menubar_links))          
                   
x = Scrap()
x.ScrapLinksFromBrowser()
# x.ScrapLinkWithUrllib()   