from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import datetime

#[CODE 1]
def pascucci_store(result):
    for page in range(1,10):
        pascucci_url = 'https://www.caffe-pascucci.co.kr/store/storeList.asp?page=%d' %page
        print(pascucci_url)
        html = urllib.request.urlopen(pascucci_url)
        soupPascucci = BeautifulSoup(html, 'html.parser')
        tag_tbody = soupPascucci.find('tbody')
        print(tag_tbody)
        for store in tag_tbody.find_all('tr'):
            if len(store) <= 3:
                break
            store_td = store.find_all('td')
            store_name = store_td[1].string
            store_area = store_td[2].string

            store_address = store.find('p', class_='addr').string
            store_phone = store.find('span', class_='tel').string
            result.append([store_name]+[store_area]+[store_address]
                          +[store_phone])
    return

#[CODE 0]
def main():
    result = []
    print('MegaCoffee store crawling >>>>>>>>>>>>>>>>>>>>>>>>>>')
    pascucci_store(result)   #[CODE 1] 호출 
    pascucci_tbl = pd.DataFrame(result, columns=('store', 'area', 'address','phone'))
    pascucci_tbl.to_csv('pascucci.csv', encoding='cp949', mode='w', index=True)
    del result[:]
       
if __name__ == '__main__':
     main()
