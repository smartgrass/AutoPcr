
import sys
from sysconfig import get_path
from tkinter import E
from tkinter.tix import Tree
from xmlrpc.client import Boolean
import PySimpleGUI as sg
from configparser import ConfigParser

import ctypes
from importlib.resources import path
import inspect
from re import A
import threading
import pyautogui
import time
import os
from ctypes import *
from PIL import ImageGrab
import aircv as ac
import keyboard

#Glabol
print("path " ,os.path.dirname(sys.executable))
# print("path " , os.getcwd())

curDir = os.path.dirname(__file__)
#图片路径拼接
def GetImagPath(pngName):
	global curDir
	return os.path.join(curDir,pngName)

#利用文件是否存在判断是Exe 还是 Py文件
if(os.path.exists(GetImagPath('config.ini')) == False):
	print('Exe Run')
	curDir =os.getcwd()

waitTime = 0
minMatch = 0.7 #最低相似度匹配
warnMatch = 0.85 #相似度小于此时, 打印黄字
dxcIndex =1
StartBossIndex = 0
isUseChunHei = True #地下城是否使用春黑连点

tMain = threading.Thread()
t0 =threading.Thread()
t1 = threading.Thread()


#===========AutoPcr==============

#快速检测图片
def IsHasImg(targetImg,isClick = True,stopTime = 2):
	return WaitToClickImg(targetImg,isClick,True,stopTime)

#等待图片出现,低频率检测
def WaitImgLongTime(targetImg):
	maxTryTime = 30*4  #4分钟 最大等待上限
	longTimer = 0
	while (WaitToClickImg(targetImg,False,True) == False):
		time.sleep(2)
		longTimer = longTimer+1
		if(longTimer > maxTryTime):
			return
#查找图片
#isClick:找到图片后是否点击
#isShip:查找失败后是否跳过
#maxTry:查找失败重新尝试次数
def WaitToClickImg(targetImg,isClick = True,isShip = True,maxTry = 7,autoExit = False):
	target_ImgPath = GetImagPath(targetImg)
	Screen_ImgPath = image_X()
	print(target_ImgPath)
	imsrc = ac.imread(Screen_ImgPath) # 原始图像
	imsch = ac.imread(target_ImgPath) # 带查找的部分
	match_result = ac.find_template(imsrc, imsch, minMatch)
	print('match : %s %s'%(targetImg,match_result))
	global waitTime

	if match_result != None:
		x1, y1 = match_result['result']
		if(match_result['confidence']  < warnMatch):
			print("\033[1;33m %s %s \033[0m"%(targetImg ,match_result['confidence']))
		waitTime = 0

		if(isClick):
			pyautogui.moveTo(x1,y1)
			pyautogui.click()
			time.sleep(0.4)
		return True
	else:
		waitTime = waitTime+1
		print((isShip==False))
		if((isShip==False)|(waitTime < maxTry)):
			time.sleep(0.1)
			if(isShip == False):
				time.sleep(3)
			if(waitTime < maxTry & autoExit):
				DoKeyDown(exitKey)
			return WaitToClickImg(targetImg,isClick,isShip,maxTry,autoExit)
		else:
			print("Ship >> ",targetImg)
			return False

#屏幕截图,并返回保存路径
def image_X():
	global curDir
	img = ImageGrab.grab()
	img.save(curDir + "/temp.png")
	return curDir + "/temp.png"

#Fight界面
def ToFightPage():
	if(IsHasImg("fight2.png")==False):
		WaitToClickImg("fight.png",True,True,5)
	time.sleep(1)
def ToHomePage():
	if(IsHasImg("home2.png")==False):
		WaitToClickImg("home.png",True,True,5)
	time.sleep(1)
def ToShopPage():
	WaitToClickImg("shop/shop1.png",True,True,5)
	time.sleep(1)

#按钮事件
def DoKeyDown(_key):
	pyautogui.press(_key)
	time.sleep(0.6)
#快按钮事件
def FastKeyDown(_key):
	print(_key)
	time.sleep(0.03)
	pyautogui.press(_key)

def LoopKeyDown(_key):
	time.sleep(2)
	while(True):
		FastKeyDown(_key)

#选择队伍
def SelectParty(x,y):
	time.sleep(1)
	DoKeyDown(partyKey)
	time.sleep(0.4)
	DoKeyDown(x)
	DoKeyDown(y)
#点到消失为止
def ClickUntilNul(path):
	WaitToClickImg(path)
	while(IsHasImg(path)):
		IsHasImg(path)


