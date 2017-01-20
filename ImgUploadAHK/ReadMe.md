## 简介
一个快捷的图片上传实用功能，在windows环境下编辑markdown时，可以 **方便快捷** 地把一张图片上传至图库并生成图片链接的功能。  

## 步骤

- 注册七牛，设置图床  
- 将符合系统版本的AutoHotKey.dll文件保存在Windows/System32文件夹中。*AutoHotkey.dll是用来实现脚本语言对AutoHotkey的调用*
- 测试 uploadImg_ahk.py
- 下载安装AutoHotKey,把执行的脚本添加进HotKeys.ahk文件中（run后的路径为绝对路径）,示例如下：

```
^!c::
Send ^c
Clipwait
Run %Comspec% /c "Python D:\github\ImgUploadAHK\uploadImg_ahk.py %Clipboard%"
Return
```
- 以管理员的身份启动HotKeys.ahk文件


## 使用说明
1. 选中并复制想要上传的图片，`ctrl + c`或右键复制
2. 按下快捷键`ctrl + alt + c`,此操作实现图片上传至图库，并生成图片链接到剪切板。
3. 按下`ctrl + v`，把剪切板的链接（格式: `![名称](url)`）复制到markdown文件。
