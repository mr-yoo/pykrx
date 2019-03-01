import pykrx.stock.norm.wrap as norm
import pykrx.stock.index.wrap as index
from pykrx.stock.norm.ticker import *


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


def get_ticker(date=None):
    return StockTicker().get(date)


def get_delist(fromdate, todate):
    return StockTicker().get_delist(fromdate=fromdate, todate=todate)


def get_ohlcv_by_date(fromdate, todate, ticker, freq='d'):
    """
    :param fromdate: 조회 시작 일자 (YYYYMMDD)
    :param todate  : 조회 종료 일자 (YYYYMMDD)
    :param ticker  : 조회할 종목의 티커
    :param freq    : d - 일 / m - 월 / y - 년
    :return:
    """
    isin = StockTicker().get_isin(ticker)
    df = norm.get_ohlcv_by_date(fromdate, todate, isin)
    return _resample_ohlcv(df, freq)


def get_price_change_by_ticker(fromdate, todate):
    return norm.get_price_change_by_ticker(fromdate, todate, "ALL")


def get_fundamental_by_ticker(date):
    return norm.get_fundamental_by_ticker(date, "ALL")


def get_kospi_index_ohlcv_by_date(fromdate, todate, freq='d'):
    """
    :param fromdate: 조회 시작 일자 (YYYYMMDD)
    :param todate  : 조회 종료 일자 (YYYYMMDD)
    :param freq    : d - 일 / m - 월 / y - 년
    :return:
    """
    # 001 : 코스피 지수
    df = index.get_ohlcv_by_date(fromdate, todate, "001")
    return _resample_ohlcv(df, freq)


if __name__ == "__main__":
    # df = get_ohlcv_by_date("20190225", "20190228", "000660")
    # df = get_price_change_by_ticker("20190225", "20190228")
    # df = get_fundamental_by_ticker("20190225")
    df = get_kospi_index_ohlcv_by_date("20180225", "20190228")
    print(df.head())

