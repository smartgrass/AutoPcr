from operator import ne
import sys
from xmlrpc.client import Boolean
import PySimpleGUI as sg
from configparser import ConfigParser
import ctypes
import inspect
from re import A
import threading
import time
import os
from ctypes import *
from PIL import ImageGrab
from PIL import Image
import aircv as ac
import keyboard
import win32gui, win32ui, win32con,win32api
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
nextDxcLevel=1
StartBossIndex = 0

tMain = threading.Thread()
t0 =threading.Thread()
t1 = threading.Thread()

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


#region win32初始化
#获取后台窗口的句柄，注意后台窗口不能最小化
#雷电模拟器 或 雷电模拟器-1 或直接None

window_title = None
MainhWnd =  0
Subhwnd = None
width = 960
height = 540
saveDC = None
mfcDC = None
saveBitMap = None

def winfun(hwnd, lparam):
	global Subhwnd
	subtitle = win32gui.GetWindowText(hwnd)
	if subtitle == 'TheRender':
		Subhwnd = hwnd
		print("Find Subhwnd",Subhwnd)


def WaitWin32Start():
	#如果Main为0则等待
	global window_title,MainhWnd,Subhwnd,saveDC,mfcDC,saveBitMap
	if(mnqIndex == "0"):
		window_title ="雷电模拟器"
	elif(mnqIndex == "1"):
		window_title ="雷电模拟器-1"
	print("当前请求模拟器名称: " + window_title +" (如启动失败则检查多开器中的模拟器名称)" )

	MainhWnd =  win32gui.FindWindow('LDPlayerMainFrame', window_title)
	while(MainhWnd ==0):
		print("等待模拟器启动中...")
		time.sleep(1.5)
		MainhWnd =  win32gui.FindWindow('LDPlayerMainFrame', window_title)

	#已打开雷电
	print("Find MainhWnd",MainhWnd)
	win32gui.EnumChildWindows(MainhWnd, winfun, None)
	while(Subhwnd == None):
		time.sleep(1)
		print("wait subHwnd...")
		win32gui.EnumChildWindows(MainhWnd, winfun, None)

	hWndDC = win32gui.GetWindowDC(Subhwnd)
	#创建设备描述表
	mfcDC = win32ui.CreateDCFromHandle(hWndDC)
	#创建内存设备描述表
	saveDC = mfcDC.CreateCompatibleDC()
	#创建位图对象准备保存图片
	saveBitMap = win32ui.CreateBitmap()
	saveBitMap.CreateCompatibleBitmap(mfcDC,width,height)
	#将截图保存到saveBitMap中
	saveDC.SelectObject(saveBitMap)


def SavaShoot():
	#保存bitmap到内存设备描述表
	global window_title,MainhWnd,Subhwnd,saveDC,mfcDC,saveBitMap
	saveDC.BitBlt((0,0), (width,height), mfcDC, (0, 0), win32con.SRCCOPY)
	bmpinfo = saveBitMap.GetInfo()
	bmpstr = saveBitMap.GetBitmapBits(True)

	im_PIL = Image.frombuffer('RGB',(bmpinfo['bmWidth'],bmpinfo['bmHeight']),bmpstr,'raw','BGRX',0,1)
	im_PIL.save(GetFullPath("temp.png")) #保存
	return GetFullPath("temp.png")
	# im_PIL.show() #显示

key_map = {
    "0": 48, "1": 49, "2": 50, "3": 51, "4": 52, "5": 53, "6": 54, "7": 55, "8": 56, "9": 57,
    'F1': 112, 'F2': 113, 'F3': 114, 'F4': 115, 'F5': 116, 'F6': 117, 'F7': 118, 'F8': 119,
    'F9': 120, 'F10': 121, 'F11': 122, 'F12': 123, 'F13': 124, 'F14': 125, 'F15': 126, 'F16': 127,
    "A": 65, "B": 66, "C": 67, "D": 68, "E": 69, "F": 70, "G": 71, "H": 72, "I": 73, "J": 74,
    "K": 75, "L": 76, "M": 77, "N": 78, "O": 79, "P": 80, "Q": 81, "R": 82, "S": 83, "T": 84,
    "U": 85, "V": 86, "W": 87, "X": 88, "Y": 89, "Z": 90,
    'BACKSPACE': 8, 'TAB': 9, 'TABLE': 9, 'CLEAR': 12,
    'ENTER': 13, 'SHIFT': 16, 'CTRL': 17,
    'CONTROL': 17, 'ALT': 18, 'ALTER': 18, 'PAUSE': 19, 'BREAK': 19, 'CAPSLK': 20, 'CAPSLOCK': 20, 'ESC': 27,
    'SPACE': 32, 'SPACEBAR': 32, 'PGUP': 33, 'PAGEUP': 33, 'PGDN': 34, 'PAGEDOWN': 34, 'END': 35, 'HOME': 36,
    'LEFT': 37, 'UP': 38, 'RIGHT': 39, 'DOWN': 40, 'SELECT': 41, 'PRTSC': 42, 'PRINTSCREEN': 42, 'SYSRQ': 42,
    'SYSTEMREQUEST': 42, 'EXECUTE': 43, 'SNAPSHOT': 44, 'INSERT': 45, 'DELETE': 46, 'HELP': 47, 'WIN': 91,
    'WINDOWS': 91, 'NMLK': 144,
    'NUMLK': 144, 'NUMLOCK': 144, 'SCRLK': 145,
    '[': 219, ']': 221, '+': 107, '-': 109}


