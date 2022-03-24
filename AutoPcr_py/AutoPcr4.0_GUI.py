
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
mnqIndexKey ='mnqDrop'
dxcDropKey ='dxcDrop'
dxcDropValue =["炸脖龙","绿龙"]
mnqIndexDropValue=["1","0"]


cfg = ConfigParser()
configPath = GetFullPath('config.ini')
cfg.read(configPath,'utf-8')
mnqIndex = cfg.get('MainSetting',mnqIndexKey)
MainSettingKey='MainSetting_'+mnqIndex

def SetConfigAuto(key,AllValues):
	SetConfig(key,str(AllValues[key]))

def SetConfig(key,value):
	cfg.set(MainSettingKey,key,value)

def ReadStrConfig(key):
	window[key].Update(GetStrConfig(key))
def ReadBoolConfig(key):
	window[key].Update(GetBoolConfig(key))

def GetStrConfig(key):
	return cfg.get(MainSettingKey,key)

def GetBoolConfig(boolKey):
	return Boolean(cfg.get(MainSettingKey,boolKey)=='True')

def SetCurMnqIndex():
	cfg.set('MainSetting',mnqIndexKey,mnqIndex)
def SetMnqDir():
	print(LeiDianDir)
	cfg.set('MainSetting',LeiDianDirKey,LeiDianDir)
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
isXinSui =GetBoolConfig(isXinSuiKey)
isXQB = GetBoolConfig(isXQBKey)
isSend = GetBoolConfig(isSendKey)
isNeedSeed= GetBoolConfig(isNeedSeedKey)
isRunAndStart = False

isHomeTake= GetBoolConfig(isHomeTakeKey)
isHouDongHard=GetBoolConfig(isHouDongHardKey)
isUseAllPower=GetBoolConfig(isUseAllPowerKey)


LeiDianDir = cfg.get('MainSetting',LeiDianDirKey)
dxcBoss=GetStrConfig(dxcDropKey)
needZbName = GetStrConfig(needZbNameKey)

#new
DxcDuiWu ='1,2,3'
isAllSelectKey_1 = 'isAllSelect_1'
isAllSelectKey_2 = 'isAllSelect_2'
isAllSelect1 = False
isAllSelect2= False


#保存配置
def SavaConfig(AllValues):
	RunTimeValue()
	SetConfigAuto(isJJCKey,AllValues)
	SetConfigAuto(isTansuoKey,AllValues)
	SetConfigAuto(isDxcKey,AllValues)
	SetConfigAuto(isExpKey,AllValues)
	SetConfigAuto(isNiuDanKey,AllValues)
	SetConfigAuto(isRunAndStartKey,AllValues)

	#new
	SetConfigAuto(isXQBKey,AllValues)
	SetConfigAuto(isXinSuiKey,AllValues)
	SetConfigAuto(isKillBossKey,AllValues)
	SetConfigAuto(isSendKey,AllValues)
	SetConfigAuto(isNeedSeedKey,AllValues)
	SetConfigAuto(dxcDropKey,AllValues)

	SetConfigAuto(isHomeTakeKey,AllValues)
	SetConfigAuto(isUseAllPowerKey,AllValues)
	SetConfigAuto(isHouDongHardKey,AllValues)

	SetConfigAuto(needZbNameKey,AllValues)
	# SetConfigAuto(LeiDianDirKey,AllValues)
	global LeiDianDir
	LeiDianDir = AllValues[LeiDianDirKey]
	SetCurMnqIndex()
	SetMnqDir()

	with open(configPath, "w+",encoding='utf-8') as f:
		cfg.write(f)
def ReadConfig():
	RunTimeValue()
	ReadBoolConfig(isJJCKey)
	ReadBoolConfig(isTansuoKey)
	ReadBoolConfig(isDxcKey)
	ReadBoolConfig(isExpKey)
	ReadBoolConfig(isNiuDanKey)
	ReadBoolConfig(isRunAndStartKey)
	#new
	ReadBoolConfig(isXQBKey)
	ReadBoolConfig(isXinSuiKey)
	ReadBoolConfig(isKillBossKey)
	ReadBoolConfig(isSendKey)
	ReadBoolConfig(isNeedSeedKey)
	ReadBoolConfig(isHomeTakeKey)
	ReadBoolConfig(isUseAllPowerKey)
	ReadBoolConfig(isHouDongHardKey)

	ReadStrConfig(dxcDropKey)
	ReadStrConfig(needZbNameKey)
	# ReadStrConfig(mnqIndexKey,AllValues)


def WriteCmds():
	path = str(LeiDianDir)
	index = str(mnqIndex)
	WriteLeiDian(path,index)
	# WirteStartPy()

def WriteLeiDian(path,index):
	print('write ',path,'StartLeiDian.cmd')
	fileName = 'StartLeiDian.cmd'
	if(index == '1'):
		fileName = 'StartLeiDian1.cmd'
	with open(GetFullPath(fileName),'w') as f:
		cmdStr =("cd /d "+path+"\n\ndnconsole.exe launchex --index "+index+" --packagename com.bilibili.priconne\n\nexit")
		f.write(cmdStr)

# def WirteStartPy():
# 	with open(GetFullPath('StartPy.cmd'),'w') as f:
# 		cmdStr =("python "+curDir+"\AutoPcr4.0.py\n\nexit")
# 		f.write(cmdStr)

