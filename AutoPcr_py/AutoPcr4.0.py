from math import fabs
from pydoc import doc
from sqlite3 import Time
import sys
from tkinter import E
from xmlrpc.client import Boolean
import PySimpleGUI as sg
from configparser import ConfigParser

import ctypes
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

#region 获取当前路径
print("path " ,os.path.dirname(sys.executable))

curDir = os.path.dirname(__file__)
#图片路径拼接
def GetFullPath(pngName):
	global curDir
	return os.path.join(curDir,pngName)

#利用文件是否存在判断是Exe 还是 Py文件
if(os.path.exists(GetFullPath('config.ini')) == False):
	print('Exe Run')
	curDir =os.getcwd()

#endregion

waitTime = 0
minMatch = 0.7 #最低相似度匹配
hightMatch = 0.90
warnMatch = 0.85 #相似度小于此时, 打印黄字
dxcIndex =1
StartBossIndex = 0
isUseChunHei = True #地下城是否使用春黑连点

tMain = threading.Thread()
t0 =threading.Thread()
t1 = threading.Thread()

#region 图片检查&点击事件
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

def WaitToClickImg(targetImg,isClick = True,isShip = True,maxTry = 7,autoExit = False,match = minMatch,isRgb = False,offsetY=0):
	#isClick:找到图片后是否点击
	#isShip:查找失败后是否跳过
	#maxTry:查找失败重新尝试次数
	target_ImgPath = GetFullPath(targetImg)
	Screen_ImgPath = image_X()
	print(target_ImgPath)
	imsrc = ac.imread(Screen_ImgPath) # 原始图像
	imsch = ac.imread(target_ImgPath) # 带查找的部分
	match_result = ac.find_template(imsrc, imsch, match,rgb=isRgb)

	print('match : %s %s'%(targetImg,match_result))
	global waitTime

	if match_result != None:
		# print(match,minMatch,targetImg)
		# if(match > minMatch):
		# 	for	ma in match_result:
		# 		print('confidence ',ma)
		# 	print("Find Highist " ,len(match_result))


		x1, y1 = match_result['result']
		if(match_result['confidence']  < warnMatch):
			print("\033[1;33m %s %s \033[0m"%(targetImg ,match_result['confidence']))
		waitTime = 0

		if(isClick):
			y1 = y1+offsetY
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
			return WaitToClickImg(targetImg,isClick,isShip,maxTry,autoExit,match,isRgb)
		else:
			print("Ship >> ",targetImg)
			return False

#屏幕截图,并返回保存路径
def image_X():
	global curDir
	img = ImageGrab.grab()
	sp = os.path.join(curDir,"temp.png")
	img.save( sp)
	return sp

#点到消失为止
def ClickUntilNul(path):
	WaitToClickImg(path)
	time.sleep(0.5)
	while(IsHasImg(path)):
		IsHasImg(path)

# #点击然后exit消失为止
# def ClickUntilNul2(path,exsitPath):
# 	WaitToClickImg(path)
# 	while(IsHasImg(exsitPath,False) == False):
# 		DoKeyDown(exitKey)
# 		ClickUntilNul2(path,exsitPath)
# 		break

def DoKeyDown(_key):
	pyautogui.press(_key)
	time.sleep(0.6)

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

#快按钮事件
def FastKeyDown(_key):
	print(_key)
	time.sleep(0.03)
	pyautogui.press(_key)

global loopKey
def LoopKeyDown():
	time.sleep(2)
	while(True):
		FastKeyDown(loopKey)

def StartLoopKeyDown(key):
	global loopKey
	loopKey = key
	t1.start()

def StopLoopKeyDown():
	stop_thread(t1)

#endregion

#region 界面跳转
def ToFightPage():
	if(IsHasImg("main/fight2.png")==False):
		if(WaitToClickImg("main/fight.png",True,True,5,True) == False):
			DoKeyDown(exitKey)
			DoKeyDown(exitKey)
			print('re to Fight')
			ToFightPage()
	time.sleep(1)
