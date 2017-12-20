import bs4
import requests
import re
import crypto_db
import time

class CoinMarketScraper():

    def get_website(self,url):
        self.res = requests.get(url)
        return self.res.text

    def init_crawler(self):
        # inits the scrape and starts scrapping for the main part
        r = self.get_website("https://coinmarketcap.com/all/views/all/")
        self.soup = bs4.BeautifulSoup(r,'html.parser')
        self.deals = self.soup.find_all('div',{'class':'container'})
        return self.deals

    def get_price_table(self,deals):
        self.deals = deals
        for deal in self.deals:
            row = deal.find_all('div',{'class','row'})
            for inner_col in row:
                cols = inner_col.find_all('div',{'class':'col-lg-10'})
                for inner_row in cols:
                    i_rows = inner_row.find_all('div',{'class':'row'})
                    for xs_col in i_rows:
                        col_xs = xs_col.find_all('div',{'class':'col-xs-12'})
                        for xs_row in col_xs:
                            tab = xs_row.find_all('div',{'class':'table-responsive compact-name-column'})
                            for cur_wrap in tab:
                                wrapp = cur_wrap.find_all('table',{'class':'table js-summary-table'})
        return wrapp


    def get_data_from_table(self,wrapp):
        self.wrapp = wrapp
        for w in self.wrapp:
            cryptos = w.find_all('tbody')
            for cryp in cryptos:
                cc = cryp.find_all('tr',{'class':""})
        return cc

    def get_current_data(self,price_class):
        count = 0
        self.price_class = price_class
        for data in self.price_class:
            symbol,price_val,percent_data,link = self.get_req_data(data)
            #print(symbol,price_val,percent_data)
            crypto_db.add_crypto(symbol,percent_data[0],percent_data[1],percent_data[2],price_val,link)
            count += 1
            if count == 100:
                break

    def get_crypto_price(self,data):
        self.data = data
        self.p = 0
        nwp = self.data.find_all('td',{'class':'no-wrap text-right'})
        for price_data in nwp:
            self.p = price_data.find_all('a',{'class':'price'})[0].text
            self.l = "https://coinmarketcap.com" + price_data.find_all('a',{'class':'price'})[0]['href']
        return self.p,self.l

    def get_req_data(self,data):
        self.data = data
        percent_1hr,percent_24hr,percent_7d = 0,0,0
        price_val = self.data.find_all('td',{'class':'no-wrap market-cap text-right'})[0]['data-usd']
        symbol = self.data.find_all('td',{'class':'text-left col-symbol'})[0].text
        price,link = self.get_crypto_price(self.data)
        if price_val == '?':
            price_val = 0
        try:
            # regular exp to find percent class. Since CMC generates class names dynamically
            # based on the value of the percent, the class/css is rendered by the JS lib
            #  when the page is loaded. So trying out using the class name doesnt work
            # the regex is basically saying that any text or number after the 'percent-' grab it.
            percent_1hr = self.data.find_all('td',{'class':re.compile("no-wrap percent-1h[A-Za-z0-9]*")})[0].text
            percent_24hr = self.data.find_all('td',{'class':re.compile("no-wrap percent-24h[A-Za-z0-9]*")})[0].text
            percent_7d = self.data.find_all('td',{'class':re.compile("no-wrap percent-7d[A-Za-z0-9]*")})[0].text
            #print("{0} at {1} with {2}/hr increase or decrease".format(symbol,price_val,percent_1hr))
        except:
            # throws some error because of empty lists
            pass
        return symbol,price,(percent_1hr,percent_24hr,percent_7d),link

    def run(self):
        self.layers = self.init_crawler()
        self.price_table = self.get_price_table(self.layers)
        self.all_data = self.get_data_from_table(self.price_table)
        self.get_current_data(self.all_data)
        #return self.curr_data

if __name__ == '__main__':
    cmc = CoinMarketScraper()
    start_time = time.time()
    print(cmc.run())
    print(time.time() - start_time," sec ")