def GetWinPos():
	print("")

rect=None
trueH=0
trueW=0
lastX=0
lastY =0
def Click(x=None, y=None):
	try:
		global Subhwnd,lastY,lastX,rect,trueH,trueW
		if(x==None):
			x = lastX
			y = lastY
		else:
			lastX = x
			lastY = y

		if(rect==None):
			rect = win32gui.GetClientRect(Subhwnd)
			trueH = rect[3]
			trueW = rect[2]

		tx = int(x * trueW/960)
		ty = int(y * trueH/540)
		# print(trueH,trueW,"simPos:",x,y,"truePos:",tx,ty)
		positon = win32api.MAKELONG(int(tx), int(ty))
		win32api.SendMessage(Subhwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, positon)
		time.sleep(0.02)
		win32api.SendMessage(Subhwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON,positon)
		time.sleep(0.1)
	except Exception as e:
		print(f"fallback adb click:{e}")

def testKey():
	win32gui.PostMessage(Subhwnd, win32con.WM_KEYDOWN, 90, 0)
	win32gui.PostMessage(Subhwnd, win32con.WM_KEYUP, 90, 0)

#抬起按键

def release_key(key_code):
    win32api.keybd_event(key_code, win32api.MapVirtualKey(key_code, 0), win32con.KEYEVENTF_KEYUP, 0)
#按下按键
def press_key(key_code):
    win32api.keybd_event(key_code, win32api.MapVirtualKey(key_code, 0), 0, 0)
#  按一下按键
def press_and_release_key(key_code):
    press_key(key_code)
    release_key(key_code)

#endregion


#region 图片检查&点击事件
#快速检测图片
def IsHasImg(targetImg,isClick = True,stopTime = 4):
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

def WaitToClickImg(targetImg,isClick = True,isShip = True,maxTry = 12,autoExit = False,match = minMatch,isRgb = False,offsetY=0):
	#isClick:找到图片后是否点击
	#isShip:查找失败后是否跳过
	#maxTry:查找失败重新尝试次数
	target_ImgPath = GetFullPath(targetImg)
	Screen_ImgPath = SavaShoot()
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
			time.sleep(0.1)
			Click(x1,y1)
			time.sleep(0.6)
		return True
	else:
		waitTime = waitTime+1
		print((isShip==False))
		if((isShip==False)|(waitTime < maxTry)):
			time.sleep(0.18)
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

def pressKey(key):
	keyCode =key_map[key]
	win32gui.PostMessage(Subhwnd, win32con.WM_KEYDOWN, keyCode, 0)
	time.sleep(0.05)
	win32gui.PostMessage(Subhwnd, win32con.WM_KEYUP, keyCode, 0)
def DoKeyDown(key):
	pressKey(key)
	time.sleep(0.6)

def LongTimeCheck(im1,im2):
	isWaiting = True
	#True表示识别1图 False表示识别2图
	while(isWaiting):
		time.sleep(2)
		if(IsHasImg(im1,False)):
			print('has ',im1)
			return True
		if(IsHasImg(im2,False)):
			print('has ',im2)
			return False


#快按钮事件
def FastKeyDown(_key):
	print(_key)
	time.sleep(0.03)
	pressKey(_key)


global loopKey
def LoopKeyDown():
	time.sleep(2)
	while(True):
		if(loopKey =='exit'):
			return
		FastKeyDown(loopKey)

def StartLoopKeyDown(key):
	print("start loop " ,key)
	global loopKey
	loopKey = key
	global t1
	t1 = threading.Thread(target=LoopKeyDown,args=())
	t1.start()


