# subwaymod 모듈
import requests
from bs4 import BeautifulSoup
import re
import operator

class Subway:
    def __init__(self):
        self.stores = []        # 모든 매장 정보를 담을 리스트
        self.all_address = {}   # 모든 매장 주소를 담을 딕셔너리

    def put_store(self, a):
        # a는 ['339', '부산반여점', '부산광역시 해운대구 선수촌로 78', '아침메뉴\n딜리버리', '051-783-6384', ''] 구조로 되어있음

        # 주소를 일관성있게 바꿔주는 코드
        pattern_seoul = re.compile(r'^서울[^ ]?\b')
        pattern_jeju = re.compile(r'^제주[^ ]?\b')
        pattern_daegu = re.compile(r'^대구[^ ]?\b')
        pattern_daejeon = re.compile(r'^대전광역시유성구')
        pattern_junggu = re.compile(r'중구중림로')
        pattern_suwon = re.compile(r'^수원시')

        if pattern_seoul.search(a[2]):      # 서울을 서울특별시로 바꿔줌
            change = pattern_seoul.search(a[2]).group()
            a[2] = a[2].replace(change, '서울특별시')

        if pattern_jeju.search(a[2]):      # 제주도를 제주특별자치도로 바꿔줌
            change = pattern_jeju.search(a[2]).group()
            a[2] = a[2].replace(change, '제주특별자치도')

        if pattern_daegu.search(a[2]):      # 대구시를 대구광역시로 바꿔줌
            change = pattern_daegu.search(a[2]).group()
            a[2] = a[2].replace(change, '대구광역시')

        if pattern_daejeon.search(a[2]):      # 대전광역시유성구를 대전광역시 유성구로 바꿔줌
            change = pattern_daejeon.search(a[2]).group()
            a[2] = a[2].replace(change, '대전광역시 유성구')

        if pattern_junggu.search(a[2]):      # 중구중림로를 중구 중림로로 바꿔줌
            change = pattern_junggu.search(a[2]).group()
            a[2] = a[2].replace(change, '중구 중림로')

        if pattern_suwon.search(a[2]):      # 수원시를 경기도 수원시로 바꿔줌
            change = pattern_suwon.search(a[2]).group()
            a[2] = a[2].replace(change, '경기도 수원시')

        address_list = a[2].split()     # 주소 문자열을 split하여 리스트로 변환
        if address_list[0] in self.all_address.keys():      # all_address 안에 주소 정보를 넣어준다(key는 도/시, value는 시/군/구)
            self.all_address[address_list[0]].add(address_list[1])
        else:
            self.all_address[address_list[0]] = {address_list[1]}

        store_dict = {'name': a[1], 'address': a[2], 'add1': address_list[0], 'add2': address_list[1], 'tel': a[4]}

        self.stores.append(store_dict)      # 각 매장 정보를 stores 리스트 안에 딕셔너리로 저장한다

    def search_add1(self):      # 시/도 정보를 입력받아서 조회해주는 함수
        while 1:
            print('\n--------시/도--------')      # 시/도 목록 프린팅

            for a in self.all_address.keys():
                print(a)
            print('전체매장\n--------------------\n')

            add1_input = input('시/도를 입력하세요: ')      # 시/도 정보 입력받음

            count = 0

            if add1_input == '전체매장':        # 전체매장 조회
                for a in self.stores:
                    print('[', a['name'], ']', '\n주소: ', a['address'], '\t전화번호: ', a['tel'], '\n')
                    count += 1
                print('전국 총', count, '개 매장이 있습니다.')

            elif add1_input in self.all_address.keys():     # 시/도 정보 입력받으면 search_add2함수 실행
                self.search_add2(add1_input)

            else:
                print('잘못 입력하셨습니다.')        # 잘못 입력했을 경우 처음으로 돌아감

            again = input('다시 조회하시려면 1을, 끝내시려면 아무거나 입력해주세요: ')
            if again != '1':
                break
            print()

    def search_add2(self, add1_input):
        print('\n------시/군/구------')

        for a in self.all_address[add1_input]:  # 시/군/구 목록 프린팅
            print(a)
        print('전체매장\n--------------------\n')

        while 1:
            add2_input = input('시/군/구를 입력하세요: ')        # 시/군/구 정보 입력받음

            count = 0

            if add2_input == '전체매장':        # 전체매장 조회
                for a in self.stores:
                    if a['add1'] == add1_input:
                        print('[', a['name'], ']', '\n주소: ', a['address'], '\t전화번호: ', a['tel'], '\n')
                        count += 1
                print(add1_input, '총', count, '개 매장이 있습니다.')
                break

            elif add2_input in self.all_address[add1_input]:        # 시/군/구 정보 입력받으면 해당 목록 프린팅
                for a in self.stores:
                    if a['add1'] == add1_input and a['add2'] == add2_input:
                        print('[', a['name'], ']', '\n주소: ', a['address'], '\t전화번호: ', a['tel'], '\n')
                        count += 1
                print(add1_input, add2_input, '총', count, '개 매장이 있습니다.')
                break

            else:
                print('잘못 입력하셨습니다.')        # 잘못 입력했을 경우 처음으로 돌아감(시/구 입력으로)
                break

    def sort(self):     # 써브웨이 지역별 매장 개수를 프린팅하는 함수. 매장이 많은 지역부터 프린팅
        add1_dict = {}       # add1의 개수 정보를 저장할 딕셔너리
        add1_sorted_list = []       # add1의 개수 정보를 정렬해서 저장할 리스트

        for a in self.all_address.keys():
            add1_dict[a] = len(self.all_address[a])     # all_address를 이용해 add1 요소별 개수 세기

        add1_sorted_list = sorted(add1_dict.items(), key=operator.itemgetter(1), reverse=True)      # add1_dict의 value를 내림차순으로 정렬하여 add1_sorted_list에 저장

        for e in add1_sorted_list:
            print(e[0], '\t', e[1], '개')


def scrap(subway):
    for url_num in range(1, 36):  # 전체 페이지 긁어오기(1~35페이지)
        url = 'http://subway.co.kr/storeSearch?page=' + str(url_num)
        result = requests.get(url)
        soup = BeautifulSoup(result.text, 'html.parser')

        store_result = soup.find('div', {'class': 'board_list_wrapper'})

        for li in store_result.find_all('tr'):
            if li.find('td') is None:
                continue

            store_list = []

            for el in li.find_all('td'):
                store_list.append(el.text.strip())

            subway.put_store(store_list)
