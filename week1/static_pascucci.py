from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import datetime


def pascucci_store(result):
    for page in range(1, 10):
        # 파스쿠찌 url을 입력하되 페이지가 바뀌게끔 반복문으로 처리한다.
        pascucci_url = 'https://www.caffe-pascucci.co.kr/store/storeList.asp?page=%d' % page
        print(pascucci_url)
        html = urllib.request.urlopen(pascucci_url)

        # BeuatifulSoup을 사용하여 html 정보를 가져온다.
        soupPascucci = BeautifulSoup(html, 'html.parser')

        # 우리가 가져오고 싶은 정보는 tbody의 tr태그 중 하나이다.
        tag_tbody = soupPascucci.find('tbody')
        for store in tag_tbody.find_all('tr'):
            if len(store) <= 3:
                break
            store_td = store.find_all('td')
            store_name = store_td[1].string
            store_area = store_td[2].string

            # 주소와 가게번호는 td태그 안에 또 다른 태그로 감싸져 있기 때문에 태그와 클래스 명을 활용하여 가져온다.
            store_address = store.find('p', class_='addr').string
            store_phone = store.find('span', class_='tel').string
            result.append([store_name]+[store_area]+[store_address]
                          + [store_phone])
    return


def main():
    result = []
    print('MegaCoffee store crawling >>>>>>>>>>>>>>>>>>>>>>>>>>')
    pascucci_store(result)  # [CODE 1] 호출
    pascucci_tbl = pd.DataFrame(result, columns=(
        'store', 'area', 'address', 'phone'))
    pascucci_tbl.to_csv('staticPascucci.csv',
                        encoding='cp949', mode='w', index=True)
    del result[:]


if __name__ == '__main__':
    main()