def ToHomePage():
	if(IsHasImg("main/home2.png")==False):
		if(WaitToClickImg("main/home.png",True,True,5) == False):
			DoKeyDown(exitKey)
			DoKeyDown(exitKey)
			print('re to Fight')
			ToHomePage()
	time.sleep(1)
def ToShopPage():
	WaitToClickImg("shop/shop1.png",True,True,5)
	time.sleep(1)
#endregion

#选择队伍
def SelectParty(x,y):
	time.sleep(1)
	DoKeyDown(partyKey)
	time.sleep(0.4)
	x= x-1
	y= y-1
	DoKeyDown(groupKeys[x])
	DoKeyDown(duiKeys[y])

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
	DoKeyDown(listSelectKeys[0])
	time.sleep(1)
	DoKeyDown(playerKey)
	time.sleep(6)
	print("sleep...")
	WaitToClickImg('jjc/ship.png',isShip= False)
	WaitToClickImg('jjc/ship.png')
	pyautogui.click()
	time.sleep(2)
	LongTimeCheck("dxc/win.png","jjc/lose.png")
	time.sleep(1.5)
	DoKeyDown(nextKey)
	time.sleep(3)
	DoKeyDown(nextKey)

def StartPJJC():
	ToFightPage()
	WaitToClickImg("jjc/pjjc.png")
	# WaitToClickImg("jjc/get.png")
	time.sleep(1)
	DoKeyDown(exitKey)
	WaitToClickImg("jjc/pjjcTop.png",False)
	DoKeyDown(exitKey) #关掉提示框
	DoKeyDown(listSelectKeys[0]) #选择
	time.sleep(1.5)
	DoKeyDown(playerKey)
	time.sleep(0.3)
	DoKeyDown(playerKey)
	time.sleep(0.3)
	DoKeyDown(playerKey)
	time.sleep(0.3)
	DoKeyDown(playerKey)
	print("sleep for 5s...")
	time.sleep(5)
	WaitToClickImg('jjc/ship.png',isShip= False)
	WaitToClickImg('jjc/ship.png')
	pyautogui.click()
	time.sleep(1.5)
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
	DoKeyDown(listSelectKeys[0])
	time.sleep(0.5)
	WaitToClickImg("tansuo/start.png")
	WaitToClickImg("main/sure.png")
	WaitToClickImg("tansuo/return.png")
	time.sleep(0.5)
	DoKeyDown(exitKey)
	print("===exit===")
	DoKeyDown(exitKey)
	#exp
	if(IsHasImg("tansuo/topExp.png",False) == False):
		ToFightPage()
		time.sleep(0.5)
		WaitToClickImg("tansuo/tansuo.png")
		time.sleep(0.5)
		WaitToClickImg("tansuo/exp.png")

	WaitToClickImg("tansuo/topExp.png",False)
	DoKeyDown(listSelectKeys[0])
	time.sleep(0.5)
	WaitToClickImg("tansuo/start.png")
	WaitToClickImg("main/sure.png")
	WaitToClickImg("tansuo/return.png")
	time.sleep(0.5)
	DoKeyDown(exitKey)
	DoKeyDown(exitKey)
	time.sleep(1.5)

def StartTakeAll():
	time.sleep(2)
	ToHomePage()
	WaitToClickImg("task/task.png")
	WaitToClickImg("task/takeAll.png")
	WaitToClickImg("task/close.png")
def TakeGift():
	ToHomePage()
	WaitToClickImg("task/gift.png")
	WaitToClickImg("task/takeAll.png")
	WaitToClickImg("task/sure.png",match=hightMatch)
	ExitSaoDang()
	ToHomePage()
#region 地下城
StartBossIndex = 0