def StopLoopKeyDown():
	global loopKey
	loopKey ='exit'
	print('StopLoopKeyDown')


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
	time.sleep(0.1)
	DoKeyDown(duiKeys[y])
	time.sleep(0.1)

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
	DoKeyDown(playerKey)
	time.sleep(7)
	print("sleep...")
	if(WaitToClickImg('jjc/ship.png',maxTry=25) == False):
		WaitToClickImg('jjc/ship.png',maxTry=25)
	Click()
	time.sleep(2)
	LongTimeCheck("dxc/win.png","jjc/lose.png")
	time.sleep(1.5)
	DoKeyDown(nextKey)
	time.sleep(1.5)
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
	time.sleep(6)
	if(WaitToClickImg('jjc/ship.png',maxTry=20) == False):
		WaitToClickImg('jjc/ship.png',maxTry=20)
	Click()
	Click()
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
	if(IsHasImg("tansuo/topMana.png",False)):
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
	if(IsHasImg("tansuo/topExp.png",False)):
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
lastGroup =""

def StartDxc(index =1):
	print("===地下城==")
	global nextDxcLevel
	nextDxcLevel = index
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
	if(nextDxcLevel <= 1):
		print('wait box1...')
		WaitToClickImg(dxcDir + "/box1.png",False)
		print('found box1 => start')
	if(nextDxcLevel <= 0):
		nextDxcLevel = 1

	if(nextDxcLevel <= 1):
		DxcBoxFight(1)
		time.sleep(4)
		CheckAuto()
		DxcBoxFightWait() 	#1战中
	if(nextDxcLevel <= 2):
		DxcBoxFight(2)
		DxcBoxFightWait() #2
	if(nextDxcLevel <= 3):
		DxcBoxFight(3)
		DxcBoxFightWait() #3
	if(nextDxcLevel <= 4):
		DxcBoxFight(4)
		DxcBoxFightWait()  #4
	if(nextDxcLevel <= 5):
		if(isKillBoss):
			StartBoss()

def CheckAuto():
	if(WaitToClickImg('Main/auto2.png',True,match=0.93,isRgb=True,maxTry=40)):
		print('检测到自动未开启, 开启自动')
		WaitToClickImg('Main/auto2.png',True,match=0.93,isRgb=True,maxTry=6)

#进入地下城界面
def EnterDxc():
	WaitToClickImg("main/dxc.png")
	time.sleep(1.5)
	IsHasImg(dxcDir + "/ex.png")
	time.sleep(1)
	IsHasImg("main/sure.png")
	time.sleep(2)

def GetBossLoopKey(level):
	rawValue = dxcBossLoopRole
	values = rawValue.split(",")
	listLen = len(values)
	if(rawValue == ""):
		return '0'
	if(listLen > level):
		return values[level]
	return '0'

def GetGroupInfo(level,isBoss):
	rawValue = ""
	if(isBoss):
		rawValue = dxcGroupBoss
	else:
		rawValue =dxcGroupDaoZhong
	values = rawValue.split(",")
	listLen = len(values)
	if(rawValue == ""):
		return "5-1"
	if(listLen >= level):
		return values[level-1]
	else:
		return values[listLen-1]


def CheckSelectGroup(level,isBoss):
	global lastGroup
	curGroup= GetGroupInfo(level,isBoss)
	#如果上一个队伍和下一个队伍相同 则什么都不做
	if(lastGroup!= curGroup):
		time.sleep(1)
		lastGroup =curGroup
		infos = curGroup.split("-")
		SelectParty(int(infos[0]),int(infos[1]))
		time.sleep(1)


def DxcBoxFight(level):
	global nextDxcLevel
	nextDxcLevel = level+1
	#自动取消关闭奖励界面
	if(level == 1):
		ClickUntilNul(dxcDir + "/box1.png")
	elif(level == 2):
		ClickUntilNul(dxcDir + "/box2.png")
	elif(level == 3):
		ClickUntilNul(dxcDir + "/box3.png")
	elif(level == 4):
		ClickUntilNul(dxcDir + "/box4.png")

	time.sleep(1)
	DoKeyDown(playerKey)
	time.sleep(1.5)
	CheckSelectGroup(level,False)

	DoKeyDown(playerKey)

