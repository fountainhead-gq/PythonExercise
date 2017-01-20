# -*- coding: utf-8 -*-

from datetime import datetime
import re
import sys
from color import Colored


class CheckDate(object):
    INVALID_DATE = '日期格式无效.'
    OUT_OF_DATE = '输入日期不再查询范围内'

    def exit_after_echo(self, msg):
        colored = Colored()
        print(colored.red(msg))
        sys.exit(1)

    def valid_date(self, date):
        date = self._parse_date(date)

        if not date:
            self.exit_after_echo(self.INVALID_DATE)

        try:
            date = datetime.strptime(date, '%Y%m%d')
        except ValueError:
            self.exit_after_echo(self.INVALID_DATE)

        # 查询最大日期
        offset = date - datetime.today()
        if offset.days not in range(-1, 58):
            self.exit_after_echo(self.OUT_OF_DATE)

        return datetime.strftime(date, '%Y-%m-%d')

    @staticmethod
    def _parse_date(date):
        result = ''.join(re.findall('\d', date))
        l = len(result)

        # eg 6-1, 6.26, 0626...
        if l in (2, 3, 4):
            year = str(datetime.today().year)
            return year + result

        # eg 201661, 2016-6-26, 20160626...
        if l in (6, 7, 8):
            return result
        return ''