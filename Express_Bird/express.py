# -*- coding: utf-8 -*-

import requests
import hashlib
import base64
import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from color import Colored


class ExpressBird(object):
    # user id
    APP_ID = "1266669"
    API_KEY = "10f4f092-57d0-4189-ba07-cf2b9db85609"

    url = 'http://api.kdniao.cc/Ebusiness/EbusinessOrderHandle.aspx'
    # url = 'http://testapi.kdniao.cc:8081/Ebusiness/EbusinessOrderHandle.aspx'
    headers = {
        "Accept": "application/x-www-form-urlencoded;charset=utf-8",
        "Accept-Encoding": "utf-8",

    }

    def hash_md5(self, args):
        md5 = hashlib.md5()
        md5.update(args.encode('utf-8'))
        encoded = md5.hexdigest()
        base64_str = base64.b64encode(encoded.encode('utf-8'))
        return base64_str

    def get_company(self, logistics_code):
        logistics_number = {
            # 物流单号
            'LogisticCode': logistics_code
        }
        logistics_number = json.dumps(logistics_number, sort_keys=True)
        request_data = logistics_number + self.API_KEY
        request_data = self.hash_md5(request_data)
        # 必填参数
        logistics_data = {
            # json格式请求内容
            'RequestData': logistics_number,
            # APP ID
            'EBusinessID': self.APP_ID,
            # 指令类型，默认2002
            'RequestType': '2002',
            # 数据内容签名
            'DataSign': request_data.decode(),
            # 数据类型
            'DataType': '2'
        }
        logistics_data= urlencode(logistics_data).encode('utf-8')
        req = Request(self.url, logistics_data, self.headers)
        get_data = (urlopen(req).read().decode('utf-8'))
        #r = requests.post(self.url, data=logistics_data, headers=self.headers)
        #express_data = json.loads(r.text)
        express_data = json.loads(get_data)
        return express_data

    def get_express(self, logistics_code, company_code):
        logistics_number = {
            # 物流单号
            'LogisticCode': logistics_code,
            # 快递公司编号
            'ShipperCode': company_code
        }
        logistics_number = json.dumps(logistics_number, sort_keys=True)
        request_data = logistics_number + self.API_KEY
        request_data = self.hash_md5(request_data)

        # 必填参数
        logistics_data = {
            # json格式请求内容
            'RequestData': logistics_number,
            # APP ID
            'EBusinessID': self.APP_ID,
            # 指令类型，默认1002
            'RequestType': '1002',
            # 数据内容签名
            'DataSign': request_data.decode(),
            # 数据类型
            'DataType': '2'
        }
        #r = requests.get(self.url, verify=False, params=logistics_data, headers=self.headers)
        #express_data = json.loads(r.text)
        logistics_data= urlencode(logistics_data).encode('utf-8')
        req = Request(self.url, logistics_data, self.headers)
        get_data = (urlopen(req).read().decode('utf-8'))
        express_data = json.loads(get_data)
        return express_data

    def search_express(self, logistics_code):
        colored = Colored()
        get_company = self.get_company(logistics_code)
        print('\n')
        if get_company['Success'] == False:
            print(colored.red('快递单号有误或签名验证失败'))
            return
        if not any(get_company['Shippers']):
            print('未查到该快递单号,请检查输入单号信息是否有误！')
        get_express = self.get_express(logistics_code, get_company['Shippers'][0]['ShipperCode'])
        if get_express['Success'] == True:
            if get_express['State'] == '2':
                express_state = colored.yellow('在途中')
            elif get_express['State'] == '3':
                express_state = colored.green('已签收')
            elif get_express['State'] == '4':
                express_state = colored.red('问题件')
            else:
                express_state = colored.magenta('状态不详')
            output_data = '{}的运单号『{}』的状态为：{}\n'.format(colored.cyan(get_company['Shippers'][0]['ShipperName']),
                                                     colored.yellow(logistics_code),  express_state)
            print(output_data)
            if get_express['Traces']:
                for item in get_express['Traces']:
                    print(' 『 {}  {} 』\n '.format(item['AcceptTime'], item['AcceptStation']))



if __name__ == '__main__':
    express_code = input("请输入快递单号: ").strip()
    express_bird = ExpressBird()
    express_bird.search_express(express_code)




