def DxcBoxFightWait():
	time.sleep(2.5)
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

	global StartBossIndex #0开始计数
	values = dxcGroupBoss.split(",")
	listLen = len(values)
	if(StartBossIndex >= listLen): #0开始计数
		print("===Boss 挑战 失败==='")
		return

	print('===StartBoss===')
	ClickUntilNul(dxcDir + "/box5.png")
	time.sleep(1)
	DoKeyDown(playerKey)

	time.sleep(0.4)

	CheckSelectGroup(StartBossIndex+1,True)
	time.sleep(0.4)

	DoKeyDown(playerKey)
	time.sleep(0.4)
	DoKeyDown(playerKey)

	roleLoop = GetBossLoopKey(StartBossIndex)
	print('roleLoop ',roleLoop)
	if(roleLoop != '0'):
		StartLoopKeyDown(roleLoop)

	StartBossIndex = StartBossIndex+1
	WaitBossFight()

def WaitBossFight():
	if(LongTimeCheck('dxc/win.png',dxcDir+'/lose.png')):
		#win
		print('win')
		StopLoopKeyDown()
		time.sleep(2.5)
		DoKeyDown(nextKey)
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
		time.sleep(2)
		DoKeyDown(nextKey)
		DoKeyDown(nextKey)
		time.sleep(1)
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
		Click()
	WaitToClickImg('tansuo/start.png')
	WaitToClickImg("main/sure.png")
	time.sleep(0.2)
	WaitToClickImg("main/skip.png")
	time.sleep(0.3)
	Click()


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
	time.sleep(0.4)
	WaitToClickImg('other/hhDown.png')
	time.sleep(0.2)
	for i in range(2):
		if(WaitToClickImg('other/sendBtn.png',True,match=0.93,isRgb=True)):
			WaitToClickImg('other/sendMax.png',True,True,7,False,0.85)
			WaitToClickImg('main/sure.png')
			time.sleep(0.2)
			DoKeyDown(exitKey)
			DoKeyDown(exitKey)


def GetZBPath(name):
	return os.path.join('other\\zuanbei\\',str(name)+'.png')

isRetryNeedZb = False

def needSeedZb():
	global isRetryNeedZb
	print('need Send ')
	if(isRetryNeedZb == False):
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

		if(isNeedSeed == False):
			isRetryNeedZb = True
			needSeedZb()
			return

	if(WaitToClickImg(GetZBPath(needZbName),False,maxTry = 8,match = 0.9) == False):
		print("找不到装备->反转排序")
		DoKeyDown(partyKey)
	if(WaitToClickImg(GetZBPath(needZbName),maxTry = 8,match = 0.9)):
		WaitToClickImg('other/needSend2.png')
		WaitToClickImg('main/sure.png')
		WaitToClickImg('main/sure.png')
	else:
		DoKeyDown(exitKey)
		DoKeyDown(exitKey)

def ghHomeTake():
	WaitToClickImg('main/ghHome.png')
	time.sleep(1)
	WaitToClickImg('main/ghHome_take.png')
	DoKeyDown(exitKey)
	WaitToClickImg('task/close.png')
	DoKeyDown(exitKey)

tuichuMaxTry =0

def ClickPlayer():
	if(WaitToClickImg('main/player'+mnqIndex+'.png',offsetY=55)):
		if(WaitToClickImg('tansuo/start2.png',match=hightMatch,isRgb=True,isClick=False,maxTry=6) == False):
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
	WaitToClickImg('main/player'+mnqIndex+'.png',offsetY=25)
	for	i in range(5):
		if(WaitToClickImg('tansuo/start2.png',match=hightMatch,isRgb=True,maxTry=8,isClick=False)):
			MoveToLeft()
		SaoDang(2)
		DoKeyDown(groupKeys[0])
		DoKeyDown(groupKeys[0])
		DoKeyDown(groupKeys[0])
	DoKeyDown(exitKey)
	ExitSaoDang()

def MoveToLeft():
	DoKeyDown('C')

def UseAllPower():
	print('OnHouDongHard')
	ToFightPage()
	WaitToClickImg('main/zhuXian.png',True)

	while(WaitToClickImg('main/player'+mnqIndex+'.png')==False):
		DoKeyDown(exitKey)
		if(WaitToClickImg('main/player'+mnqIndex+'.png')):
			break
	i = 0
	isSaodang = True
	while(WaitToClickImg('tansuo/start2.png',match=hightMatch,isRgb=True,maxTry=6,isClick=False)):
		MoveToLeft()
		i=i+1
		if(i>3):
			isSaodang =False
			break

	if(isSaodang):
		SaoDang(60)
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
		StartDxc(int(dxcStartLevel))
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

def CloseMoniqi():
	print("3 秒后关闭模拟器")
	time.sleep(3)
	win32api.ShellExecute(0, 'open', GetFullPath('CloseLeiDian.cmd'), '', '', 1)

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