def StartDxc(index =1):
	print("===地下城==")
	dxcIndex = index
	ToFightPage()
	#进入地下城
	EnterDxc()
	if(IsHasImg(dxcDir + "/ex.png",False)):
		print('今天打完了')
		ToHomePage()
		return
	if(isKillBoss==False):
		time.sleep(1)
		if(WaitToClickImg(dxcDir+"/box5.png",False,True,4)):
			WaitToClickImg(dxcDir + "/run.png")
			WaitToClickImg("main/sure.png")
			StartDxc()
			return

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
		if(isKillBoss):
			StartBoss()
#进入地下城界面
def EnterDxc():
	WaitToClickImg("main/dxc.png")
	time.sleep(1.5)
	IsHasImg(dxcDir + "/ex.png")
	time.sleep(1)
	IsHasImg("main/sure.png")
	time.sleep(2)
#地下城第一次战斗
def DxcFristFight():
	WaitToClickImg(dxcDir + "/box1.png")
	time.sleep(1)
	DoKeyDown(playerKey) #进入挑战
	time.sleep(1)
	#选中队伍
	SelectParty(5,1)
	time.sleep(0.4)
	DoKeyDown(playerKey)
	dxcIndex =2

def DxcBoxFight(level):
	dxcIndex = level+1
	#自动取消关闭奖励界面
	if(level == 2):
		ClickUntilNul(dxcDir + "/box2.png")
	elif(level == 3):
		ClickUntilNul(dxcDir + "/box3.png")
	elif(level == 4):
		ClickUntilNul(dxcDir + "/box4.png")

	time.sleep(1)
	DoKeyDown(playerKey)
	time.sleep(1.5)
	DoKeyDown(playerKey)

def DxcBoxFightWait():
	time.sleep(2)
	WaitImgLongTime(dxcDir + "/win.png")
	time.sleep(2)
	DoKeyDown(nextKey) #返回
	time.sleep(3)
	DoKeyDown(exitKey)
	time.sleep(0.5)
	DoKeyDown(exitKey) #跳过宝箱
	time.sleep(0.5)
	DoKeyDown(exitKey)
	time.sleep(0.5)

def StartBoss():
	print('===StartBoss===')
	ClickUntilNul(dxcDir + "/box5.png")
	time.sleep(1)
	DoKeyDown(playerKey)
	global StartBossIndex
	time.sleep(0.4)
	if(StartBossIndex == 0):
		SelectParty(5,2)
		time.sleep(0.4)
	if(StartBossIndex == 1):
		time.sleep(0.4)
	if(StartBossIndex == 2):
		SelectParty(5,3)
		time.sleep(0.4)
	DoKeyDown(playerKey)
	time.sleep(0.4)
	DoKeyDown(playerKey)
	StartBossIndex = StartBossIndex+1
	if(isUseChunHei):
		StartLoopKeyDown(roleKeys[3])
	WaitBossFight()

def WaitBossFight():
	if(LongTimeCheck('dxc/win.png','dxc/lose.png')):
		#win
		print('win')
		StopLoopKeyDown()
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
		StopLoopKeyDown()
		WaitToClickImg('dxc/dxcBack.png')
		time.sleep(2)
		StartBoss()

#endregion

def BuyExp():
	time.sleep(1)
	ToHomePage()
	ToShopPage()
	WaitToClickImg('shop/shopTop.png',False)
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
	WaitToClickImg('main/sure.png')
	time.sleep(0.5)
	WaitToClickImg('main/sure.png')
	ToHomePage()

def NiuDan():
	WaitToClickImg('main/niuDan.png')
	time.sleep(2)
	DoKeyDown(partyKey)
	DoKeyDown(partyKey)

	if(IsHasImg('other/niu1.png')):
		WaitToClickImg('main/sure.png')
	ToHomePage()

def EnterDiaoCha():
	ToFightPage()
	WaitToClickImg('main/diaoCha.png')

