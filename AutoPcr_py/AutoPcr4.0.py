from configparser import ConfigParser
import ctypes
import inspect
import threading
import time
import os
from ctypes import *
from PIL import ImageGrab
from PIL import Image
import aircv as ac
import keyboard
import win32gui, win32ui, win32con,win32api,win32print
import sys
#region 获取当前路径
curDir = os.path.dirname(__file__)

print(os.path.dirname(__file__),"\ncwd",os.getcwd())

os.chdir(curDir)

if(os.path.exists('.\\config.ini') == False):
	print('no config ->Exe Run')
	# log = curDir+" os.path.dirname(sys.executable) "+os.path.dirname(sys.executable)
	# sg.popup(log)
	time.sleep(0.5)
	curDir =os.path.dirname(sys.executable)
	os.chdir(curDir)

#图片路径拼接
def GetFullPath(pngName):
    return '.\\' + pngName

#endregion

waitTime = 0
minMatch = 0.7 #最低相似度匹配
hightMatch = 0.90
warnMatch = 0.85 #相似度小于此时, 打印黄字

tMain = threading.Thread()
t0 =threading.Thread()
t1 = threading.Thread()

#region 读取配置
#其他页面
useAllMoveTimeKey = "useAllMoveTime"
moniqTimeKey = 'moniqTime'
dxcDropKey ='dxcDrop'
mnqIndexKey ='mnqDrop'
isMultKey ='isMult'
dxcDropValue =["炸脖龙","绿龙","ex4"]
mnqIndexDropValue=["1","0"]

cfg = ConfigParser()
configPath = GetFullPath('config.ini')
cfg.read(configPath,encoding='utf-8')

isMult =cfg.getboolean('MainSetting',isMultKey,fallback=False)

mnqIndex = cfg.get('MainSetting',mnqIndexKey,fallback='0')

def string_to_float(str):
	try:
		return float(str)
	except:
		return 20
def string_to_Int(str):
	try:
		return int(str)
	except:
		return 0

useAllMoveTime =string_to_Int(cfg.get('MainSetting',useAllMoveTimeKey,fallback='0'))

moniqTime = string_to_float(cfg.get('MainSetting',moniqTimeKey,fallback='20'))

MainSettingKey='MainSetting_'+str(mnqIndex)

#region win32初始化
#获取后台窗口的句柄，注意后台窗口不能最小化
#雷电模拟器 或 雷电模拟器-1 或直接None

window_title = None
MainhWnd =  0
Subhwnd = None
width = 960
height = 540
Scale = 1
saveDC = None
mfcDC = None
saveBitMap = None


#获取真正的大小
rect=None
trueH=0
trueW=0
SaveH=0
SaveW=0
lastX=0
lastY =0

def winfun(hwnd, lparam):
	global Subhwnd
	subtitle = win32gui.GetWindowText(hwnd)
	if subtitle == 'TheRender':
		Subhwnd = hwnd
		print("Find Subhwnd",Subhwnd)


def get_real_resolution():
    """获取真实的分辨率"""
    hDC = win32gui.GetDC(0)
    wide = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
    high = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
    return {"wide": wide, "high": high}


def get_screen_size():
    """获取缩放后的分辨率"""
    wide = win32api.GetSystemMetrics(0)
    high = win32api.GetSystemMetrics(1)
    return {"wide": wide, "high": high}


def get_scaling():
    '''获取屏幕的缩放比例'''
    real_resolution = get_real_resolution()
    screen_size = get_screen_size()
    proportion = round(real_resolution['wide'] / screen_size['wide'], 2)
    return proportion