def ClickCenter():
	print("Center")
	Click(x = width/2,y=height*0.4)
	Click(x = width/2,y=height*0.45)
	Click(x = width/2,y=height*0.35)

def WaitStart():
	print('=== WaitStart ===')
	while(IsHasImg("main/fight.png",False,stopTime=3) == False):
		DoKeyDown(exitKey)
		time.sleep(2)
		DoKeyDown(exitKey)
		time.sleep(3)
		if(IsHasImg("main/skipIco.png",True)):
			Click()
			time.sleep(2)
		if(IsHasImg("other/brithDay.png")):
			ClickCenter()

		if(IsHasImg("main/home.png",stopTime=3)):
			print("find home")


	time.sleep(0.5)
	DoKeyDown(exitKey)
	time.sleep(0.5)
	DoKeyDown(exitKey)
	while(IsHasImg("main/fight.png",False) == False):
		DoKeyDown(exitKey)
		time.sleep(1)
		DoKeyDown(exitKey)
		time.sleep(1)
	time.sleep(0.5)
	ToHomePage()

#按下Esc 停止
def CheckEnd(_key):
	while(True):
		keyboard.wait(_key)
		print(_key)
		os._exit(0)

#1-5是编组位置 6 是队伍
#num1-3 队伍位置
partyKey ='Y'
exitKey ='Z'
huodongKey='X'
playerKey = 'P'	#p是挑战位置
nextKey = 'L' #n 是下一步
endKey ='Esc'
#roleKey 123
listSelectKeys=['I','J','N']
roleKeys = ['1','2','3','4','5']
groupKeys = ['Q','W','E','R','T']
duiKeys =['U','H','B']


StartRunName = "启动模拟器并运行"
RunName = "运行"



def GetStrConfig(key):
	try:
		return cfg.get(MainSettingKey,key)
	except :
		return ""

def GetBoolConfig(boolKey):
	try:
		return Boolean(cfg.get(MainSettingKey,boolKey)=='True')
	except :
		return False

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
isAutoCloseKey ="isAutoClose"

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

dxcGroupDaoZhongKey ='DxcGroupDaoZhong'
dxcGroupBossKey ='DxcGroupBoss'
dxcBossLoopRoleKey ='dxcBossLoopRole'
dxcStartLevelKey ='dxcStartLevel'

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
isAutoClose = GetBoolConfig(isAutoCloseKey)

isHomeTake= GetBoolConfig(isHomeTakeKey)
isHouDongHard=GetBoolConfig(isHouDongHardKey)
isUseAllPower=GetBoolConfig(isUseAllPowerKey)
needZbName = GetStrConfig(needZbNameKey)


dxcGroupBoss=GetStrConfig(dxcGroupBossKey)
dxcGroupDaoZhong =GetStrConfig(dxcGroupDaoZhongKey)
dxcBossLoopRole = GetStrConfig(dxcBossLoopRoleKey)
dxcStartLevel = GetStrConfig(dxcStartLevelKey)
if(dxcStartLevel==""):
	dxcStartLevel = "1"

dxcBoss=GetStrConfig(dxcDropKey)
dxcDir = ''
if(dxcBoss =="炸脖龙"):
	dxcBossNum =1
	dxcDir ="dxc"
elif(dxcBoss =="绿龙"):
	dxcBossNum = 2
	dxcDir = "dxc_ex3"

#endregion
def test():
	time.sleep(1)
	for i in range(100):
		time.sleep(0.5)
		testWin(i,i)

	print("testend")
	time.sleep(40)
	return
def testWin(x,y):
	ret = win32gui.GetWindowRect(Subhwnd)
	ret2 = win32gui.GetClientRect(Subhwnd)
	height = ret[3] - ret[1]
	width = ret[2] - ret[0]
	tx = int(x * width/960)
	ty = int(y * height/540)
	print(ret,ret2)
	print(height,width,"oldPos:",x,y,"truePos:",tx,ty)

	return

def RunAutoPcr():
	#按下Esc键停止
	global t0
	global t1
	t0 = threading.Thread(target=CheckEnd,args=(endKey,))
	t0.start()
	WaitWin32Start()
	# test()
	time.sleep(0.5)
	if(isRunAndStart):
		print('Wait Start... 20s ')
		time.sleep(20)
		WaitStart()
	else:
		time.sleep(2)

	print('=== Start ===')
	print('\n=== 按Exc退出程序 ===\n')
#日常
	DailyTasks()
	# tuichu()
	print('=== end ===')

	if(isAutoClose):
		CloseMoniqi()

	time.sleep(2)
	os._exit(0)

if __name__ == '__main__':
	RunAutoPcr()