def SaoDang(_time =4):
	WaitToClickImg('tansuo/plus.png')
	for i in range(_time):
		pyautogui.click()
	WaitToClickImg('tansuo/start.png')
	WaitToClickImg("main/sure.png")
	WaitToClickImg("main/skip.png")
	time.sleep(0.3)
	pyautogui.click()


def ExitSaoDang():
	time.sleep(0.5)
	DoKeyDown(exitKey)
	time.sleep(0.3)
	DoKeyDown(exitKey)

def Xqb():
	if(WaitToClickImg('tansuo/xqbEnter.png')==False):
		ExitSaoDang()
		WaitToClickImg('tansuo/xqbEnter.png')


	WaitToClickImg('tansuo/xqbTop.png',False)
	DoKeyDown(listSelectKeys[0])


	SaoDang()
	ExitSaoDang()

	DoKeyDown(exitKey)
	DoKeyDown(exitKey)
	WaitToClickImg('tansuo/xqbTop.png',False)

	DoKeyDown(listSelectKeys[1])
	SaoDang()
	ExitSaoDang()


def xinSui():
	if(WaitToClickImg('tansuo/xinSuiEnter.png')==False):
		ExitSaoDang()
		WaitToClickImg('tansuo/xinSuiEnter.png')

	WaitToClickImg('tansuo/xinSuiTop.png',False)
	DoKeyDown(listSelectKeys[0])

	SaoDang()
	ExitSaoDang()

	DoKeyDown(exitKey)
	DoKeyDown(exitKey)
	WaitToClickImg('tansuo/xinSuiTop.png',False)

	DoKeyDown(listSelectKeys[1])
	SaoDang()
	ExitSaoDang()


def SendZb():
	ToHomePage()
	WaitToClickImg('other/hanghui.png')
	WaitToClickImg('other/hhDown.png',True,True,4)
	time.sleep(0.2)
	for i in range(2):
		if(WaitToClickImg('other/sendBtn.png',True,match=0.93,isRgb=True)):
			WaitToClickImg('other/sendMax.png',True,True,7,False,0.85)
			WaitToClickImg('main/sure.png')
			time.sleep(0.2)
			DoKeyDown(exitKey)
			DoKeyDown(exitKey)

def  Click():
	pyautogui.click()

def GetZBPath(name):
	return os.path.join('other\\zuanbei\\',str(name)+'.png')

def needSeedZb():
	print('need Send ')
	ToHomePage()
	WaitToClickImg('other/hanghui.png')
	time.sleep(0.8)
	WaitToClickImg('other/needSend.png')
	Click()
	if(WaitToClickImg('other/needSend2.png',False)==False):
		print("上次捐赠确认->退出重试")
		DoKeyDown(groupKeys[0])
		time.sleep(0.5)
		WaitToClickImg('other/needSend.png')

	if(WaitToClickImg(GetZBPath(needZbName),False,maxTry = 4) == False):
		print("找不到装备->反转排序")
		DoKeyDown(partyKey)
	if(WaitToClickImg(GetZBPath(needZbName),maxTry = 4)):
		WaitToClickImg('other/needSend2.png')
		WaitToClickImg('main/sure.png')
		WaitToClickImg('main/sure.png')
	else:
		DoKeyDown(exitKey)
		DoKeyDown(exitKey)

def ghHomeTake():
	WaitToClickImg('main/ghHome.png')
	time.sleep(0.5)
	WaitToClickImg('main/ghHome_take.png')
	DoKeyDown(exitKey)
	WaitToClickImg('task/close.png')
	DoKeyDown(exitKey)

tuichuMaxTry =0

def ClickPlayer():
	if(WaitToClickImg('main/player'+mnqIndex+'.png',offsetY=55)):
		if(WaitToClickImg('tansuo/start2.png',match=hightMatch,isRgb=True,isClick=False,maxTry=3) == False):
			print("没有出现挑战界面->重试")
			tuichuMaxTry = tuichuMaxTry+1
			if(tuichuMaxTry>4):
				tuichuMaxTry =0
				return
			ClickPlayer()
		else:
			tuichuMaxTry =0