def StartJJC():
	print("===竞技场==")
	ToFightPage()
	WaitToClickImg("jjc/jjc.png")
	# WaitToClickImg("jjc/get.png")
	time.sleep(1)
	DoKeyDown(exitKey)
	WaitToClickImg("jjc/jjcTop.png",False)
	DoKeyDown(exitKey)
	DoKeyDown(exitKey)
	DoKeyDown('num1')
	time.sleep(1)
	DoKeyDown(playerKey)
	time.sleep(12)
	print("sleep...")
	LongTimeCheck("dxc/win.png","jjc/lose.png")
	time.sleep(1.5)
	DoKeyDown(nextKey)
	time.sleep(3)

def StartPJJC():
	ToFightPage()
	WaitToClickImg("jjc/pjjc.png")
	# WaitToClickImg("jjc/get.png")
	time.sleep(1)
	DoKeyDown(exitKey)
	WaitToClickImg("jjc/pjjcTop.png",False)
	DoKeyDown(exitKey) #关掉提示框
	DoKeyDown('num1') #选择
	time.sleep(1.5)
	DoKeyDown(playerKey)
	time.sleep(0.3)
	DoKeyDown(playerKey)
	time.sleep(0.3)
	DoKeyDown(playerKey)
	time.sleep(0.3)
	DoKeyDown(playerKey)
	print("sleep for 30s...")
	time.sleep(30)
	LongTimeCheck("jjc/pjjcEnd.png","jjc/pjjcEnd.png")
	time.sleep(2.5)
	DoKeyDown(nextKey)
	time.sleep(2)

def StartTanSuo():
	print("===探索===")
	ToFightPage()
	time.sleep(0.5)
	WaitToClickImg("tansuo/tansuo.png")
	time.sleep(0.5)
	WaitToClickImg("tansuo/mana.png")
	WaitToClickImg("tansuo/topMana.png",False)
	DoKeyDown('num1')
	time.sleep(0.5)
	WaitToClickImg("tansuo/plus.png")
	WaitToClickImg("tansuo/start.png")
	WaitToClickImg("tansuo/sure.png")
	WaitToClickImg("tansuo/return.png")
	time.sleep(0.5)
	DoKeyDown(exitKey)
	print("===exit===")
	DoKeyDown(exitKey)
	#exp
	ToFightPage()
	time.sleep(0.5)
	WaitToClickImg("tansuo/tansuo.png")
	time.sleep(0.5)
	WaitToClickImg("tansuo/exp.png")
	WaitToClickImg("tansuo/topExp.png",False)
	DoKeyDown('num1')
	time.sleep(0.5)
	WaitToClickImg("tansuo/plus.png")
	WaitToClickImg("tansuo/start.png")
	WaitToClickImg("tansuo/sure.png")
	WaitToClickImg("tansuo/return.png")
	time.sleep(0.5)
	DoKeyDown(exitKey)
	DoKeyDown(exitKey)
	time.sleep(1.5)

def StartTakeAll():
	time.sleep(2.5)
	ToHomePage()
	WaitToClickImg("task/task.png")
	WaitToClickImg("task/takeAll.png")
	WaitToClickImg("task/close.png")
	ToHomePage()


def StartDxc(index =1):
	print("===地下城==")
	dxcIndex = index
	ToFightPage()
	#进入地下城
	EnterDxc()

	if(dxcIndex <= 1):
		DxcFristFight()
		DxcBoxFightWait() 	#1战中
	if(dxcIndex <= 2):
		DxcBoxFight(2)
		DxcBoxFightWait() #2
	if(dxcIndex <= 3):
		DxcBoxFight(3)
		DxcBoxFightWait() #3
	if(dxcIndex <= 4):
		DxcBoxFight(4)
		DxcBoxFightWait()  #4
	if(dxcIndex <= 5):
		#boss
		StartBoss()
#进入地下城界面
def EnterDxc():
	WaitToClickImg("dxc/dxc.png")
	time.sleep(1.5)
	IsHasImg("dxc/ex2.png")
	time.sleep(1)
	IsHasImg("dxc/enter.png")
	time.sleep(2)
#地下城第一次战斗
def DxcFristFight():
	WaitToClickImg("dxc/box1.png")
	time.sleep(1)
	DoKeyDown(playerKey) #进入挑战
	time.sleep(1)
	#选中队伍
	SelectParty('5','num1')
	time.sleep(0.4)
	DoKeyDown(playerKey)
	dxcIndex =2

