from abc import ABCMeta, abstractmethod
from typing import Tuple
from win32 import win32gui, win32api, win32console
import ctypes
from win32.lib import win32con
from pythonwin import win32ui
import numpy as np
# import matplotlib.pyplot as plt
from cv2 import cv2 as cv
import os
# from . import constants
import time


class Driver(metaclass=ABCMeta):
    @abstractmethod
    def click(self, x, y):
        pass

    @abstractmethod
    def input(self, text):
        pass

    @abstractmethod
    def screenshot(self, output="screen_shot.png"):
        pass

    @abstractmethod
    def getScreenSize(self) -> Tuple[int, int]:
        pass

    @abstractmethod
    def swipe(self, start: Tuple[int, int], end: Tuple[int, int], duration: int):
        pass

    def getRootWindowLocation(self) -> Tuple[int, int]:
        # 获取根窗口的位置坐标
        return (0,0)

    def getScale(self):
        return 1


class ADBDriver(Driver):
    def __init__(self, device_name):
        super().__init__()
        self.device_name = device_name

    def click(self, x, y):
        self._shell("input tap {} {}".format(x, y))

    def input(self, text):
        self._shell("input text {}".format(text))

    def screenshot(self, output="screen_shot.png"):
        # 每次要花1-2秒
        self._shell("screencap -p /sdcard/opsd.png")
        output = "{}-{}".format(self.device_name, output)
        self._cmd("pull /sdcard/opsd.png {}".format(output))
        return output

    def getScreenSize(self) -> Tuple[int, int]:
        return map(lambda x: int(x), self._shell("wm size", True).split(":")[-1].split("x"))


    def swipe(self, start, end=None, duration=500):
        if not end:
            end = start
        self._shell("input swipe {} {} {} {} {}".format(
            *start, *end, duration))

    def _shell(self, cmd, ret=False):
        return self._cmd("shell {}".format(cmd))

    def _cmd(self, cmd, ret=False):
        cmd = "adb -s {} {}".format(self.device_name, cmd)
        if ret:
            os.system(cmd)
        else:
            return os.popen(cmd).read()

class DNADBDriver(ADBDriver):
    '''
    基于ADB的雷电模拟器扩展驱动
    '''

    def __init__(self, device_name, dnpath, index, click_by_mouse=False):
        super().__init__(device_name)
        self.dnpath = dnpath
        self.index = index
        self.click_by_mouse = click_by_mouse
        shcore = ctypes.windll.shcore
        monitor = win32api.MonitorFromPoint((0,0),1)
        scale = ctypes.c_int()
        shcore.GetScaleFactorForMonitor(
            monitor.handle,
            ctypes.byref(scale)
        )
        self.scale = float(scale.value / 100)

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
                tx = int(x * width/constants.BASE_WIDTH)
                ty = int(y * height/constants.BASE_HEIGHT)
                positon = win32api.MAKELONG(tx, ty)
                win32api.SendMessage(self._subhwin, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, positon)
                win32api.SendMessage(self._subhwin, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON,positon)
            except Exception as e:
                print(f"fallback adb click:{e}")
                super().click(x,y)
        else:
            super().click(x, y)

    def input(self, text):
        '''
        adb 不支持中文使用dnconsole接口
        '''
        contain_hanzi = False
        for char in text:
            if '\u4e00' <= char <= '\u9fa5':
                contain_hanzi = True
                break
        if contain_hanzi:
            os.system(
                '{}\ldconsole.exe action --index {} --key call.input --value "{}"'.format(self.dnpath, self.index, text))
        else:
            super().input(text)

    def screenshot(self, output='screen_shot.png'):
        window_title = self._getWindowTitle()
        width, height = constants.BASE_WIDTH, constants.BASE_HEIGHT
        try:
            hwin = win32gui.FindWindow('LDPlayerMainFrame', window_title)
            self._subhwin = None
            def winfun(hwnd, lparam):
                subtitle = win32gui.GetWindowText(hwnd)
                if subtitle == 'TheRender':
                    self._subhwin = hwnd
            win32gui.EnumChildWindows(hwin, winfun, None)
            hwindc = win32gui.GetWindowDC(self._subhwin)
            srcdc = win32ui.CreateDCFromHandle(hwindc)
            memdc = srcdc.CreateCompatibleDC()
            bmp = win32ui.CreateBitmap()
            bmp.CreateCompatibleBitmap(srcdc, width, height)
            memdc.SelectObject(bmp)
            memdc.BitBlt((0, 0), (width, height), srcdc,
                         (0, 0), win32con.SRCCOPY)
            signedIntsArray = bmp.GetBitmapBits(True)
            img = np.frombuffer(signedIntsArray, dtype='uint8')
            img.shape = (height, width, 4)
            srcdc.DeleteDC()
            memdc.DeleteDC()
            win32gui.ReleaseDC(hwin, hwindc)
            win32gui.DeleteObject(bmp.GetHandle())
            return img[:, :, :3]
        except Exception as e:
            print(e)
            return super().screenshot(output=output)

    def getRootWindowLocation(self):
        window_title = self._getWindowTitle()
        try:
            hwin = win32gui.FindWindow('LDPlayerMainFrame', window_title)
            ret = win32gui.GetWindowRect(hwin)
            return (ret[0], ret[1] + self._getDnToolbarHeight())
        except:
            return super().getRootWindowLocation()

    def _getDnToolbarHeight(self):
        return 27

    def _getWindowTitle(self):
        window_title = '雷电模拟器'
        if self.index > 0:
            window_title = "{}-{}".format(window_title, self.index)
        return window_title

    def getScale(self):
        return self.scale