def tuichu():
	ClickPlayer()
	if(WaitToClickImg('tansuo/start2.png',match=hightMatch,isRgb=True,isClick=False)):
		DoKeyDown(playerKey)
		DoKeyDown(playerKey)
		DoKeyDown(playerKey)
		LongTimeCheck("main/next.png","main/next.png")
		DoKeyDown(exitKey)
		DoKeyDown(nextKey)
		time.sleep(0.3)
		DoKeyDown(exitKey)
		DoKeyDown(nextKey)
		DoKeyDown(exitKey)
		DoKeyDown(nextKey)
		tuichu()
	else:
		print("end")
	return

def OnHouDongHard():
	print('OnHouDongHard')
	ToFightPage()
	WaitToClickImg('main/dxc.png',False)
	DoKeyDown(huodongKey)
	time.sleep(0.5)
	DoKeyDown(exitKey)
	time.sleep(0.5)
	DoKeyDown(exitKey)
	WaitToClickImg('main/player'+mnqIndex+'.png')
	for	i in range(5):
		if(WaitToClickImg('tansuo/start2.png',match=hightMatch,isRgb=True,maxTry=4,isClick=False)):
			MoveToLeft()
		SaoDang(2)
		DoKeyDown(groupKeys[0])
		DoKeyDown(groupKeys[0])
		DoKeyDown(groupKeys[0])
	DoKeyDown(exitKey)
	ExitSaoDang()

def MoveToLeft():
	DoKeyDown('c')

def UseAllPower():
	print('OnHouDongHard')
	ToFightPage()
	WaitToClickImg('main/zhuXian.png',True)

	if(WaitToClickImg('main/player'+mnqIndex+'.png')==False):
		DoKeyDown(exitKey)
		WaitToClickImg('main/player'+mnqIndex+'.png')
	i = 0
	while(WaitToClickImg('tansuo/start2.png',match=hightMatch,isRgb=True,maxTry=3,isClick=False)):
		MoveToLeft()
		i=i+1
		if(i>4):
			break
	SaoDang(30)
	ExitSaoDang()
	ExitSaoDang()

#日常任务
def DailyTasks():
	if(isExp):
		BuyExp()
	if(isNiuDan):
		NiuDan()
	if(isTansuo):
		StartTanSuo()
	if(isJJC):
		StartJJC()
		StartPJJC()
	if(isDxc):
		StartDxc(0)
	if(isHomeTake):
		ghHomeTake()
		StartTakeAll()

	if(isXQB):
		EnterDiaoCha()
		Xqb()
	if(isXinSui):
		EnterDiaoCha()
		xinSui()
	if(isSend):
		SendZb()
	if(isNeedSeed):
		needSeedZb()
	if(isHouDongHard):
		OnHouDongHard()
	if(isUseAllPower):
		UseAllPower()
		StartTakeAll()
	if(isHomeTake):
		TakeGift()

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
	while(IsHasImg("main/fight.png",False) == False):
		DoKeyDown(exitKey)
		time.sleep(2)
		DoKeyDown(exitKey)
		time.sleep(3)
	while(IsHasImg("main/fight.png",False) == False):
		DoKeyDown(exitKey)
		time.sleep(1)
		DoKeyDown(exitKey)
		time.sleep(1)
	time.sleep(0.5)
	while(IsHasImg("main/fight.png",False) == False):
		time.sleep(0.5)
		DoKeyDown(exitKey)
		time.sleep(0.5)
		DoKeyDown(exitKey)


#按下Esc 停止
def CheckEnd(_key):
	while(True):
		keyboard.wait(_key)
		print(_key)
		os._exit(0)