# def WirteStart(path):
# 	with open(GetFullPath('start.cmd'),'w') as f:
# 		print('write ',path,'start.cmd')
# 		cmdStr  = "start call "+curDir+"\startPy.cmd\n\n"+"cd /d "+ path+"\n\ndnconsole.exe launchex --index 0 --packagename com.bilibili.priconne\n\nexit"
# 		f.write(cmdStr)

def CallLeiDian():
	index = str(mnqIndex)
	if(index=='0'):
		win32api.ShellExecute(0, 'open', GetFullPath('StartLeiDian.cmd'), '', '', 1)
	if(index=='1'):
		win32api.ShellExecute(0, 'open', GetFullPath('StartLeiDian1.cmd'), '', '', 1)
def CallPy():
	win32api.ShellExecute(0, 'open',  GetFullPath('AutoPcr4.0.py'), '', '', 1)          # 运行程序

def StartPcr():
	CallLeiDian()
	CallPy()


left_col = [
[sg.Text('日常功能'),sg.Checkbox('',isAllSelect1,key=isAllSelectKey_1,enable_events=True)],
[sg.Checkbox('竞技场',isJJC,key=isJJCKey),sg.Checkbox('探索',isTansuo,key=isTansuoKey),sg.Checkbox('地下城',isDxc,key=isDxcKey)],
[sg.Checkbox('购买经验',isExp,key=isExpKey),sg.Checkbox('扭蛋',isNiuDan,key=isNiuDanKey),sg.Checkbox('领取奖励',isHomeTake,key=isHomeTakeKey)],
[sg.Checkbox('星球杯',isXQB,key = isXQBKey),sg.Checkbox('请求捐赠',isNeedSeed,key=isNeedSeedKey)],
[sg.Text('次用功能'),sg.Checkbox('',isAllSelect2,key=isAllSelectKey_2,enable_events=True)],
[sg.Checkbox('活动困难本',isHouDongHard,key=isHouDongHardKey),sg.Checkbox('普通关卡清空所有体力',isUseAllPower,key=isUseAllPowerKey)],
[sg.Checkbox('赠送礼物',isSend,key=isSendKey),sg.Checkbox('心之碎片',isXinSui,key = isXinSuiKey)],

[sg.Text('雷电模拟器文件夹:')],
[sg.InputText(LeiDianDir,size =(35,None),key= LeiDianDirKey)],
[sg.Button('保存配置'), sg.Button(RunName), sg.Button(StartRunName),sg.Button('test')]]
right_col = [[sg.Text('其他配置                  ')],
[sg.Text('模拟器序号'),sg.DropDown(mnqIndexDropValue,mnqIndex,enable_events=True,size =(8,None),key =mnqIndexKey),
sg.Checkbox('启动模拟器',isRunAndStart,key=isRunAndStartKey)],
[sg.Text('地下城'),sg.DropDown(dxcDropValue, dxcBoss ,key=dxcDropKey,size=(20,None)),sg.Checkbox('击杀boss',isKillBoss,key=isKillBossKey)],
[sg.Text('求装备:other/zuanbei/'),sg.InputText(needZbName,size =(8,None),key= needZbNameKey),sg.Text('.png')],
# [sg.Text('绿龙队伍'),sg.InputText(DxcDuiWu,size=(35,None))],
]

layout = [
# [sg.Pane(
	[sg.Column(left_col, element_justification='l',  expand_x=True, expand_y=True), sg.Column(right_col, element_justification='l', expand_x=True, expand_y=True) ]
	# , orientation='h', relief=sg.RELIEF_SUNKEN, k='-PANE-')]
	]

# Create the Window
window = sg.Window('AutoPcr', layout)

def RunTimeValue():
	global isRunAndStart,mnqIndex,MainSettingKey
	isRunAndStart = values[isRunAndStartKey] #这个需要获取
	mnqIndex = values[mnqIndexKey]
	MainSettingKey='MainSetting_'+mnqIndex
	print('MainSettingKey = ',MainSettingKey)

def SetAllSelect1():
	window[isJJCKey].Update(isAllSelect1)
	window[isTansuoKey].Update(isAllSelect1)
	window[isDxcKey].Update(isAllSelect1)
	window[isExpKey].Update(isAllSelect1)
	window[isNiuDanKey].Update(isAllSelect1)
	window[isHomeTakeKey].Update(isAllSelect1)
	window[isNeedSeedKey].Update(isAllSelect1)
	window[isXQBKey].Update(isAllSelect1)
def SetAllSelect2():
	window[isSendKey].Update(isAllSelect2)
	window[isHouDongHardKey].Update(isAllSelect2)
	window[isUseAllPowerKey].Update(isAllSelect2)
	window[isXinSuiKey].Update(isAllSelect2)

# sg.popup_get_folder('Enter the file you wish to process')
# Event Loop to process "events" and get the "values" of the inputs
while True:
	event, values = window.read()
	print(event)
	if event == 'test':
		print("==============")
		print("Values = ",values["isJJC"])

	if event ==  isAllSelectKey_1:
		isAllSelect1 = bool(1-isAllSelect1)
		SetAllSelect1()
	if event ==  isAllSelectKey_2:
		isAllSelect2 = bool(1-isAllSelect2)
		SetAllSelect2()

	if event == mnqIndexKey:
		ReadConfig()

	if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
		print("close")
		os._exit(0)
		break
	if event == '保存配置':
		print('初始化配置')
		SavaConfig(values)
		WriteCmds()
	if ((event == RunName) | (event == StartRunName)):
		if(event == StartRunName):
			values[isRunAndStartKey] = True
		SavaConfig(values)
		StartPcr()
