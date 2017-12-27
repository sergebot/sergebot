

import bs4
import requests
import re


crypto_img_dict = {}

for x in range(1,2):
    r = requests.get("https://coinranking.com/?page={0}".format(x))
    print("Scraping page #",x)
    soup = bs4.BeautifulSoup(r.text,'html.parser')
    body_data = soup.find_all('body',{'class':'frame'})
    for body in body_data:
        frame_row_expand_data = body.find_all('div',{'class':'frame__row frame__row--expand'})
        #print(frame_row_expand_data)
        for frame_row_expand in frame_row_expand_data:
            coin_list_data = frame_row_expand.find_all('div',{'class':'coin-list'})
            #print(coin_list_data)
            for coin_list in coin_list_data:
                coin_list_body_data = coin_list.find_all('div',{'class':'coin-list__body'})
                #print(coin_list_body_data)
                for coin_list_body in coin_list_body_data:
                    coin_list_row_data = coin_list_body.find_all('a',{'class':'coin-list__body__row'})
                    for coin_list_row in coin_list_row_data:
                        wrapper_data = coin_list_row.find_all('div',{'class':'wrapper'})
                        for wrapper in wrapper_data:
                            grid_data = wrapper.find_all('div',{'class':'grid'})
                            for grid in grid_data:
                                grid_col_data = grid.find_all('div',{'class':'grid__col grid__col--3-of-8 grid__col--m-4-of-12 grid__col--s-5-of-10 grid__col--am'})
                                for grid_col in grid_col_data:
                                    grid_body_row_data = grid_col.find_all('div',{'class':'coin-list__body__row__cryptocurrency'})
                                    for grid_body_row in grid_body_row_data:
                                        cryp_name_data = grid_body_row.find_all('div',{'class':'coin-list__body__row__cryptocurrency__name'})
                                        cryp_image_data = grid_body_row.find_all('div',{'class':'coin-list__body__row__cryptocurrency__prepend'})
                                        for cryp_name in cryp_name_data:
                                            crp_name = cryp_name.find_all('span',{'class':'coin-name'})[0].text
                                            #print(crp_name)
                                            for cryp_img in cryp_image_data:
                                                crypto_icon_data = cryp_img.find_all('span',{'class':'coin-list__body__row__cryptocurrency__prepend__icon'})
                                                for crypto_icon in crypto_icon_data:
                                                    try:
                                                        crp_icon = crypto_icon.find_all('img',{'class':'coin-list__body__row__cryptocurrency__prepend__icon__img'})[0]['src']

                                                        crp_sym = crypto_icon.find_all('img',{'class':'coin-list__body__row__cryptocurrency__prepend__icon__img'})[0]['alt']
                                                        crp_sym = re.search(r'\((.*?)\)',crp_sym).group(1)
                                                        crypto_img_dict[crp_sym] = crp_icon
                                                    except:
                                                        pass


print(crypto_img_dict)
