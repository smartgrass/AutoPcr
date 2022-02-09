## 公主连结自动化任务 

git: https://github.com/smartgrass/AutoPcr

b站: https://www.bilibili.com/video/BV14a411q7uA


<img src="https://github.com/smartgrass/AutoPcr/blob/main/png/Top.png" width= "500"/>

# 更新-GUI版本(仅限Windows系统) 

<img src="https://github.com/smartgrass/AutoPcr/blob/main/png/GUIWindow.png" width= "500"/>

需要配好雷电模拟器路径

新增库 -> SetupPip.cmd

# 更新-一键开启版本(仅限Windows系统) 

用管理员模式打开AutoPcr_py/Start.cmd 就可以了自动启动模拟器,开app自动刷任务

然后,为了更加偷懒,可以给start.cmd创建快捷方式

属性->快捷方式->高级-> √ 用管理员身份运行

<img src="https://github.com/smartgrass/AutoPcr/blob/main/png/QuickStart.png" width= "500"/>

### 配置

要给两个cmd文件配上路径,改成自己的AutoPcr目录 和 雷电模拟器的目录

Start.cmd :

<img src="https://github.com/smartgrass/AutoPcr/blob/main/png/cmd0.png"  width= "500"/>

StartPy.cmd:

<img src="https://github.com/smartgrass/AutoPcr/blob/main/png/cmd1.png" width= "500"/>


# 更新-春黑连点版本
从评论区知道了春黑加连点能自动1刀,试了下可以,就用了

春黑版本文件是 AutoPcr_ChunHei.py

新增库 -> SetupPip.cmd

然后是新增一个快捷键'm'给连点用

<img src="https://github.com/smartgrass/AutoPcr/blob/main/png/NewKey1.png"/>

都配好后就可以用了

其次是按Esc可以中断程序

# 提示:

1.本源码供学习用，禁止用于商业相关

2.使用时不能有中文路径

3.推荐用雷电, mumu用不了(据说是管理员权限的问题)


# 运行需求:

py版本需要python环境, 没用过python的还是不推荐去用了

exe版本就直接用吧

## 1.py核心库:

 aircv 做图像识别;
 
 pyautogui库做按钮键盘事件;
 
 PIL库做屏幕截图;
 
 keyboard 做键盘事件检测
 
安装命令:
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple opencv-python

pip install -i https://pypi.tuna.tsinghua.edu.cn/simple aircv

pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pyautogui

pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pillow

pip install -i https://pypi.tuna.tsinghua.edu.cn/simple keyboard

pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pypiwin32


### (或者管理员模式运行 "SetupPip.cmd" 安装)

## 2.分辨率和按键设置

编辑器分辨率保持和截图一样 这对识别率很重要;

设置完分辨率后建议固定窗口大小

(模拟器大小900x506-dpi180-固定大小)

<img src="https://github.com/smartgrass/AutoPcr/blob/main/AutoPcr_py/%E6%A8%A1%E6%8B%9F%E5%99%A8%E5%A4%A7%E5%B0%8F900x506-dpi180-%E5%9B%BA%E5%AE%9A%E5%A4%A7%E5%B0%8F.png"  width= "800"/>


按键配置

E 是 窗口边缘,退出用的

p 是 开始挑战按钮

N 是结算时下一步的按钮

1-5是编组 6是我的队伍

Num1-3(数字键盘) 是对应队伍1-3

<img src="https://github.com/smartgrass/AutoPcr/blob/main/AutoPcr_py/%E6%A8%A1%E6%8B%9F%E5%99%A8%E9%94%AE%E4%BD%8D%E8%AE%BE%E7%BD%AE.png" width= "800"/>


## 3.地下城配队

清小怪是5组1队

boss是5组2队 ; 5组3队是boss补刀备用队 
