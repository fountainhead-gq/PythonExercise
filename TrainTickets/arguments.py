# -*- coding: utf-8 -*-

from docopt import docopt
import requests
import re
from requests.packages.urllib3.exceptions import InsecureRequestWarning


class Arguments(object):
    def get_arguments(self):
        arguments = docopt(__doc__)
        # 获取车站信息的url
        url = "https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.8955"
        # requests.packages.urllib3.disable_warnings()
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
        }

        r = requests.get(url, verify=False, headers=headers)
        re_words = re.compile(u"([\u4e00-\u9fa5]+)\|([A-Z]+)")  # 校验中文
        re_words = re.findall(re_words, r.text)
        char_station = dict(re_words)
        char_stations = dict(zip(char_station.keys(), char_station.values()))

        alpha_station = re.findall(r'([A-Z]+)\|([a-z]+)', r.text)
        alpha_station = dict(alpha_station)
        alpha_station = dict(zip(alpha_station.values(), alpha_station.keys()))

        from_stations = ''
        if alpha_station.get(arguments['<from>']):  # 提取全拼
            from_stations = alpha_station.get(arguments['<from>'])
        elif char_stations.get(arguments['<from>']):  # 提取中文
            from_stations = char_stations.get(arguments['<from>'])

        to_stations = ''
        if alpha_station.get(arguments['<to>']):
            to_stations = alpha_station.get(arguments['<to>'])
        elif char_stations.get(arguments['<to>']):
            to_stations = char_stations.get(arguments['<to>'])

        from_station = from_stations
        to_station = to_stations
        date = arguments['<date>']
        return [from_station, to_station, date]