def DxcBoxFight(level):
	dxcIndex = level+1
	#自动取消关闭奖励界面
	if(level == 2):
		ClickUntilNul("dxc/box2.png")
	elif(level == 3):
		ClickUntilNul("dxc/box3.png")
	elif(level == 4):
		ClickUntilNul("dxc/box4.png")

	time.sleep(1)
	DoKeyDown(playerKey)
	time.sleep(1.5)
	DoKeyDown(playerKey)

def DxcBoxFightWait():
	time.sleep(2)
	WaitImgLongTime("dxc/win.png")
	time.sleep(2)
	DoKeyDown(nextKey) #返回
	time.sleep(3)
	DoKeyDown(exitKey)
	time.sleep(0.5)
	DoKeyDown(exitKey) #跳过宝箱
	time.sleep(0.5)
	DoKeyDown(exitKey)
	time.sleep(0.5)

StartBossIndex = 0

def StartBoss():
	print('===StartBoss===')
	ClickUntilNul("dxc/box5.png")
	time.sleep(1)
	DoKeyDown(playerKey)
	global StartBossIndex
	time.sleep(0.4)
	if(StartBossIndex == 0):
		SelectParty('5','num2')
		time.sleep(0.4)
	if(StartBossIndex == 1):
		time.sleep(0.4)
	if(StartBossIndex == 2):
		SelectParty('5','num3')
		time.sleep(0.4)
	DoKeyDown(playerKey)
	time.sleep(0.4)
	DoKeyDown(playerKey)
	StartBossIndex = StartBossIndex+1
	if(isUseChunHei):
		t1.start()
	WaitBossFight()

def WaitBossFight():
	if(LongTimeCheck('dxc/win.png','dxc/lose.png')):
		#win
		print('win')
		stop_thread(t1)
		time.sleep(2)
		DoKeyDown(nextKey)
		time.sleep(3)
		DoKeyDown(exitKey)
		time.sleep(0.5)
		DoKeyDown(exitKey)
		time.sleep(0.5)
		DoKeyDown(exitKey)
		ToHomePage()
		print('end')
	else:
		#lose
		stop_thread(t1)
		WaitToClickImg('dxc/dxcBack.png')
		time.sleep(2)
		StartBoss()


def BuyExp():
	ToShopPage()
	WaitToClickImg('shop/select1.png')
	if(IsHasImg('shop/exp2.png',False) == False):
		ToHomePage()
		print('no to buy')
		return
	expCounter = 1
	while((expCounter < 4) & (IsHasImg('shop/exp.png'))):
		expCounter = expCounter+1
		print('IsHasImg' ,expCounter)
	WaitToClickImg('shop/buyBtn.png')
	WaitToClickImg('shop/buyTitle.png',False)
	WaitToClickImg('tansuo/sure.png')
	time.sleep(0.5)
	WaitToClickImg('tansuo/sure.png')
	ToHomePage()

def NiuDan():
	WaitToClickImg('niuDan.png')
	time.sleep(1)
	DoKeyDown('6')
	if(IsHasImg('other/niu2.png')):
		ToHomePage()
	else:
		print()

def SendZb():
	print()
	ToHomePage()
	WaitToClickImg('other/hanghui.png')

def LongTimeCheck(im1,im2):
	isWaiting = True
	#True表示识别1图 False表示识别2图
	while(isWaiting):
		if(IsHasImg(im1,False)):
			print('has ',im1)
			return True
		if(IsHasImg(im2,False)):
			print('has ',im2)
			return False
		time.sleep(2)

#点到消失为止
def ClickUntilNul2(path,exsitPath):
	WaitToClickImg(path)
	while(IsHasImg(exsitPath,False) == False):
		DoKeyDown(exitKey)
		ClickUntilNul2(path,exsitPath)
		break


def AutoHuoDong():
	print("===活动===")
	ClickUntilNul2("player.png","challengeBtn.png")
	time.sleep(0.5)
	DoKeyDown(playerKey)
	time.sleep(0.5)
	DoKeyDown(playerKey)
	DoKeyDown(playerKey)
	time.sleep(2)
	WaitImgLongTime("next.png")
	time.sleep(1)
	DoKeyDown(nextKey)
	time.sleep(2)
	DoKeyDown(nextKey)
	DoKeyDown(nextKey)
	AutoHuoDong()

def DailyTasks():
	if(isSend):
		SendZb()
	if(isNiuDan):
		NiuDan()
	if(isExp):
		BuyExp()
	if(isTansuo):
		StartTanSuo()
	if(isJJC):
		StartJJC()
		StartPJJC()
	if(isDxc):
		StartDxc(1)
		StartTakeAll()

