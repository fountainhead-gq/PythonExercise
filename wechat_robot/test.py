#!/usr/bin/env python
# coding: utf-8

from wxbot import *


# handle_msg_all 函数用于处理收到的每条消息，而 schedule 函数可以做一些任务性的事情(例如不断向好友推送信息或者一些定时任务)。
class MyWXBot(WXBot):
    def handle_msg_all(self, msg):
        if msg['msg_type_id'] == 4 and msg['content']['type'] == 0:
            self.send_msg_by_uid('hi', msg['user']['id'])

    def schedule(self):
        self.send_msg('tb', 'schedule')
        time.sleep(1)


def main():
    bot = MyWXBot()
    bot.DEBUG = True
    bot.conf['qr'] = 'png'
    bot.run()


if __name__ == '__main__':
    main()