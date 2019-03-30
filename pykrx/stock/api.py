import pykrx.stock.market as market
import pykrx.stock.index as index
from pykrx.stock.market import *
from pykrx.stock.index import *
from pykrx.stock.short import *


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
    # df = get_market_price_change_by_ticker("20190225", "20190228")
    # df = get_market_fundamental_by_ticker("20190225")
    # df = get_index_kospi_ohlcv_by_date("20180225", "20190228", "코스피 200")
    df = get_index_kospi_by_group("20190228")
    print(df.head())