#1-5是编组位置 6 是队伍
#num1-3 队伍位置
partyKey ='y'
exitKey ='z'
huodongKey='x'
playerKey = 'p'	#p是挑战位置
nextKey = 'l' #n 是下一步
endKey ='Esc'
#roleKey 123
listSelectKeys=['i','j','n']
roleKeys = ['1','2','3','4','5']
groupKeys = ['q','w','e','r','t']
duiKeys =['u','h','b']


StartRunName = "启动模拟器并运行"
RunName = "运行"


#region 读取配置
#其他页面
dxcDropKey ='dxcDrop'
mnqIndexKey ='mnqDrop'
dxcDropValue =["炸脖龙","绿龙"]
mnqIndexDropValue=["1","0"]

cfg = ConfigParser()
configPath = GetFullPath('config.ini')
cfg.read(configPath,encoding='utf-8')
mnqIndex = cfg.get('MainSetting',mnqIndexKey)
MainSettingKey='MainSetting_'+mnqIndex

def GetStrConfig(key):
	return cfg.get(MainSettingKey,key)

def GetBoolConfig(boolKey):
	return Boolean(cfg.get(MainSettingKey,boolKey)=='True')

isRunAndStart = False

StartRunName = "启动模拟器并运行"
RunName = "运行"

isJJCKey ='isJJC'
isTansuoKey ='isTansuo'
isDxcKey = 'isDxc'
isExpKey = 'isExp'
isNiuDanKey ='isNiuDan'
LeiDianDirKey ='LeiDianDir'
isRunAndStartKey ='isRunAndStart'

#newKey
isXQBKey='isXQB'
isXinSuiKey='isXinSui'
isSendKey='isSend'

isNeedSeedKey ='isNeedSeed'
isKillBossKey ='isKillBoss'

isHomeTakeKey='isHomeTake'
isHouDongHardKey='isHouDongHard'
isUseAllPowerKey='isUseAllPower'
needZbNameKey = 'needZbName'

isJJC = GetBoolConfig(isJJCKey)
isTansuo =GetBoolConfig(isTansuoKey)
isDxc = GetBoolConfig(isDxcKey)
isExp = GetBoolConfig(isExpKey)
isNiuDan =GetBoolConfig(isNiuDanKey)
isKillBoss = GetBoolConfig(isKillBossKey)
LeiDianDir = cfg.get('MainSetting',LeiDianDirKey)

isXinSui =GetBoolConfig(isXinSuiKey)
isXQB = GetBoolConfig(isXQBKey)
isSend = GetBoolConfig(isSendKey)
isNeedSeed= GetBoolConfig(isNeedSeedKey)
isRunAndStart = GetBoolConfig(isRunAndStartKey)

isHomeTake= GetBoolConfig(isHomeTakeKey)
isHouDongHard=GetBoolConfig(isHouDongHardKey)
isUseAllPower=GetBoolConfig(isUseAllPowerKey)
needZbName = GetStrConfig(needZbNameKey)


dxcBoss=GetStrConfig(dxcDropKey)
dxcDir = ''
if(dxcBoss =="炸脖龙"):
	dxcBossNum =1
	dxcDir ="dxc"
elif(dxcBoss =="绿龙"):
	dxcBossNum = 2
	dxcDir = "dxc_ex3"

#endregion


def RunAutoPcr():
	#按下Esc键停止
	global t0
	global t1
	t0 = threading.Thread(target=CheckEnd,args=(endKey,))
	t0.start()
	t1 = threading.Thread(target=LoopKeyDown,args=())
	time.sleep(0.5)
	if(isRunAndStart):
		print('Wait Start... 25s ')
		time.sleep(25)
		WaitStart()
	else:
		time.sleep(2)
	print('=== Start ===')
	print('\n=== 按Exc退出程序 ===\n')
#日常
	DailyTasks()
	# tuichu()
	print('=== end ===')
	os._exit(0)

if __name__ == '__main__':
	RunAutoPcr()