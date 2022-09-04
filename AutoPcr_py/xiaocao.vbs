Dim fso
Set fso = CreateObject("Scripting.FileSystemObject")
StrCurPath = fso.GetFolder(".")
Set WshShell = WScript.CreateObject("WScript.Shell")
strDesktop = WshShell.SpecialFolders("Desktop")
set oShellLink = WshShell.CreateShortcut(StrCurPath & "/AutoPcr4.0_GUI快捷方式.lnk")
oShellLink.TargetPath = StrCurPath+"\AutoPcr4.0_GUI.py"
oShellLink.WindowStyle = 1
oShellLink.Hotkey = "Ctrl+Alt+e"
oShellLink.IconLocation = StrCurPath+"\other\icon.ico, 0"
oShellLink.Description = "快捷方式"
oShellLink.WorkingDirectory = StrCurPath
oShellLink.Save