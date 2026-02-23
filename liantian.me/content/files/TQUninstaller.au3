#RequireAdmin
#Region ;**** Directives created by AutoIt3Wrapper_GUI ****
#AutoIt3Wrapper_Icon=favicon.ico
#AutoIt3Wrapper_UseUpx=y
#AutoIt3Wrapper_Res_Description=天擎卸载工具
#AutoIt3Wrapper_Res_Fileversion=6.7.0.3
#AutoIt3Wrapper_Res_Fileversion_AutoIncrement=y
#AutoIt3Wrapper_Res_ProductName=TQUninstaller
#AutoIt3Wrapper_Res_ProductVersion=6.7.0
#AutoIt3Wrapper_Res_CompanyName=liantian-cn
#AutoIt3Wrapper_Res_LegalCopyright=https://liantian.me/
#AutoIt3Wrapper_Res_Language=2052
#EndRegion ;**** Directives created by AutoIt3Wrapper_GUI ****
#cs ----------------------------------------------------------------------------

 AutoIt Version: 3.3.16.0
 Author:         myName

 Script Function:
	Template AutoIt script.

#ce ----------------------------------------------------------------------------

; Script Start - Add your code below here
#include <FileConstants.au3>
#include <MsgBoxConstants.au3>



Func GetDir($sFilePath)

    Local $aFolders = StringSplit($sFilePath, "\")
    Local $iArrayFoldersSize = UBound($aFolders)
    Local $FileDir = ""

    If (Not IsString($sFilePath)) Then
        Return SetError(1, 0, -1)
    EndIf

    $aFolders = StringSplit($sFilePath, "\")
    $iArrayFoldersSize = UBound($aFolders)

    For $i = 1 To ($iArrayFoldersSize - 2)
        $FileDir &= $aFolders[$i] & "\"
    Next

    Return $FileDir

EndFunc   ;==>GetDir

MsgBox($MB_SYSTEMMODAL, "提示", "选择360EntClient.exe所在路径。", 10)

Local Const $sMessage = "选择360EntClient.exe所在路径"

Local $sFileOpenDialog = FileOpenDialog($sMessage, @ProgramFilesDir & "\", "360EntClient (360EntClient.exe)", $FD_FILEMUSTEXIST)


If @error Then
	MsgBox($MB_SYSTEMMODAL, "", "没有选择的正确，程序退出")
	Exit
EndIf

Local $sFileDirPath = GetDir($sFileOpenDialog)
FileChangeDir($sFileDirPath)

Local $sTrayPath  = $sFileDirPath & "safemon\360tray.exe"

Run($sTrayPath & " /disablesp" ,$sFileDirPath & "safemon\")

Local $hWnd = WinWait("[TITLE:奇安信天擎]", "", 10)

If @error Then
	MsgBox($MB_SYSTEMMODAL, "提示", "请手动关闭保护模式，然后确定。")
Else
	ControlClick($hWnd,"","[CLASS:Button; INSTANCE:2]")
EndIf

Local $sIniPath  = $sFileDirPath & "EntClient\conf\EntBase.dat"

IniWrite($sIniPath, "protect", "uipass", "")
IniWrite($sIniPath, "protect", "qtpass", "")
IniDelete ($sIniPath, "protect", "uienable ")
IniDelete ($sIniPath, "protect", "qtenable")
IniDelete ($sIniPath, "protect", "uimode")
IniDelete ($sIniPath, "protect", "qtmode")
IniDelete ($sIniPath, "protect", "ui_encrypt_type")
IniDelete ($sIniPath, "protect", "qt_encrypt_type")

Run($sFileDirPath & "uninst.exe",$sFileDirPath)

