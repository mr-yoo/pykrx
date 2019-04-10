from pykrx.comm import dataframe_empty_handler
from pykrx.stock.index.core import (MKD20011, MKD20011_KOSPI, MKD20011_PDF)
from datetime import datetime
import numpy as np


def _get_kospi_ticker_dict():
    """KOSPI index ticker
    """
    date = datetime.now().strftime("%Y%m%d")
    try:
        return _get_kospi_ticker_dict.ticker
    except AttributeError:
        df = MKD20011().read(date)
        _get_kospi_ticker_dict.ticker = df.set_index('idx_nm')[
            'idx_ind_cd'].to_dict()
        return _get_kospi_ticker_dict.ticker


def _get_kospi_ticker_to_id(ticker):
    return _get_kospi_ticker_dict()[ticker]


def get_index_kospi_ticker_list():
    return list(_get_kospi_ticker_dict().keys())


@dataframe_empty_handler
def get_index_kospi_ohlcv_by_date(fromdate, todate, ticker):
    """
    :param fromdate: 조회 시작 일자 (YYYYMMDD)
    :param todate  : 조회 종료 일자 (YYYYMMDD)
    :param ticker  : 코스피/코스피 벤치마크/코스피 200/코스피 100/
                      코스피 50/코스피 대형주/코스피 중형주/코스피 소형주
                      - 종합지수 - 코스피          (001)
                      - 종합지수 - 코스피 벤치마크 (100)
                      - 대표지수 - 코스피 200      (028)
                      - 대표지수 - 코스피 100      (034)
                      - 대표지수 - 코스피 50       (035)
                      - 규모별   - 코스피 대형주   (002)
                      - 규모별   - 코스피 중형주   (003)
                      - 규모별   - 코스피 소형주   (004)
                      - 생 략
    :return        : Kospi Index의 OHLCV DataFrame
                         시가         고가         저가         종가     거래량
        날짜
        20190125  2147.919922  2178.010010  2146.639893  2177.729980  410002000
        20190128  2184.409912  2188.149902  2169.169922  2177.300049  371619000
        20190129  2172.830078  2183.360107  2162.530029  2183.360107  552587000
        20190130  2183.489990  2206.199951  2177.879883  2206.199951  480390000
        20190131  2222.879883  2222.879883  2201.219971  2204.850098  545248000
    """
    index = _get_kospi_ticker_to_id(ticker)
    df = MKD20011_KOSPI().read(fromdate, todate, index)
    df = df[['trd_dd', 'opnprc_idx', 'hgprc_idx', 'lwprc_idx',
             'clsprc_idx', 'acc_trdvol']]
    df.columns = ['날짜', '시가', '고가', '저가', '종가', '거래량']        
    df = df.replace(',', '', regex=True)
    df = df.replace('', '0', regex=True)
    df = df.replace('/', '', regex=True)
    df = df.set_index('날짜')
    df = df.astype({'시가': np.float32, '고가': np.float32,
                    '저가': np.float32, '종가': np.float32,
                    '거래량': np.int64})
    df['거래량'] = df['거래량'] * 1000
    return df


@dataframe_empty_handler
def get_index_kospi_by_group(date):
    """시장지수
    :param date: 조회 일자 (YYYYMMDD)
    :return    : 시장 지수 DataFrame
                                   기준시점    발표시점 기준지수 현재지수    시가총액
        코스피                   1983.01.04  1980.01.04   100.0   2486.35  1617634318
        코스피 벤치마크          2015.09.14  2010.01.04  1696.0   2506.92  1554948117
        코스피 비중제한 8% 지수  2017.12.18  2015.01.02  1000.0   1272.93  1559869409
        코스피 200               1994.06.15  1990.01.03   100.0    327.13  1407647304
        코스피 100               2000.03.02  2000.01.04  1000.0   2489.34  1277592989
        코스피 50                2000.03.02  2000.01.04  1000.0   2205.53  1102490712
    """
    df = MKD20011().read(date)

    df = df[['idx_nm', 'annc_tm', 'bas_tm', 'bas_idx', 'prsnt_prc',
             'idx_mktcap']]
    df.columns = ['지수명', '기준시점', '발표시점', '기준지수', '현재지수',
                  '시가총액']
    df = df.set_index('지수명')
    df = df.replace(',', '', regex=True)
    df = df.replace('', 0)
    df = df.astype({"기준지수": float, "현재지수": float, "시가총액": int}, )
    return df


@dataframe_empty_handler
def get_index_portfolio_deposit_file(date, ticker):
    index = _get_kospi_ticker_to_id(ticker)    
    df = MKD20011_PDF().read(date, index)
    return df['isu_cd'].to_list()


if __name__ == "__main__":    
    import pandas as pd
    pd.set_option('display.expand_frame_repr', False)
    # df = get_index_kospi_ohlcv_by_date("19900101", "19900301", "코스피")
    df = get_index_portfolio_deposit_file("20190410", "코스피 소형주")
    df = get_index_portfolio_deposit_file("20190410", "코스피 200")
    print(df)