# -*- coding:utf-8 -*-

import requests
import re
import json
from prettytable import PrettyTable
from color import Colored


class CityInfo(object):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
    }
    # 高德地图API_KEY
    API_KEY = "ea6874fd0b4030e5617e71e0565cea8d"
    colored = Colored()

    # 获取IP
    def get_ip(self):
        url = "http://www.ip.cn/"
        r = requests.get(url, verify=False, headers=self.headers)
        res = re.search(u'(\d+\.\d+\.\d+\.\d+)', r.text)
        if res:
            return res.group(0)
        return None

    # 获取所在的城市
    def get_city(self, args):
        city = args.city
        get_ip = self.get_ip()
        url ="http://restapi.amap.com/v3/ip?ip={}&output=json&key={}".format(get_ip, self.API_KEY)
        r = requests.get(url, verify=False, headers=self.headers)
        get_city = json.loads(r.text)
        if not city:
            city = get_city['city']
        # print(get_city)
        return city

    def get_place(self, keyword, city):
        url= 'http://restapi.amap.com/v3/place/text?&keywords={}&city={}&output=json&offset=100&page=1&key={}&extensions=all'.format(keyword, city, self.API_KEY)
        r = requests.get(url, verify=False, headers=self.headers)
        res = json.loads(r.text)
        if res:
            return res
        return None

    def city_place(self, args):
        city = self.get_city(args)
        keyword = args.keyword
        res = self.get_place(keyword, city)
        header = [self.colored.cyan('名称'), self.colored.cyan('地址'), self.colored.cyan('电话')]
        pt = PrettyTable()
        pt.field_names = header
        for line in res['pois']:
            row = [line['name'], line['address'], line['tel']]
            pt.add_row(row)
        print(pt)

    def surface_traffic(self, args):
        origin = args.start
        destination = args.end
        city = self.get_city(args)

        origin = self.get_place(origin, city)
        if not origin['pois']:
            print('无法找到起始位置')
            return
        start_point = origin['pois'][0]['location']
        destination = self.get_place(destination, city)
        if not destination['pois']:
            print('无法找到目的位置')
            return
        end_point = destination['pois'][0]['location']

        url = "http://restapi.amap.com/v3/direction/transit/integrated?origin={}&destination={}&city={}&output=json&key={}".format(start_point, end_point, city, self.API_KEY)
        r = requests.get(url, verify=False, headers=self.headers)
        if not r:
            return
        res = json.loads(r.text)
        header = [self.colored.cyan('路线'), self.colored.cyan('换乘车站'), self.colored.cyan('途经站数'),self.colored.cyan('首末班车时刻表'),
                  self.colored.cyan('预计时间'), self.colored.cyan('步行距离'),self.colored.cyan('总距离')]
        pt = PrettyTable()
        pt.field_names = header
        count = 0
        for transit in res['route']['transits']:
            count += 1
            scheme = self.colored.magenta('方案 {}'.format(str(count)))
            walking_distance = self.colored.magenta('{}米'.format(int(transit['walking_distance'])))
            distance = self.colored.magenta('{:0.1f}千米'.format(int(transit['distance'])/1000))

            pt.add_row([scheme, '', '', '', '',  walking_distance, distance])
            lines = []
            for segment in transit.get('segments', []):
                if segment['bus']['buslines']:
                    for bus in segment['bus']['buslines']:
                        start_time = ''
                        end_time = ''
                        first_last_bus = ''
                        if bus['start_time']:
                            start_time = '{}:{}'.format(bus['start_time'][:2],bus['start_time'][2:])
                        if bus['end_time']:
                            end_time = '{}:{}'.format(bus['end_time'][:2], bus['end_time'][2:])
                        if start_time and end_time:
                            first_last_bus = '{}--{}'.format(start_time, end_time)
                        duration = '{:0.1f} 分钟'.format(int(bus['duration']) / 60)
                        station = '{}--{}'.format(bus['departure_stop']['name'], bus['arrival_stop']['name'])
                        name = bus['name']
                        via_num = bus['via_num']
                        via_nums = str(int(via_num) + 1)
                        if int(via_num) >= 9:
                            via_num = self.colored.red(via_nums)
                        else:
                            via_num = self.colored.green(via_nums)
                        lines =[
                            # 推荐路线
                            self.colored.green(name),
                            # 上车站--下车站
                            self.colored.yellow(station),
                            # 途径站数
                            via_num,
                            # self.colored.white(via_num),
                            # 首末班车时间
                            self.colored.white(first_last_bus),
                            # 历时
                            self.colored.cyan(duration),
                            '',
                            ''
                        ]
                    pt.add_row(lines)
        print(pt)



