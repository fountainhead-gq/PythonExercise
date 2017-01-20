# 利用高德地图api查询城市交通


### 用法

```
usage: webapi.py [-h] [-k KEYWORD] {site,traffic} ...

城市信息查询.

optional arguments:
  -h, --help                       show this help message and exit
  -k KEYWORD, --keyword KEYWORD    关键词

操作命令:
  {site,traffic}
   site               查询地点信息
   traffic            查询公交信息
```



### 查询城市地点信息

```
usage: webapi.py site [-h] keyword [city]

查询城市地点信息

positional arguments:
  keyword     查询的关键词
  city        查询城市（缺省为ip所在城市）
```

```
python webapi.py site 如家
```

输出结果

![rujia](http://7xq50z.com1.z0.glb.clouddn.com/rujia.jpg)



### 查询交通信息

```
usage: webapi.py traffic [-h] start end [city]

查询公交信息

positional arguments:
  start       出发地
  end         目的地
  city        查询城市
```

```
python webapi.py traffic 北土城 望京
```

![traffic](http://7xq50z.com1.z0.glb.clouddn.com/traffic.jpg)
