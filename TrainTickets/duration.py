# -*- coding: utf-8 -*-
from color import Colored


class GetDuration(object):
    def get_duration(self, row):
        # 获取车次运行时间
        # duration = row.get('lishi').replace(':', 'h') + 'm'
        duration = row.get('lishi').replace(':', '小时') + '分钟'
        # take 0 hour , only show minites
        colored = Colored()
        if duration.startswith('00'):
            return colored.green(duration[4:])
        # take <10 hours, show 1 bit
        if duration.startswith('0'):
            return colored.green(duration[1:])
        if duration.startswith('9'):
            return colored.white('列车停运')
        return colored.magenta(duration)
