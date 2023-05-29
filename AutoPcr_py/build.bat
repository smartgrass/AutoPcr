@echo off

echo. 建立临时文件夹

set pathDir=%~dp0

echo %pathDir%

cd /d %pathDir%

md TMP
md TMP\dxc\
md TMP\dxc_ex3\
md TMP\jjc\
md TMP\main\
md TMP\other\
md TMP\shop\
md TMP\tansuo\
md TMP\task\

echo. 复制资源
XCOPY  .\AutoPcr4.0.py .\TMP\ /Y
XCOPY  .\AutoPcr4.0_GUI.py .\TMP\ /Y
XCOPY  .\AutoPcr4.0_GUI.spec .\TMP\ /Y
XCOPY  .\AutoPcr4.0.spec .\TMP\ /Y
XCOPY  .\config.ini .\TMP\ /Y
XCOPY  .\运行说明\模拟器配置 .\TMP\运行说明\ /q /e /r /S /Y

XCOPY  .\运行说明\其他说明(可跳过) .\TMP\其他说明(可跳过)\ /q /e /r /S /Y

XCOPY  .\dxc .\TMP\dxc\ /q /e /r /S /Y
XCOPY  .\jjc .\TMP\jjc\ /q /e /r /S /Y
XCOPY  .\main .\TMP\main\ /q /e /r /S /Y
XCOPY  .\other .\TMP\other\ /q /e /r /S /Y
XCOPY  .\shop .\TMP\shop\ /q /e /r /S /Y
XCOPY  .\tansuo .\TMP\tansuo\ /q /e /r /S /Y
XCOPY  .\task .\TMP\task\ /q /e /r /S /Y

echo. 打包cmd

cd .\TMP

echo %cd%

pyinstaller  .\AutoPcr4.0.spec
MOVE .\dist\AutoPcrCmd.exe .\

echo. 打包exe
pyinstaller   .\AutoPcr4.0_GUI.spec
MOVE .\dist\AutoPcr.exe .\


echo. 打包zip
rd /s /q .\build
rd /s /q .\dist
del .\AutoPcr4.0_GUI.spec
del .\AutoPcr4.0_GUI.py
del .\AutoPcr4.0.spec
del .\AutoPcr4.0.py

cd ..
python -m zipfile -c AutoPcr.zip .\TMP\AutoPcr.exe .\TMP\AutoPcrCmd.exe  .\TMP\config.ini .\TMP\com.bilibili.priconne_960x540.kmp .\TMP\com.android.launcher3.smp .\TMP\com.bilibili.priconne.smp .\TMP\dxc\ .\TMP\jjc\ .\TMP\main\ .\TMP\other\ .\TMP\shop\ .\TMP\tansuo\ .\TMP\task\ .\TMP\运行说明\ .\TMP\其他说明(可跳过)

echo. 删除临时文件夹
rd /s /q .\TMP

timeout \t 60