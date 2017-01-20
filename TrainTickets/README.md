## 12306火车票查询
`ticket`提供基于命令行的火车票信息查询功能。

### 开发环境

python 3.5

### 第三方依赖

- [prettytable](https://code.google.com/archive/p/prettytable/wikis/Tutorial.wiki)  
- [requests](http://docs.python-requests.org/zh_CN/latest/user/quickstart.html)
- [docopt](https://github.com/docopt/docopt)


### 余票和票价查询

```
> python ticket.py beijing shanghai 20160930
> python ticket.py -g 北京 上海 0930  # 指定车次类型
```


#### 不安装的情况

```
# 下载文件ticket.exe，文件目录下直接运行程序
> ticket 北京 上海 2016-10-10
```

### 帮助

```
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
```

### 示例
![ticket](http://7xq50z.com1.z0.glb.clouddn.com/ticket.jpg)


### 提示
查询近60天内的车票信息。