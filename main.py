from subwaymod import *

subway = Subway()       # subway 인스턴스 생성

scrap(subway)

print('---써브쉐이 지역별 매장 수---')        # 써브웨이 지역별 매장 수를 보여줌
subway.sort()
print('----------------------------\n')

ask = input('지역별 매장정보를 조회하시려면 1을, 끝내시려면 아무거나 입력해주세요: ')     # 써브웨이 매장 조회
if ask == '1':
    subway.search_add1()