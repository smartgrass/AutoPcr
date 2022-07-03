import win32gui, win32ui, win32con,win32api

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
#为bitmap开辟存储空间
saveBitMap.CreateCompatibleBitmap(mfcDC,width,height)
#将截图保存到saveBitMap中
saveDC.SelectObject(saveBitMap)
#保存bitmap到内存设备描述表
saveDC.BitBlt((0,0), (width,height), mfcDC, (0, 0), win32con.SRCCOPY)
bmpinfo = saveBitMap.GetInfo()
bmpstr = saveBitMap.GetBitmapBits(True)

im_PIL = Image.frombuffer('RGB',(bmpinfo['bmWidth'],bmpinfo['bmHeight']),bmpstr,'raw','BGRX',0,1)

im_PIL.save(GetFullPath("temp.png")) #保存

im_PIL.show() #显示



def click(self, x, y):
	if self.click_by_mouse:
		window_title = self._getWindowTitle()
		try:
			hwin = win32gui.FindWindow('LDPlayerMainFrame', window_title)
			self._subhwin = None
			def winfun(hwnd, lparam):
				subtitle = win32gui.GetWindowText(hwnd)
				if subtitle == 'TheRender':
					self._subhwin = hwnd
			win32gui.EnumChildWindows(hwin, winfun, None)
			ret = win32gui.GetWindowRect(self._subhwin)
			height = ret[3] - ret[1]
			width = ret[2] - ret[0]
			tx = int(x * width/540)
			ty = int(y * height/960)
			positon = win32api.MAKELONG(tx, ty)
			win32api.SendMessage(self._subhwin, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, positon)
			win32api.SendMessage(self._subhwin, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON,positon)
		except Exception as e:
			print(f"fallback adb click:{e}")
	else:
		print(f"else")


if __name__ == '__main__':
	print()