## 公主连结自动化任务

git: https://github.com/smartgrass/AutoPcr

b站: https://www.bilibili.com/video/BV1xT4y1U75y

Exe版本(v6.4): https://share.weiyun.com/otsYmFrk

<img src="https://github.com/smartgrass/AutoPcr/blob/main/png/Top.png" width= "500"/>

# 更新保留配置

config.ini是配置文件, 如果想保留配置, 可以在更新代码后, 把这个文件放回原位

#6.5 6.6  2023/6/28

修复p竞技场进入卡住

按键配置简化

# 6.4 小更新  2023/6/12
活动VHboss

行会点赞

清空体力左移选项:

用于指定清空体力的目标关卡,比如写1则对应倒数第二个关卡

<img src="https://github.com/smartgrass/AutoPcr/blob/main/png/MoveLeft.png" width= "300"/>

# 6.2 小更新  2023/5/7

扫荡弹出经验药处理

自动推图优化, 好感度,升级窗口,boss对话跳过


# 更新6.0 三周年版本 2023/4/15

扫荡地下城

买多次购买经验药

# 更新5.6 可挂后台版本

自动推图, 自动剧情 (说明见 文件夹 运行说明/其他说明)

跳过启动时生日

使用win32gui代替鼠标点击, 运行时可挂后台,但不能最小化

如果小号启动失败 ,则需要检查模拟器名称是否为"雷电模拟器-1"

运行配置见'运行说明'文件夹


# 提示:

1.本源码供学习用，禁止用于商业相关

2.使用时不能有中文路径

3.Esc可退出程序

### 运行失败原因

1.没有安装python, 不会安装Python可以选择上面的Exe版本

2.没安装第三方库 解决: 管理员模式运行SetupPip.cmd

3.文件夹有中文路径

4.GUI版模拟器启动不了?  解决: 模拟器路径改完 需要点击保存路径

5.没有使用管理员模式运行 解决:将python.exe设置为管理员方式启动:

-属性->兼容性->更改所有用户设置->√管理员身份运行

-建议模拟器启动也设为管理员模拟式启动


# 运行需求:
Windows
python环境, 没用过python的还是不推荐去用了


## 1.py核心库:

 aircv 做图像识别;

 win32gui库获取模拟器截屏, 并做按钮键盘事件;

 PIL库做截图保存;

管理员模式运行 "SetupPip.cmd" 安装

