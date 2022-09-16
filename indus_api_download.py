# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import json
import pandas as pd
import requests # http 요청 모듈
from urllib.parse import urlencode # URL encoding
import os 

os.chdir(r'D:\업무\220605 비식별화')


# 업종별 에너지소비량 마이크로 데이터 서비스
end_point = 'http://apis.data.go.kr/B553530/GHG_CONSUM_02'
function = '/GHG_CONSUM_02_LIST' # 상세기능명
api_key = 'XXXXX' # 공공데이터 포털에서 받은 서비스키 입력
service_key = '?ServiceKey='+ api_key 


# 상세기능명 정보, 아래의 function 부분의 숫자를 서비스에 맞게 수정해야 함
# ex 업종별 CO2 배출량 현황 마이크로 데이터 서비스 -> function = '/GHG_LIST_04_03_VIEW' # 상세기능명
# 1. 에너지-온실가스 조사대상 업체현항 마이크로 데이터 서비스
# 2. 업종별 에너지 소비량 마이크로 데이터 서비스
# 3. 업종별 CO2 배출량 현황 마이크로 데이터 서비스
# 4. 온실가스 배출량 환산계수 서비스
# 5. 분석보고서 결과분석통계 현황 서비스

# 한국에너지공단_에너지사용 및 온실가스배출량 통계-마이크로데이터
end_point = 'http://apis.data.go.kr/B553530/GHG_LIST_04'
function = '/GHG_LIST_04_03_VIEW' # 상세기능명
key_encoding = 'XXXXX'
service_key = '?ServiceKey='+ key_encoding 

# 필수사항
# 서비스키 ServiceKey
# 페이지번호 pageNo
# 검색건수 numOfRows

# 선택사항
# 항목명_국문 항목명_영문
# 데이터유형 apiType
# 대상연도 q1
# 광역지역명 q2
# 사업장 종사자규모명 q3
# 표준산업분류코드 q4
# 에너지원구분명 q5
# 에너지원명 q6


page_no = 0
records = []

try:
    while(True):
        print('.', end='')    
        page_no += 1
        parameters = {
            'pageNo':page_no,
            'numOfRows':100,    # numOfRows는 100개가 최대
            'apiType' : 'json',
            'q1' : '2018', # 연도
            # 'q2' : '제주', # 지역
            # 'q3' : '5인 미만', # 종사자수
            # 'q4' : '20121', # 표준산업분류코드
            # 'q5' : '석유류', # 에너지원구분명
            # 'q6' : '나프타(납사)', # 에너지원명
            }
        url = end_point + function + service_key + '&' + urlencode(parameters)
        
        # if page_no >3:
        #     break

        res = requests.get(url) # get 방식으로 페이지 요청
        json_dict = json.loads(res.text) # 문자열 형태의 json 결과를 dict 형태로 변환
        records += json_dict['opentable']['field']

except (KeyError, json.decoder.JSONDecodeError): # 더이상 수집이 불가한 경우에 KeyError 발생
    if page_no != 1:
        print('데이터 수집 완료')

result = pd.DataFrame.from_records(records)
result.to_excel('result_배출량_2018.xlsx')

# rename_cols = {
#     'WRKPLC_FANM': '사업장가명', 
#     'ENGY_CNSM_QNTY_YN':'에너지소비량 구분', 
#     'DATA_REG_DT':'자료 등록 일시', 
#     'WRKPLC_WRKR_VOL_NM':'사업장 종사자규모명',
#     'ENGSRC_DVSN_NM':'에너지원구분명', 
#     'KSIC_CD':'표준산업분류코드', 
#     'ENGSRC_NM':'에너지원명', 
#     'KSIC_NM':'표준산업분류명',
#     'ENGY_CNSM_QNTY_NIDVAL':'에너지소비량', 
#     'WIDM_LOCL_NM':'광역지역명', 
#     'TRGT_YEAR':'대상연도',
#     }

# result = result.rename(columns=rename_cols)
# result.to_excel('result.xlsx')
