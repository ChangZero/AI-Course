from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import urllib.request
import pandas as pd
import datetime
import time


def pascucci_store(result):
    pascucci_URL = "https://www.caffe-pascucci.co.kr/store/storeList.asp"
    wd = webdriver.Chrome()
    wd.get(pascucci_URL)
    time.sleep(2)

    # 스크롤 내리기
    wd.execute_script(
        "window.scrollTo(0,500)")
    time.sleep(2)

    # 도시 찾는 버튼 클릭
    city_btn = wd.find_element_by_xpath(
        '//*[@id="searchFrm"]/div/dl/dd[1]/div[1]')
    city_btn.click()
    time.sleep(1)

    # 도시(서울) 선택
    city_label = wd.find_element_by_xpath(
        '//*[@id="searchFrm"]/div/dl/dd[1]/div[1]/div[3]/div/ul/li[2]')
    city_label.click()
    time.sleep(1)

    # 주차가능 여부 선택
    parking_btn = wd.find_element_by_xpath(
        '//*[@id="searchFrm"]/div/dl/dd[2]/div/span[3]/a')
    parking_btn.click()
    time.sleep(1)

    # 흡연실 여부 선택
    smoking_btn = wd.find_element_by_xpath(
        '//*[@id="searchFrm"]/div/dl/dd[2]/div/span[2]/a')
    smoking_btn.click()
    time.sleep(1)

    # 스크롤 내리기
    wd.execute_script(
        "window.scrollTo(0,1000)")
    time.sleep(1)

    html = wd.page_source
    soupPascucci = BeautifulSoup(html, 'html.parser')
    tag_tbody = soupPascucci.find('tbody')
    print(tag_tbody)
    for store in tag_tbody.find_all('tr'):
        i = 1
        print("======{}=======".format(i))
        if len(store) <= 3:
            break

        print(store)
        store_name = store.find('td', class_='storeName').string
        store_area = store.find('td', class_='storeArea').string
        store_address = store.find('p', class_='addr').string
        store_phone = store.find('span', class_='tel').string
        result.append([store_name]+[store_area]+[store_address]
                      + [store_phone])
    return


def main():
    result = []
    print('pascucci store crawling >>>>>>>>>>>>>>>>>>>>>>>>>>')
    pascucci_store(result)

    pascucci_tbl = pd.DataFrame(result, columns=(
        'store', 'area', 'address', 'phone'))
    pascucci_tbl.to_csv('dynamicPascucci.csv',
                        encoding='cp949', mode='w', index=True)


if __name__ == '__main__':
    main()
