import pykrx.stock.market as market
import pykrx.stock.index as index
from pykrx.stock.market import get_market_fundamental_by_ticker
from pykrx.stock.index import *
from pykrx.stock.short import *
import calendar


def _resample_ohlcv(df, freq):
    """
    :param df   : KRX OLCV format의 DataFrame
    :param freq : d - 일 / m - 월 / y - 년
    :return:    : resampling된 DataFrame
    """
    if freq != 'd':
        how = {'시가': 'first', '고가': 'max', '저가': 'min', '종가': 'last',
               '거래량': 'sum'}
        if freq == 'm':
            df = df.resample('MS').apply(how)
        elif freq == 'y':
            df = df.resample('YS').apply(how)
        else:
            print("choose a freq parameter in ('m', 'y', 'd')")
            raise RuntimeError
    return df


#def get_business_days(year, month):
#    first_day, last_day = calendar.monthrange(year, month)
#    first_day_in_string = "{}{:02d}{:02d}".format(year, month, first_day)
#    last_day_in_string = "{}{:02d}{:02d}".format(year, month, last_day)
#
#    # HACK: 동화약품 (000020)은 가장 오래된 상장 기업
#    df = get_market_ohlcv_by_date(first_day_in_string, last_day_in_string, "000020")
#    return df.index.tolist()


def get_market_ohlcv_by_date(fromdate, todate, ticker, freq='d'):
    """
    :param fromdate: 조회 시작 일자 (YYYYMMDD)
    :param todate  : 조회 종료 일자 (YYYYMMDD)
    :param ticker  : 조회할 종목의 티커
    :param freq    : d - 일 / m - 월 / y - 년
    :return:
    """
    isin = market.get_stock_ticker_isin(ticker)
    df = market.get_market_ohlcv_by_date(fromdate, todate, isin)
    return _resample_ohlcv(df, freq)


def get_market_price_change_by_ticker(fromdate, todate):
    df_a = market.get_market_price_change_by_ticker(fromdate, todate)    
    # MKD80037는 상장 폐지 종목은 제외한 정보를 전달하기 때문에, 시작일의 가격
    # 정보 중에서 시가를 가져온다.
    # - 시작일이 주말일 경우를 고려해서 가까운 미래의 평일의 날짜를 얻어온다.
    # - 동화약품(000020)은 가장 오래된 상장 회사
    hack = get_market_ohlcv_by_date(fromdate, todate, "000020")
    fromdate = hack.index[0]    
    # - 시작일 하루간의 가격 정보를 얻어온다.
    df_1 = market.get_market_price_change_by_ticker(fromdate, fromdate)
    # - 시작일에는 존재하지만 기간 동안 없는(상폐) 종목을 찾아낸다.
    # - 종가/대비/등락률/거래량/거래대금을 0으로 업데이트한다.    
    cond = ~df_1.index.isin(df_a.index)    
    if len(df_1[cond]) > 1:    
        print(df_1[cond])
        df_1.loc[cond, '종가'    ] = 0
        df_1.loc[cond, '변동폭'  ] = -df_1.loc[cond, '시가']    
        df_1.loc[cond, '등락률'  ] = -100.0
        df_1.loc[cond, '거래량'  ] = 0    
        df_1.loc[cond, '거래대금'] = 0
        # 조회 정보에 상장 폐지 정보를 추가한다.    
        df_a.append(df_1[cond])            
    return df_a


def get_market_fundamental_by_date(fromdate, todate, ticker, freq='d'):
    isin = market.get_stock_ticker_isin(ticker)
    df = market.get_market_fundamental_by_date(fromdate, todate, isin)
    return _resample_ohlcv(df, freq)


def get_index_kospi_ohlcv_by_date(fromdate, todate, ticker, freq='d'):
    """
    :param fromdate: 조회 시작 일자 (YYYYMMDD)
    :param todate  : 조회 종료 일자 (YYYYMMDD)
    :param freq    : d - 일 / m - 월 / y - 년
    :return:
    """
    # 001 : 코스피 지수
    df = index.get_index_kospi_ohlcv_by_date(fromdate, todate, ticker)
    return _resample_ohlcv(df, freq)


if __name__ == "__main__":
    # df = get_market_ohlcv_by_date("20190225", "20190228", "000660")
    # df = get_market_price_change_by_ticker("20190225", "20190231")
    # df = get_market_fundamental_by_ticker("19960103")
    # df = get_market_fundamental_by_date('20190322', '20190329', '035420')
    # df = get_index_kospi_ohlcv_by_date("20180225", "20190228", "코스피 200")
    # df = get_index_kospi_by_group("20190228")
    # df = get_market_ohlcv_by_date("20150720", "20150810", "000020")
    df = get_market_price_change_by_ticker("20150620", "20150810")
    print(df.head(2))