def WaitWin32Start():
	#如果Main为0则等待
	global window_title,MainhWnd,Subhwnd,saveDC,mfcDC,saveBitMap,Scale,SaveH,SaveW
	global rect,trueH,trueW
	if(mnqIndex == "0"):
		window_title ="雷电模拟器"
	elif(mnqIndex == "1"):
		window_title ="雷电模拟器-1"

	if(isFor64):
		window_title = window_title+"(64)"

	MainhWnd = 0
	while(MainhWnd ==0):
		print("等待模拟器启动中...:")
		if(isMult):
			MainhWnd =  win32gui.FindWindow('LDPlayerMainFrame', window_title)
		else:
			MainhWnd =  win32gui.FindWindow('LDPlayerMainFrame',None)
		time.sleep(1.5)


	#已打开雷电
	print("Find MainhWnd",MainhWnd)
	win32gui.EnumChildWindows(MainhWnd, winfun, None)
	while(Subhwnd == None):
		time.sleep(1.5)
		print("wait subHwnd...")
		win32gui.EnumChildWindows(MainhWnd, winfun, None)

	#获取窗口大小
	rect = win32gui.GetClientRect(Subhwnd)
	trueH = rect[3]
	trueW = rect[2]
	Scale = get_scaling()

	print("TrueH ",trueH, "TrueW",trueW ,"Scale",Scale)
	SaveW = int(trueW * Scale)
	SaveH = int(trueH * Scale)
	print("SaveH ",SaveH, "SaveW",SaveW)

	hWndDC = win32gui.GetWindowDC(Subhwnd)
	#创建设备描述表
	mfcDC = win32ui.CreateDCFromHandle(hWndDC)
	#创建内存设备描述表
	saveDC = mfcDC.CreateCompatibleDC()
	#创建位图对象准备保存图片
	saveBitMap = win32ui.CreateBitmap()
	#saveBitMap.CreateCompatibleBitmap(mfcDC,trueW,trueH)
	#saveBitMap.CreateCompatibleBitmap(mfcDC,width,height)
	saveBitMap.CreateCompatibleBitmap(mfcDC,SaveW,SaveH)
	#将截图保存到saveBitMap中
	saveDC.SelectObject(saveBitMap)


def SavaShoot():
	#保存bitmap到内存设备描述表
	global window_title,MainhWnd,Subhwnd,saveDC,mfcDC,saveBitMap
	#saveDC.BitBlt((0,0), (width,height), mfcDC, (0, 0), win32con.SRCCOPY)
	win32con.SRCINVERT
	saveDC.BitBlt((0,0), (SaveW,SaveH), mfcDC, (0, 0), win32con.SRCCOPY)
	bmpinfo = saveBitMap.GetInfo()
	bmpstr = saveBitMap.GetBitmapBits(True)

	#im_PIL = Image.frombuffer('RGB',(bmpinfo['bmWidth'],bmpinfo['bmHeight']),bmpstr,'raw','BGRX',0,1)
	im_PIL = Image.frombuffer('RGB',(SaveW,SaveH),bmpstr,'raw','BGRX',0,1)

	newImg = im_PIL.resize((width,height),Image.Resampling.LANCZOS)

	newImg.save(GetFullPath("temp.png")) #保存

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


def Click(x=None, y=None):
	try:
		global Subhwnd,lastY,lastX,rect,trueH,trueW
		if(x==None):
			x = lastX
			y = lastY
		else:
			lastX = x
			lastY = y

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
def IsHasImg(targetImg,isClick = True,stopTime = 4,offsetY=0,isRgb =False,match=minMatch):
	return WaitToClickImg(targetImg,isClick,True,stopTime,offsetY= offsetY,isRgb=isRgb,match=match)

#等待图片出现,低频率检测, 但不点击
def WaitImgLongTime(targetImg,autoExit = False):
	maxTryTime = 30*4  #4分钟 最大等待上限
	longTimer = 0
	while (WaitToClickImg(targetImg,False,True,autoExit=autoExit) == False):
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
			y1 = y1+(offsetY*trueH/540)
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
			if(waitTime < maxTry and autoExit):
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
def ClickUntilNul(path,offsetY=0,maxTry = 20,isRgb= False,match=minMatch,nullWait =0.5):
	WaitToClickImg(path,offsetY= offsetY,isRgb= isRgb,match=match)
	time.sleep(nullWait)
	tryTime =0
	while(IsHasImg(path,offsetY= offsetY,isRgb= isRgb,match=match)):
		if(tryTime >maxTry):
			break
		tryTime = tryTime+1
		IsHasImg(path,offsetY= offsetY,isRgb=  isRgb,match=match)

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
	LongTimeCheck("jjc/win.png","jjc/lose.png")
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

