# AutoPcr 公主连结自动化任务
git : https://github.com/smartgrass/AutoPcr
<img src="https://github.com/smartgrass/AutoPcr/blob/main/png/Top.png"/>
提示:
1.本源码供学习用，禁止用于商业相关
2.使用时不能有中文路径
3.推荐用雷电, mumu用不了


运行需求:

py版本需要python环境, 没用过python的还是不推荐去用了
exe版本就直接用吧

1.py核心库:
 aircv 做图像识别;
 pyautogui库做按钮键盘事件;
 PIL库做屏幕截图;
安装命令:
 pip install aircv
 pip install pyautogui
 pip install pillow


2.分辨率和按键设置
编辑器分辨率保持和截图一样 这对识别率很重要;
设置完分辨率后建议固定窗口大小
(模拟器大小900x506-dpi180-固定大小)
<img src="https://github.com/smartgrass/AutoPcr/blob/main/AutoPcr_py/%E6%A8%A1%E6%8B%9F%E5%99%A8%E5%A4%A7%E5%B0%8F900x506-dpi180-%E5%9B%BA%E5%AE%9A%E5%A4%A7%E5%B0%8F.png"/>


按键配置
E 是 窗口边缘,退出用的
p 是 开始挑战按钮
N 是结算时下一步的按钮
1-5是编组 6是我的队伍
Num1-3(数字键盘) 是对应队伍1-3
<img src="https://github.com/smartgrass/AutoPcr/blob/main/AutoPcr_py/%E6%A8%A1%E6%8B%9F%E5%99%A8%E9%94%AE%E4%BD%8D%E8%AE%BE%E7%BD%AE.png"/>


3.地下城配队

清小怪是5组1队
boss是5组2队 ; 5组3队是boss补刀备用队 