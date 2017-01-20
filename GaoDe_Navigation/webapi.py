# -*- coding: utf-8 -*-

import argparse
from amap import CityInfo


def main():
    get_info = CityInfo()
    site = get_info.city_place
    traffic = get_info.surface_traffic
    parser = argparse.ArgumentParser(description='城市交通信息查询')
    subparsers = parser.add_subparsers(title='操作命令')

    parser.add_argument('-k', '--keyword', type=str, help='关键词')

    place_cmd = subparsers.add_parser('site', help='查询城市地点信息', description='查询城市地点信息')
    place_cmd.add_argument('keyword', help='查询的关键词')
    place_cmd.add_argument('city', nargs='?', help='查询城市')
    place_cmd.set_defaults(func=site)

    bus_cmd = subparsers.add_parser('traffic', help='查询交通信息', description='查询交通信息')
    bus_cmd.add_argument('start', help='出发地')
    bus_cmd.add_argument('end', help='目的地')
    bus_cmd.add_argument('city', nargs='?', help='查询城市')
    bus_cmd.set_defaults(func=traffic)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()