#跳过地下城
def StartDxcSkip():
	print("===地下城== ",dxcBoss)
	ToFightPage()
	#进入地下城
	EnterDxc()


def CheckAuto():
	if(WaitToClickImg('Main/auto2.png',True,match=0.93,isRgb=True,maxTry=40)):
		print('检测到自动未开启, 开启自动')
		WaitToClickImg('Main/auto2.png',True,match=0.93,isRgb=True,maxTry=6)

#进入地下城界面
def EnterDxc():
	WaitToClickImg("main/dxc.png")
	time.sleep(1.5)
	IsHasImg("dxc/ex"+str(dxcBossNum)+".png")
	time.sleep(1)
	IsHasImg("dxc/dxcSkip.png")
	IsHasImg("main/sure.png")
	ToHomePage()

#endregion

def BuyExp():
	time.sleep(1)
	ToHomePage()
	ToShopPage()
	WaitToClickImg('shop/shopTop.png',False)

	buyTime = 1
	if(isBuyMoreExp):
		buyTime = 5

	for i in range(buyTime):
		if(i==0 and (IsHasImg('shop/exp2.png',False) == False)):
			# ToHomePage()
			print('no to buy->update')
			WaitToClickImg('shop/update.png',isRgb= True)
			WaitToClickImg('main/sure.png')
		if(i>0):
			WaitToClickImg('shop/update.png',isRgb= True)
			WaitToClickImg('main/sure.png')
		expCounter = 1
		WaitToClickImg('shop/all.png')

		WaitToClickImg('shop/buyBtn.png',isRgb= True)
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


	if(WaitToClickImg('tansuo/start.png',match=hightMatch,isRgb=True,maxTry=8,isClick=False) == False):
		MoveToLeft()
		if(WaitToClickImg('tansuo/start2.png',match=hightMatch,isRgb=True,maxTry=8,isClick=False)):
			MoveToLeft()

	if(WaitToClickImg('tansuo/start.png',match=hightMatch,isRgb=True,maxTry=8,isClick=False)):
		if(WaitToClickImg('tansuo/plus.png')):
			for i in range(_time):
				Click()
		WaitToClickImg('tansuo/start.png')
		WaitToClickImg("main/sure.png")
		time.sleep(0.2)
		WaitToClickImg("main/skip.png")
		time.sleep(0.3)
		Click()
		return True
	else:
		print("没体力- > 结束")
		return False


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
	for i in range(2):
		if(SaoDang()):
			SmallExit()
			SmallExit()
			SmallExit()
			MoveToLeft()
		else:
			ExitSaoDang()
			return
	ExitSaoDang()


def xinSui():
	if(WaitToClickImg('tansuo/xinSuiEnter.png')==False):
		ExitSaoDang()
		WaitToClickImg('tansuo/xinSuiEnter.png')

	WaitToClickImg('tansuo/xinSuiTop.png',False)
	DoKeyDown(listSelectKeys[0])
	for i in range(3):
		print(i)
		if(SaoDang()):
			SmallExit()
			SmallExit()
			SmallExit()
			MoveToLeft()
		else:
			ExitSaoDang()
			return
	ExitSaoDang()

def DianZan():
	print()
	ToHomePage()
	WaitToClickImg('other/hanghui.png')
	time.sleep(0.8)
	if(WaitToClickImg('other/menber.png',maxTry=25)==False):
		SmallExit()
		WaitToClickImg('other/menber.png')
	else:
		WaitToClickImg('other/menber.png')

	WaitToClickImg('other/dianzan.png')
	WaitToClickImg('main/sure.png')
	ToHomePage()

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

