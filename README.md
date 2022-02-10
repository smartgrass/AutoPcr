## 公主连结自动化任务 

git: https://github.com/smartgrass/AutoPcr

b站: https://www.bilibili.com/video/BV14a411q7uA


<img src="https://github.com/smartgrass/AutoPcr/blob/main/png/Top.png" width= "500"/>

# 更新4.0-GUI版本(仅限Windows) 

<img src="https://github.com/smartgrass/AutoPcr/blob/main/png/GUIWindow.png" width= "500"/>

启动文件: AutoPcr4.0_GUI.py (管理员模式: 需要把python.exe的启动改为管理员模式)

需要配好雷电模拟器路径

新增库 ->运行 SetupPip.cmd

# 更新-cmd一键启动版本(仅限Windows) (可跳过)

启动文件 AutoPcr_py/Start.cmd (管理员模式)

然后,为了更加偷懒,可以给start.cmd创建快捷方式

属性->快捷方式->高级-> √ 用管理员身份运行

<img src="https://github.com/smartgrass/AutoPcr/blob/main/png/QuickStart.png" width= "400"/>

### 配置

要给两个cmd文件配上路径,改成自己的AutoPcr目录 和 雷电模拟器的目录

Start.cmd :

<img src="https://github.com/smartgrass/AutoPcr/blob/main/png/cmd0.png"  width= "500"/>

StartPy.cmd:

<img src="https://github.com/smartgrass/AutoPcr/blob/main/png/cmd1.png" width= "500"/>


# 提示:

1.本源码供学习用，禁止用于商业相关

2.使用时不能有中文路径

3.Esc可退出程序


# 运行需求:

py版本需要python环境, 没用过python的还是不推荐去用了

exe版本就直接用吧(没有新版的功能)

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

pip install -i https://pypi.tuna.tsinghua.edu.cn/simple PySimpleGUI


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

'm' 是打地下城用的,放在春黑的位置

<img src="https://github.com/smartgrass/AutoPcr/blob/main/png/NewKey1.png"/>


## 3.地下城配队

清小怪是5组1队

boss是5组2队 ; 5组3队是boss补刀备用队 
