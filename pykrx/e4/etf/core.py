from pykrx.comm.http import KrxHttp
from pandas import DataFrame


class MKD60005(KrxHttp):
    #
    @property
    def bld(self):
        return "MKD/08/0801/08010500/mkd08010500_02"

    def read(self, fromdate, todate):
        result = self.post(trd_dd=todate, fromdate=fromdate, todate=todate, date=todate, gubun2=2,
                           acsString=0, domforn="01", uly_gubun="02", gubun="00", isu_cd="KR7114820004")
        return result


if __name__ == "__main__":
    import pandas as pd
    pd.set_option('display.width', None)

    df = MKD60005().read("20190211", "20190311")
    print(df)