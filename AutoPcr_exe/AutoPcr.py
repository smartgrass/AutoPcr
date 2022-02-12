import pyautogui
import time
import os
from ctypes import *
from PIL import ImageGrab
import aircv as ac

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

#按钮事件
def DoKeyDown(_key):
	pyautogui.press(_key)
	time.sleep(0.6)
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
	WaitBossFight()

def WaitBossFight():
	if(LongTimeCheck('dxc/win.png','dxc/lose.png')):
		#win
		print('win')
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
		WaitToClickImg('dxc/dxcBack.png')
		time.sleep(2)
		StartBoss()



#图片路径拼接
def GetImagPath(pngName):
	global curDir
	return os.path.join(curDir,pngName)

#1-5是编组位置 6 是队伍
#num1-3 队伍位置
partyKey ='6'
exitKey ='e'
playerKey = 'p'	#p是挑战位置
nextKey = 'n' #n 是下一步

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
def ClickUntilNul2(path):
	WaitToClickImg(path)
	while(IsHasImg("challengeBtn.png",False) == False):
		DoKeyDown(exitKey)
		ClickUntilNul2(path)
		break


def AutoHuoDong():
	print("===活动===")
	ClickUntilNul2("player.png")
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

if __name__ == '__main__':
	curDir = os.path.dirname(__file__)
	waitTime = 0
	minMatch = 0.64 #最低相似度匹配
	warnMatch = 0.85 #相似度小于此时, 打印黄字
	dxcIndex =1
	StartBossIndex = 0
	print('=== Start ===')
	time.sleep(1)
	# WaitImgLongTime("jjc/jjcTop.png") #用于检测匹配程度,用jjcTop
	# LongTimeCheck("dxc/box3.png","dxc/box4.png")

	# AutoHuoDong()
	# StartBoss()
	# LongTimeCheck("dxc/win.png","jjc/lose.png")

	StartTanSuo()
	StartJJC()
	StartPJJC()
	StartDxc(1)
	StartTakeAll()

	print('=== end ===')
