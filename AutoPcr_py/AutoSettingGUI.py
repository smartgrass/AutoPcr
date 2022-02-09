
import sys
from sysconfig import get_path
from xmlrpc.client import Boolean
import PySimpleGUI as sg
from configparser import ConfigParser
from importlib.resources import path
from re import A
import os
from ctypes import *
import win32api

#Glabol
print("path " ,os.path.dirname(sys.executable))
# print("path " , os.getcwd())

curDir = os.path.dirname(__file__)
#图片路径拼接
def GetFullPath(pngName):
	global curDir
	return os.path.join(curDir,pngName)
#======读取配置======

cfg = ConfigParser()
configPath = GetFullPath('config.ini')
cfg.read(configPath)
isRunAndStart = False
isJJC = Boolean(cfg.get('MainSetting','isJJC')=='True')
isTansuo = Boolean(cfg.get('MainSetting','isTansuo')=='True')
isDxc = Boolean(cfg.get('MainSetting','isDxc')=='True')
isExp = Boolean(cfg.get('MainSetting','isExp')=='True')
isNiuDan = Boolean(cfg.get('MainSetting','isNiuDan')=='True')

StartRunName = "启动模拟器并运行"
RunName = "运行"

def SetCurConfig(AllValues):
	global isJJC,isTansuo,isExp,isDxc,isSend,isNiuDan
	isJJC = AllValues[0]
	isTansuo =AllValues[1]
	isDxc=AllValues[2]
	isExp=AllValues[3]
	isNiuDan = AllValues[4]
#保存配置
def SavaConfig(AllValues):
	cfg.set('MainSetting', 'isJJC', str(isJJC))
	cfg.set('MainSetting', 'isTansuo', str(isTansuo))
	cfg.set('MainSetting', 'isDxc', str(isDxc))
	cfg.set('MainSetting', 'isExp', str(isExp))
	cfg.set('MainSetting', 'isNiuDan', str(isNiuDan))
	cfg.set('MainSetting', 'isRunAndStart', str(isRunAndStart))
	with open(configPath, "w+") as f:
		cfg.write(f)

def WriteLeiDian(path):
	print('write ',path)
	with open(GetFullPath('StartLeiDian.cmd'),'w') as f:
		cmdStr =("cd /d "+path+"\n\ndnconsole.exe launchex --index 0 --packagename com.bilibili.priconne\n\nexit")
		f.write(cmdStr)


def CallLeiDian():
	win32api.ShellExecute(0, 'open', GetFullPath('StartLeiDian.cmd'), '', '', 1)
def CallPy():
	win32api.ShellExecute(0, 'open',  GetFullPath('AutoPcr4.0.py'), '', '', 1)          # 运行程序

def StartPcr():
	if(isRunAndStart):
		CallLeiDian()
	CallPy()
# isJJC = True
#============GUI================
# sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
# [sg.Text('Enter something on Row 2'), sg.InputText()],
layout = [	[sg.Checkbox('竞技场',isJJC)],[sg.Checkbox('探索',isTansuo)],[sg.Checkbox('地下城',isDxc)],
			[sg.Checkbox('购买经验',isExp)],[sg.Checkbox('扭蛋',isNiuDan)],
			[sg.Text('雷电模拟器文件夹路径'), sg.InputText('D:\program files\LeiDian\LDPlayer4.0')],
			[sg.Button(StartRunName), sg.Button(RunName),sg.Button('保存路径'), ] ]

# Create the Window
window = sg.Window('Window Title', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
	event, values = window.read()
	if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
		print("close")
		os._exit(0)
		break
	SetCurConfig(values)
	if event == '保存路径':
		WriteLeiDian(values[5])
		SavaConfig(values)
	if ((event == StartRunName) | (event == RunName)):
		isRunAndStart = (event == StartRunName)
		print('Run ', isRunAndStart)
		SavaConfig(values)
		StartPcr()
