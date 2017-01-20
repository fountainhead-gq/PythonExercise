**微信聊天机器人**  
参考其他的项目学习聊天机器人

## 1. 环境与依赖
- 运行环境Python 3.5
- 需要所依赖的库:
```python
pip install requests
pip install pyqrcode
pip install pypng
pip install hug
pip install chatterbot
```


## 2. 使用
使用不用的方法调用接口

### 运行`test`
- 直接运行代码 `python test.py`,微信扫描二维码登录网页微信。

### 运行图灵API
- 先在[图灵机器人官网](http://www.tuling123.com/)注册账号， [图灵APIKey申请地址](http://www.tuling123.com/member/robot/index.jhtml)
- `bot.py` 文件所在目录下新建 `conf.ini` 文件，内容为:申请的APIkey
```
[main]
key=a4446dc9522d44d4b39b0a6cca9ad24a
```
- 运行`python bot.py`


### 运行`ChatterBot`

运行：`hug -f bot_api.py` 、`python wechat_bot.py`，扫码登录。



## 3. 说明
`wxBot` 继承`WXBot`类并实现 `handle_msg_all` 或者 `schedule` 函数，然后实例化子类并调用 `run` 方法。

- `handle_msg_all` 函数的参数 `msg` 是代表一条消息的字典。字段的内容为：

|字段定义      |内容
|---------    |--------------------
|msg_type_id  |整数，消息类型，具体解释可以查看 消息类型表
|msg_id	      |字符串，消息id
|content      |字典，消息内容，具体含有的字段请参考 消息类型表 ，一般含有 type(数据类型)与 data(数据内容)字段，type 与 data的对应关系可以参考 数据类型表
|user	      |字典，消息来源，字典包含 name(发送者名称,如果是群则为群名称，如果为微信号，有备注则为备注名，否则为微信号或者群昵称)字段与 id(发送者id)字段，都是字符串

- 消息类型

|类型号	 |消息类型	   |content
|--------  |--------     |-------
|0	|初始化消息，内部数据	|无意义，可以忽略
|1	|自己发送的消息	|无意义，可以忽略
|2	|文件消息	|字典，包含 type 与 data 字段
|3	|群消息	 |字典， 包含 user (字典，包含 id 与 name字段，都是字符串，表示发送此消息的群用户)与 type 、 data 字段，红包消息只有 type 字段， 文本消息还有detail、desc字段， 参考 群文本消息
|4	|联系人消息	|字典，包含 type 与 data 字段
|5	|公众号消息	|字典，包含 type 与 data 字段
|6	|特殊账号消息	|字典，包含 type 与 data 字段


- 数据类型

|type	|数据类型	|data
|-----  |-------    |-------
|0	|文本	|字符串，表示文本消息的具体内容
|1	|地理位置	|字符串，表示地理位置
|3	|图片	|字符串，图片数据的url，HTTP POST请求此url可以得到jpg文件格式的数据
|4	|语音	|字符串，语音数据的url，HTTP POST请求此url可以得到mp3文件格式的数据
|5	|名片	|字典，包含 nickname (昵称)， alias (别名)，province (省份)，city (城市)， gender (性别)字段
|6	|动画	|字符串， 动画url, HTTP POST请求此url可以得到gif文件格式的数据
|7	|分享	|字典，包含 type (类型)，title (标题)，desc (描述)，url (链接)，from (源网站)字段
|8	|视频	|不可用
|9	|视频电话	|不可用
|10	|撤回消息	|不可用
|11	|空内容	|空字符串



## 4.参考

### 参考代码
- [wxbot](https://github.com/liuwons/wxBot/tree/master)
- [wechat_bot](https://github.com/wwj718/wechat_bot)

### 参考资料
- [挖掘微信Web版通信的全过程](http://www.tanhao.me/talk/1466.html/)

- [微信协议简单](http://www.blogjava.net/yongboy/archive/2015/11/05/410636.html)

- [qwx: WeChat Qt frontend](https://github.com/xiangzhai/qwx)

## 5. 其他
