# -*- coding: utf-8 -*-

"""
Usage:
    ticket [-gdtkz] <from> <to> <date>

Options:
    -h,--help   显示帮助菜单
    -g          高铁
    -d          动车
    -t          特快
    -k          快速
    -z          直达

Example:
    ticket beijing shanghai 2016-10-01
"""


from docopt import docopt
import re
import requests
from prettytable import PrettyTable
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from collections import OrderedDict
from color import Colored
from checkdate import CheckDate
from traintype import TrainType
from duration import GetDuration


class TrainCollection(object):

    def __init__(self, rows, train_type):
        self.rows = rows
        self.train_type = train_type

    def _build_params(self, row):
        # 票价请求参数, 返回有序字典,字典添加顺序和采点时参数顺序必须一致,要不然请求会失败
        checkdate = CheckDate()
        arguments = docopt(__doc__)
        date = arguments['<date>']
        d = OrderedDict()
        d['train_no'] = row.get('train_no')
        d['from_station_no'] = row.get('from_station_no')
        d['to_station_no'] = row.get('to_station_no')
        d['seat_types'] = row.get('seat_types')
        d['train_date'] = checkdate.valid_date(date)
        return d

    def _get_price(self, row):
        # 获取每列车不同席别的票价,返回一个列表
        PRICE_QUERY_URL = 'https://kyfw.12306.cn/otn/leftTicket/queryTicketPrice'  # 票价查询
        params = self._build_params(row)
        r = requests.get(PRICE_QUERY_URL, params=params, verify=False)
        rows = {}
        try:
            rows = r.json()['data']  # 得到json查询结果
        except KeyError:
            rows = {}
        except TypeError:
            pass
        except ValueError:
            rows = {}
        return rows

    def replace_and_append(self, s, c='', a='元'):
        colored = Colored()
        try:
            result = ''
            if s:
                result = re.sub('^.', c, s)
                result = result + a
            return colored.cyan(result)
        except TypeError:
            pass
        except:
            pass

    def replace_color(self, s):
        colored = Colored()
        if s.isdigit():
            return colored.green(str(s)+'张')
        else:
            return colored.white(s)

    @property
    def trains(self):
        colored = Colored()
        duration_time = GetDuration()
        for row in self.rows:
            if (self.train_type.__len__() > 0 and row['station_train_code'][0:1].lower() not in self.train_type):
                continue
            train = [
                # 车次
                colored.magenta(row['station_train_code']),
                # 车站
                ''.join([colored.red(row['from_station_name']), '-->', colored.green(row['to_station_name'])]),
                # 时间
                ''.join([colored.yellow(row['start_time']), '--', colored.yellow(row['arrive_time'])]),
                # 历时
                duration_time.get_duration(row),
                # 商务
                colored.green(row['swz_num']),
                # 特等
                self.replace_color(row['tz_num']),
                # 一等座
                self.replace_color(row['zy_num']),
                # 二等座
                self.replace_color(row['ze_num']),
                # 高级软卧
                self.replace_color(row['gr_num']),
                # 软卧
                self.replace_color(row['rw_num']),
                # 硬卧
                self.replace_color(row['yw_num']),
                # 软座
                self.replace_color(row['rz_num']),
                # 硬座
                self.replace_color(row['yz_num']),
                # 无座
                self.replace_color(row['wz_num']),
                # 其他
                self.replace_color(row['qt_num'])
            ]

            # 获取票价数据
            price_dict = self._get_price(row)
            try:
                ot_str = self.replace_and_append('\n'.join(price_dict.get('OT', '')))
            except TypeError:
                ot_str = ''
            price = [  # 票价列表
                ''.join([colored.cyan('票价'), '\n']),
                '',
                '',
                '',
                #  商务
                self.replace_and_append(price_dict.get('A9', '')),
                #  特等
                self.replace_and_append(price_dict.get('P', '')),
                #  一等
                self.replace_and_append(price_dict.get('M', '')),
                # 二等
                self.replace_and_append(price_dict.get('O', '')),
                # 高级软卧
                self.replace_and_append(price_dict.get('A6', '')),
                # 软卧
                self.replace_and_append(price_dict.get('A4', '')),
                # 硬卧
                self.replace_and_append(price_dict.get('A3', '')),
                # 软座
                self.replace_and_append(price_dict.get('A2', '')),
                # 硬座
                self.replace_and_append(price_dict.get('A1')),
                # 无座
                self.replace_and_append(price_dict.get('WZ', '')),
                # 其他
                ot_str
            ]
            data_list = [train, price]
            yield data_list  # 返回车票信息和票价信息
            #yield train

    def pretty_print(self):
        colored = Colored()

        # header = 'train station time duration first second softsleep hardsleep hardsit'.split()
        # header = ['train', 'station', 'time', 'duration', 'first', 'second', 'softsleep','hardsleep', 'hardsit']
        header = [colored.cyan('车次'), colored.cyan('车站'), colored.cyan('时间'), colored.cyan('历时'), colored.cyan('商务座'),
                  colored.cyan('特等座'), colored.cyan('一等座'), colored.cyan('二等座'), colored.cyan('高级软卧'), colored.cyan('软卧'),
                  colored.cyan('硬卧'), colored.cyan('软座'), colored.cyan('硬座'), colored.cyan('无座'), colored.cyan('其他')]
        pt = PrettyTable()
        pt._set_field_names(header)  # 设置每一列的标题
        for train in self.trains:
            pt.add_row(train[0])
            pt.add_row(train[1])
        print(pt)


def TrainTicketsQuery():
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

    check_date = CheckDate()
    date = check_date.valid_date(date)

    train_type = TrainType()
    train_type_list = train_type.getTrainType(arguments)

    # 构建URL
    url = 'https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT&queryDate={}&from_station={}&to_station={}'\
        .format(date, from_station, to_station)
    r = requests.get(url, verify=False)
    rows = r.json()['data']['datas']
    trains = TrainCollection(rows, train_type_list)
    trains.pretty_print()

if __name__ == "__main__":
    TrainTicketsQuery()