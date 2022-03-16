from math import fabs
from operator import truediv
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
hightMatch = 0.93
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

def WaitToClickImg(targetImg,isClick = True,isShip = True,maxTry = 7,autoExit = False,match = minMatch):
	#isClick:找到图片后是否点击
	#isShip:查找失败后是否跳过
	#maxTry:查找失败重新尝试次数
	target_ImgPath = GetFullPath(targetImg)
	Screen_ImgPath = image_X()
	print(target_ImgPath)
	imsrc = ac.imread(Screen_ImgPath) # 原始图像
	imsch = ac.imread(target_ImgPath) # 带查找的部分
	match_result = ac.find_template(imsrc, imsch, match)
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
			if((waitTime > maxTry)&isShip == False):
				time.sleep(1)
			return WaitToClickImg(targetImg,isClick,isShip,maxTry,autoExit)
		else:
			print("Ship >> ",targetImg)
			return False


def IsHasImgHight(targetImg,match = minMatch):
	target_ImgPath = targetImg
	Screen_ImgPath = image_X()
	# print(target_ImgPath)
	imsrc = ac.imread(Screen_ImgPath) # 原始图像
	imsch = ac.imread(target_ImgPath) # 带查找的部分
	match_result = ac.find_template(imsrc, imsch, match)
	if match_result != None:
		return True
	else:
		return False

imgIndex = 0

#屏幕截图,并返回保存路径
def image_X():
	global curDir
	global imgIndex
	img = ImageGrab.grab()

	if(imgIndex ==0 ):
		imgIndex =1
		sp = os.path.join(curDir,"temp.png")
	else:
		imgIndex =0
		sp = os.path.join(curDir,"temp2.png")
	img.save( sp)
	return sp

#点到消失为止
def ClickUntilNul(path):
	WaitToClickImg(path)
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
	# print(_key)
	time.sleep(0.006)
	pyautogui.press(_key)

global loopKey
def LoopKeyDown():
	time.sleep(0.01)
	while(True):
		# if(waitToEnd==False):
		# if(isRun):
		FastKeyDown(loopKey)

def StartLoopKeyDown(key):
	global loopKey
	loopKey = key
	t1.start()

def StopLoopKeyDown():
	stop_thread(t1)

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



#按下Esc 停止
def CheckEnd(_key):

	while(True):
		keyboard.wait(_key)
		# print('CheckEnd')
		# if(isRun):
		# 	isRun = False
		# 	print('pause')
		# else:
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


roleNameDic = {}
zhous = []
zhouDes =[] #描述

def SetRoleNameDic(line):
	nameId =0
	for name in line[1:-2].split(','):
		roleNameDic[name]=nameId
		nameId=nameId+1
		# for r in roleNameDic:
	# 	print(roleNameDic[r])

def ReadZhou():
	tf = open(GetFullPath("other/shengqian.txt"),"rt",encoding='utf-8')
	i = 0
	rName = ''
	for line in tf:
		if(i==0):
			SetRoleNameDic(line)
		else:
			rName=line.replace('\n', '')
			if(rName!='end'):
				splitStrs = rName.split(',')
				zhous.append(splitStrs[0])
				des = ''
				if(len(splitStrs)>1):
					des = '->'+splitStrs[1]
				zhouDes.append(des)

		i= i+1
		# print(i,line)
	# for line in tf.readlines()：

autoKey = 'a'
def AutoSwitch():
	WaitToClickImg('other/Auto.png')
	IsHasImg('other/Auto.png')
	# DoKeyDown(autoKey)

def StartZhou():
	#检查入场png
	bossStartPath =	GetFullPath('other/bossStart.png') #1倍速
	# sleepTime = 1.5 #2
	# bossStartPath =GetFullPath('other/bossStart2.png') #2倍速足够细
	sleepTime = 1.5


	WaitToClickImg(bossStartPath,False,False,30)
	print('bossStart')
	global loopKey
	roleIndex = 0
	zhouCount = len(zhous)
	print('next->',zhous[0])
	StartLoopKeyDown(roleKeys[roleNameDic[zhous[0]]])
	roleIndex = 1
	waitToAuto = False
	global waitToEnd
	waitTime = 0
	while(roleIndex<zhouCount):
			if(IsHasImgHight(bossStartPath)==False):
				if(waitToEnd ==False):
					# if(zhous[roleIndex] !='Auto'):
					print('next->',zhous[roleIndex],zhouDes[roleIndex])
					loopKey = roleKeys[roleNameDic[zhous[roleIndex]]]
					waitToEnd = True
					roleIndex=roleIndex+1
					time.sleep(0.1)
						# StopLoopKeyDown()
				else:
					waitTime = waitTime+1
					print('waitTime',waitTime)
					time.sleep(0.02)
			else:
				if(waitToEnd):
					waitToEnd = False
					waitTime =0
					time.sleep(0.1)
					print('awake')
				time.sleep(0.1)
	#end
	AutoSwitch()

# isRun = True
def RunAutoPcr():
	#按下Esc键停止
	global t0
	global t1
	global t2
	global waitToEnd
	waitToEnd = False
	t0 = threading.Thread(target=CheckEnd,args=(endKey,))
	t0.start()
	# t2 = threading.Thread(target=CheckPause,args=())
	# t2.start()
	t1 = threading.Thread(target=LoopKeyDown,args=())
	# time.sleep(0.5)

	ReadZhou()
	time.sleep(1)
	print('开始检查进场')
	StartZhou()
	os._exit(0)

if __name__ == '__main__':
	RunAutoPcr()