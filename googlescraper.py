from GoogleScraper import scrape_with_config, GoogleSearchError
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import imgkit
import urllib

class Scrap(object):
    def __init__(self):
        self.listoflink = []
        self.flat_list = []
        self.menubar_dropdown__links1=[]
        self.menubar_dropdown__links2=[]
        self.data = None
    def ScrapLinksFromBrowser(self):
    # See in the config.cfg file for possible values
        global config
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
                self.listoflink.append(link)

    def ListOfDomainList(self):
        domain=[]
        # VarForListOfLink = self.ScrapLinksFromBrowser()
        for each in self.listoflink:
            findlinks=re.findall('\w+\.\w+\.\w+',str(each))
            domain.append(findlinks)
        self.flat_list = set([item for sublist in domain for item in sublist])
        return self.flat_list

    def ParseDomailLinksFromScraped(self):        
        sum_of_set = set(self.flat_list)
        con_value = config.get('keyword')
        single_word = "".join(con_value.split())
        self.data  = "www."+str(single_word)+".com"        
        return self.data

    def AllParsedDomainLinksOfMenuBar(self):    
        if self.data in self.flat_list:
            site_url = Request('http://'+self.data,headers={'User-Agent': 'Mozilla/5.0'})
            read_site_url = urlopen(site_url).read()
            soup = BeautifulSoup(read_site_url,'lxml')
            iter = soup.find_all("div",{"class":"collapse navbar-collapse navbar-ex1-collapse"})        
            for each in iter:
                find_a = each.find_all("a")
                for each in find_a:
                    menu_bar_links_level1 = each.get("href")
                    self.menubar_dropdown__links1.append(menu_bar_links_level1)
            return self.menubar_dropdown__links1
        else:
            pass        

    def AllParsedDomainLinksOfDropDown(self):
        # MenubarDropdown  = self.AllParsedDomainLinksOfMenuBar()
        for each in self.menubar_dropdown__links1:
            site_url = Request('http://'+self.data+each,headers={'User-Agent': 'Mozilla/5.0'})
            read_site_url = urlopen(site_url).read()
            soup = BeautifulSoup(read_site_url,'lxml')
            iter = soup.find_all("ul",{"class":"dropdown-menu"})
            if iter:    
                for each in iter:
                    find_a = each.find_all("a")
                    for each in find_a:
                        menu_bar_links_level2 = each.get("href")
                        self.menubar_dropdown__links2.append(menu_bar_links_level2)
                return self.menubar_dropdown__links2                
            else:
                pass

    def ScreenShotsOfAlllinks(self):
        # VarForMenuBar = self.AllParsedDomainLinksOfMenuBar()
        # VarForDomain = self.AllParsedDomainLinksOfDropDown()
        counter = 0                                       
        setof_final_domain_name = list("http://"+self.data+each for each in set(self.menubar_dropdown__links1+self.menubar_dropdown__links2))
        for each in setof_final_domain_name:
            print(each)
            counter = counter+1
            imgkit.from_url(each, str(counter)+'.jpg')                        

if __name__ == "__main__":
    x = Scrap()
    x.ScrapLinksFromBrowser()
    x.ListOfDomainList()
    x.ParseDomailLinksFromScraped()
    x.ScreenShotsOfAlllinks()
    x.AllParsedDomainLinksOfMenuBar()
    x.AllParsedDomainLinksOfDropDown()
    x.ScreenShotsOfAlllinks()