def needSeedZbStart():
	global isRetryNeedZb
	print('need Send ')
	if(isRetryNeedZb == False):
		ToHomePage()
		WaitToClickImg('other/hanghui.png')
	time.sleep(1)
	WaitToClickImg('other/needSend.png')
	Click()

	time.sleep(1)
	DoKeyDown(groupKeys[0])
	DoKeyDown(groupKeys[0])


	if(IsHasImg('other/needSend.png',False)==False):
		needSeedZb()
	else:
		print("确认上期")
		WaitToClickImg('other/needSend.png')
		time.sleep(1)
		needSeedZb()


def needSeedZb():
	if(WaitToClickImg(GetZBPath(needZbName),False,maxTry = 8,match = 0.9) == False):
		print("找不到装备->选第一个")
		# DoKeyDown(partyKey)
	WaitToClickImg('other/needSend2.png')
	WaitToClickImg('main/sure.png')
	WaitToClickImg('main/sure.png')


def ghHomeTake():
	WaitToClickImg('main/ghHome.png')
	time.sleep(1)
	WaitToClickImg('main/ghHome_take.png')
	DoKeyDown(exitKey)
	WaitToClickImg('task/close.png')
	DoKeyDown(exitKey)

tuichuMaxTry =0

def ClickPlayer():
	global playerName
	if(playerName==""):
		print("玩家角色 为空!")
		playerName = "player0"

	# if (WaitToClickImg('main/'+playerName+'.png',False,True) == False):
	# 	DoKeyDown(exitKey)
	# 	DoKeyDown(exitKey)
	# 	DoKeyDown(exitKey)
	# 	time.sleep(0.2)
	time.sleep(0.1)
	if(WaitToClickImg('main/'+playerName+'.png',False)):
		time.sleep(0.1)
		DoKeyDown(exitKey)
		ClickUntilNul('main/'+playerName+'.png',offsetY=50,maxTry=8,isRgb= True,match=0.6)
	else:
		DoKeyDown(exitKey)
		DoKeyDown(exitKey)
		DoKeyDown(exitKey)
		if(IsHasImg("main/home.png",False)):
			ClickPlayer()
		else:
			#在里面
			print("在战斗中->等待战斗结束")
			WaitToClickImg("main/next2.png")


def WaitFinghtEndNext():
	print('>>WaitFinghtEndNext')

	while (WaitToClickImg("main/next2.png",False,True) == False):
		DoKeyDown(exitKey)
		DoKeyDown(exitKey)
		DoKeyDown(exitKey)
		time.sleep(0.4)

	WaitToClickImg("main/next2.png")
	DoKeyDown(exitKey)
	time.sleep(0.2)
	DoKeyDown(exitKey)
	time.sleep(0.2)
	DoKeyDown(exitKey)
	ClickUntilNul("main/next2.png")

	#最后一次检查
	if(IsHasImg("main/next2.png")):
		DoKeyDown(nextKey)
		DoKeyDown(nextKey)



def OnTuituStart():

	if(IsHasImg("main/home.png",False)):
		#在外面
		print("非战斗状态->点击玩家")
		OnTuituLoop()
	else:
		#在里面
		print("在战斗中->等待战斗结束")
		WaitFinghtEndNext()
		OnTuituLoop()

def OnTuituLoop():
	print('>>OnTuituLoop')
	ClickPlayer()
	if( WaitToClickImg('tansuo/start2.png',match=hightMatch,isRgb=True,maxTry=16,isClick=False)):
		print("检测到不能扫荡 -> 新关卡")
		time.sleep(0.2)
		DoKeyDown(playerKey)
		DoKeyDown(playerKey)
		time.sleep(0.8)
		DoKeyDown(playerKey)
		DoKeyDown(playerKey)
		DoKeyDown(playerKey)
		print("enterFight sleep 4")
		time.sleep(4)

		if(IsHasImg('main/sure.png',False)):
			print("没有体力了-> 结束")
			ExitSaoDang()
			return
		print("enterFight sleep 8")
		time.sleep(8)

		WaitFinghtEndNext()
		time.sleep(1.5)  #过渡
		OnTuituLoop()
	else:
		if(WaitToClickImg('tansuo/start.png',match=hightMatch,isRgb=True,maxTry=8,isClick=False)):
			print("已经全部通关...")
			ExitSaoDang()
		else:
			#意外弹出->退出重来
			ExitSaoDang()
			OnTuituLoop()
			return

