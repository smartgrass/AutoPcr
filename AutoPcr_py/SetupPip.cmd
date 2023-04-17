%1 start "" mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c %~s0 ::","","runas",1)(window.close)&&exit

python.exe -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip

pip install -i https://pypi.tuna.tsinghua.edu.cn/simple opencv-python

pip install -i https://pypi.tuna.tsinghua.edu.cn/simple aircv

pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pyautogui

pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pillow

pip install -i https://pypi.tuna.tsinghua.edu.cn/simple keyboard

pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pypiwin32

pip install -i https://pypi.tuna.tsinghua.edu.cn/simple PySimpleGUI

@echo off

if %errorlevel% == 0 ( echo successfully ) else ( 

echo failed Ê§°Ü,ÖØÐÂ³¢ÊÔ SetupPip_1

start %~dp0/SetupPip_1.cmd

)

pause