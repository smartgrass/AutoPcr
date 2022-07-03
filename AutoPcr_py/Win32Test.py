import win32gui, win32ui, win32con,win32api
import time
from ctypes import windll

from PIL import Image

import os

curDir = os.path.dirname(__file__)
#图片路径拼接
def GetFullPath(pngName):
	global curDir
	return os.path.join(curDir,pngName)
#获取后台窗口的句柄，注意后台窗口不能最小化
window_title = "雷电模拟器"
hWnd =  win32gui.FindWindow('LDPlayerMainFrame', window_title)#窗口的类名可以用Visual Studio的SPY++工具获取
_subhwin = 10

key_map = {
    "0": 49, "1": 50, "2": 51, "3": 52, "4": 53, "5": 54, "6": 55, "7": 56, "8": 57, "9": 58,
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

#获取句柄窗口的大小信息
left, top, right, bot = win32gui.GetWindowRect(hWnd)
width = right - left
height = bot - top
#返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
hWndDC = win32gui.GetWindowDC(hWnd)
#创建设备描述表
mfcDC = win32ui.CreateDCFromHandle(hWndDC)
#创建内存设备描述表
saveDC = mfcDC.CreateCompatibleDC()
#创建位图对象准备保存图片
saveBitMap = win32ui.CreateBitmap()
saveBitMap.CreateCompatibleBitmap(mfcDC,width,height)
def SavaShoot():
	#将截图保存到saveBitMap中
	saveDC.SelectObject(saveBitMap)
	#保存bitmap到内存设备描述表
	saveDC.BitBlt((0,0), (width,height), mfcDC, (0, 0), win32con.SRCCOPY)
	bmpinfo = saveBitMap.GetInfo()
	bmpstr = saveBitMap.GetBitmapBits(True)

	im_PIL = Image.frombuffer('RGB',(bmpinfo['bmWidth'],bmpinfo['bmHeight']),bmpstr,'raw','BGRX',0,1)
	im_PIL.save(GetFullPath("temp.png")) #保存
	# im_PIL.show() #显示



def click(x, y):
	try:
		hwin = win32gui.FindWindow('LDPlayerMainFrame', window_title)
		#遍历所有子窗口
		def winfun(hwnd, lparam):
			global _subhwin
			subtitle = win32gui.GetWindowText(hwnd)
			if subtitle == 'TheRender':
				_subhwin = hwnd
		print(_subhwin)
		win32gui.EnumChildWindows(hwin, winfun, None)
		ret = win32gui.GetWindowRect(_subhwin)
		height = ret[3] - ret[1]
		width = ret[2] - ret[0]
		tx = int(x * width/540)
		ty = int(y * height/960)
		positon = win32api.MAKELONG(tx, ty)
		win32api.SendMessage(_subhwin, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, positon)
		win32api.SendMessage(_subhwin, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON,positon)
	except Exception as e:
		print(f"fallback adb click:{e}")

def testKey():
	win32gui.PostMessage(_subhwin, win32con.WM_KEYDOWN, 90, 0)
	win32gui.PostMessage(_subhwin, win32con.WM_KEYUP, 90, 0)

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




if __name__ == '__main__':
	print("start")
	click(200,100)
	for i in range(0,10):
		print("shoot")
		time.sleep(0.2)
		testKey()

	# time.sleep(5)
	# SavaShoot()
	print("shoot")