def OnAutoTaskStart():
	print("AutoTask")
	OnAutoTask()

menuNofindTime=0

def OnAutoTask():
	print("AutoTask")
	isNoAct = True

	#菜单存在时
	if(IsHasImg('task/menu.png')):
		isNoAct = False
		if(IsHasImg('task/skip.png',match=0.8)):
			#蓝色按钮
			WaitToClickImg('task/skipBtn.png')
		else:
			#出现选项时
			if(IsHasImg("task/menu_black.png",False,isRgb=True)):
				ClickCenter()
				OnAutoTask()
				return
		time.sleep(0.6)

	#优先级 菜单 > 蓝色或关闭 按钮 > 什么都没有
	#优先级 noSound > skipBtn > close

	if(IsHasImg('task/noSound.png')):
		isNoAct = False
		time.sleep(0.6)
	if(IsHasImg('task/skipBtn.png')):
		isNoAct = False
	if(IsHasImg('task/close.png',stopTime=6)):
		isNoAct = False
		time.sleep(0.4)
		IsHasImg('task/noSound.png')
		time.sleep(0.8)

	if(isNoAct):
		if(IsHasImg('main/home.png',False)):
			time.sleep(0.6)
			if(IsHasImg('main/home.png',False,match=0.9)):
				print("任务结束")
				#NextChapter()
				return
		else:
			ClickCenter()
	print("=====Again======")
	OnAutoTask()

#下一章节
def NextChapter():
	print('切换下章节')
	WaitToClickImg('main/back.png')
	DoKeyDown(listSelectKeys[0]) #i
	DoKeyDown(listSelectKeys[0]) #i
	WaitToClickImg('main/back.png',False)
	DoKeyDown(listSelectKeys[1]) #i
	WaitToClickImg('task/noSound.png')
	OnAutoTask()

def OnHouDongHard():
	print('OnHouDongHard')
	ToFightPage()
	WaitToClickImg('main/dxc.png',False) #地下城入口存在->达到Fight界面
	DoKeyDown(huodongKey)
	time.sleep(0.5)
	DoKeyDown(exitKey)
	time.sleep(0.5)
	DoKeyDown(exitKey)
	ClickPlayer()

	for	i in range(5):
		if(SaoDang(2)):
			SmallExit()
			SmallExit()
			SmallExit()
			MoveToLeft()
		else:
			print("没体力 ->结束")
			break
	DoKeyDown(exitKey)
	ExitSaoDang()



def SmallExit():
	DoKeyDown(groupKeys[0])  #小退出,Q

def MoveToLeft():
	if(WaitToClickImg('tansuo/saodang.png',False)==False):
		DoKeyDown(exitKey)
	DoKeyDown('C')

def CurSaodang():
	ClickPlayer()
	SaoDang()

def UseAllPower():
	print('OnHouDongHard')
	ToFightPage()
	WaitToClickImg('main/zhuXian.png',True)

	ClickPlayer()

	for	i in range(useAllMoveTime):
		MoveToLeft()


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
		StartDxcSkip()
	if(isHomeTake):
		ghHomeTake()
		StartTakeAll()

	if(isXQB):
		EnterDiaoCha()
		Xqb()
	if(isXinSui):
		EnterDiaoCha()
		xinSui()
	if(isDianZan):
		DianZan()
	if(isSend):
		SendZb()
	if(isNeedSeed):
		needSeedZbStart()
	if(isHouDongHard):
		OnHouDongHard()
	if(isUseAllPower):
		UseAllPower()
		StartTakeAll()
	if(isTuitu):
		OnTuituStart()
	if(isHomeTake):
		TakeGift()
	if(isAutoTask):
		OnAutoTask()