def _async_raise(tid, exctype):
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

def stop_thread(thread):
	print("stop ",thread)
	_async_raise(thread.ident, SystemExit)

def WaitStart():
	print('=== WaitStart ===')
	time.sleep(5)
	while(IsHasImg("fight.png",False) == False):
		DoKeyDown(exitKey)
		time.sleep(0.5)
		DoKeyDown(exitKey)
		time.sleep(1)
	while(IsHasImg("fight.png",False) == False):
		DoKeyDown(exitKey)
		time.sleep(0.5)
		DoKeyDown(exitKey)
		time.sleep(1)

#按下Ctrl 停止
def CheckEnd(_key):
	while(True):
		keyboard.wait(_key)
		print(_key)
		os._exit(0)

#1-5是编组位置 6 是队伍
#num1-3 队伍位置
partyKey ='6'
exitKey ='e'
playerKey = 'p'	#p是挑战位置
nextKey = 'n' #n 是下一步
endKey ='Esc'
role3Key = 'm' #春黑是第个三位置

StartRunName = "启动模拟器并运行"
RunName = "运行"



def RunAutoPcr():
	#按下Esc键停止
	global t0
	global t1
	t0 = threading.Thread(target=CheckEnd,args=(endKey,))
	t0.start()
	t1 = threading.Thread(target=LoopKeyDown,args=(role3Key,))
	time.sleep(0.5)
	if(isRunAndStart):
		WaitStart()
	print('=== Start ===')
	# WaitImgLongTime("jjc/jjcTop.png") #用于检测匹配程度,用jjcTop
	# LongTimeCheck("dxc/box3.png","dxc/box4.png")
	# AutoHuoDong()  #打普通关用
	# StartBoss()

#日常
	DailyTasks()
	print('=== end ===')

#======读取配置======
cfg = ConfigParser()
configPath = GetImagPath('config.ini')
cfg.read(configPath)
isRunAndStart = False
isJJC = Boolean(cfg.get('MainSetting','isJJC')=='True')
isTansuo = Boolean(cfg.get('MainSetting','isTansuo')=='True')
isDxc = Boolean(cfg.get('MainSetting','isDxc')=='True')
isExp = Boolean(cfg.get('MainSetting','isExp')=='True')
isSend = Boolean(cfg.get('MainSetting','isSend')=='True')
isNiuDan = Boolean(cfg.get('MainSetting','isNiuDan')=='True')

def SetCurConfig(AllValues):
	global isJJC,isTansuo,isExp,isDxc,isSend,isNiuDan
	isJJC = AllValues[0]
	isTansuo =AllValues[1]
	isDxc=AllValues[2]
	isExp=AllValues[3]
	isSend=AllValues[4]
	isNiuDan = AllValues[5]
#保存配置
def SavaConfig(AllValues):
	cfg.set('MainSetting', 'isJJC', str(AllValues[0]))
	cfg.set('MainSetting', 'isTansuo', str(AllValues[1]))
	cfg.set('MainSetting', 'isDxc', str(AllValues[2]))
	cfg.set('MainSetting', 'isExp', str(AllValues[3]))
	cfg.set('MainSetting', 'isSend', str(AllValues[4]))
	cfg.set('MainSetting', 'isNiuDan', str(AllValues[5]))

	with open(configPath, "w+") as f:
		cfg.write(f)
# isJJC = True
#============GUI================
# sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
# [sg.Text('Enter something on Row 2'), sg.InputText()],
layout = [  [sg.Checkbox('竞技场',isJJC)],[sg.Checkbox('探索',isTansuo)],[sg.Checkbox('地下城',isDxc)],
			[sg.Checkbox('购买经验',isExp)],[sg.Checkbox('送装备',isSend)],[sg.Checkbox('扭蛋',isNiuDan)],
			[sg.Button(StartRunName), sg.Button(RunName),sg.Button('Save'), ] ]

# Create the Window
window = sg.Window('Window Title', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
	event, values = window.read()
	if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
		break
	SetCurConfig(values)
	if event == 'Save':
		SavaConfig(values)
	if ((event == StartRunName) | (event == RunName)):
		isRunAndStart = (event == StartRunName)
		print('Run ', isRunAndStart )
		tMain = threading.Thread(target=RunAutoPcr)
		tMain.start()
	# print('You entered ', values[0])
	print('You entered ', values )
	print('You event ', event )

print("close")
os._exit(0)
window.close()

#============GUIEnd================