def CloseMoniqi():
	print("3 秒后关闭模拟器")
	time.sleep(3)
	cmdStr = "cd /d "+LeiDianDir+" & dnconsole.exe quitall"
	print("cmdstr",cmdStr)
	os.system(cmdStr)
	# win32api.ShellExecute(0, 'open', GetFullPath('CloseLeiDian.cmd'), '', '', 1)

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
	Click(x = width/2,y=height*0.55)
	Click(x = width/2,y=height*0.53)
	Click(x = width/2,y=height*0.50)
	Click(x = width/2,y=height*0.45)
	Click(x = width/2,y=height*0.43)
	Click(x = width/2,y=height*0.40)

def WaitStart():
	print('=== WaitStart ===')
	while(IsHasImg("main/fight.png",False,stopTime=3) == False):
		DoKeyDown(exitKey)
		time.sleep(2)
		DoKeyDown(exitKey)
		time.sleep(3)
		#更新
		if(IsHasImg("main/sure.png",True)):
			Click()
			time.sleep(10)
			print('=== Update sleep 10 ===')
		#跳过生日
		if(IsHasImg("main/skipIco.png",True)):
			Click()
			time.sleep(2)
			ClickCenter()


		if(IsHasImg("task/menu.png",True)):
			if(IsHasImg("task/skip.png",True)):
				WaitToClickImg("main/sure.png",True)
			else:
				if(IsHasImg("task/menu_black.png",False,isRgb=True)):
					ClickCenter()
		# if(IsHasImg("other/brithDay.png")):


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
	return cfg.get(MainSettingKey,key,fallback='')

def GetBoolConfig(boolKey):
	return cfg.getboolean(MainSettingKey,boolKey,fallback=False)

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
isTuituKey='isTuituKey'
isFor64Key ='isFor64'
isAutoTaskKey='isAutoTask'

#newKey
isXQBKey='isXQB'
isXinSuiKey='isXinSui'
isSendKey='isSend'

isNeedSeedKey ='isNeedSeed'
isKillBossKey ='isKillBoss'

isDianZanKey='isDianZan'
isHomeTakeKey='isHomeTake'
isHouDongHardKey='isHouDongHard'
isUseAllPowerKey='isUseAllPower'
needZbNameKey = 'needZbName'
playerNameKey = 'playerName'

dxcGroupDaoZhongKey ='DxcGroupDaoZhong'
dxcGroupBossKey ='DxcGroupBoss'
dxcBossLoopRoleKey ='dxcBossLoopRole'
isBuyMoreExpKey = 'isBuyMoreExp'

isBuyMoreExp = GetBoolConfig(isBuyMoreExpKey)
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
isTuitu = GetBoolConfig(isTuituKey)
isFor64 = GetBoolConfig(isFor64Key)
isAutoTask = GetBoolConfig(isAutoTaskKey)

isDianZan = GetBoolConfig(isDianZanKey)
isHomeTake= GetBoolConfig(isHomeTakeKey)
isHouDongHard=GetBoolConfig(isHouDongHardKey)
isUseAllPower=GetBoolConfig(isUseAllPowerKey)
needZbName = GetStrConfig(needZbNameKey)
playerName = GetStrConfig(playerNameKey)

dxcGroupBoss=GetStrConfig(dxcGroupBossKey)
dxcGroupDaoZhong =GetStrConfig(dxcGroupDaoZhongKey)
dxcBossLoopRole = GetStrConfig(dxcBossLoopRoleKey)


dxcBoss=GetStrConfig(dxcDropKey)

if(dxcBoss =="炸脖龙"):
	dxcBossNum =2
elif(dxcBoss =="绿龙"):
	dxcBossNum = 3
else:
	dxcBossNum = 4


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
	#CurSaodang()

	time.sleep(0.5)
	if(isRunAndStart):
		print('Wait Start... ',moniqTime,"s")
		time.sleep(moniqTime)
		WaitStart()
	else:
		time.sleep(2)

	print('=== 开始 按Exc退出程序 ===\n')

#日常
	# OnAutoTask()
	DailyTasks()
	# tuichu()
	print('=== end ===')

	if(isAutoClose):
		CloseMoniqi()

	time.sleep(2)
	os._exit(0)

if __name__ == '__main__':
	RunAutoPcr()