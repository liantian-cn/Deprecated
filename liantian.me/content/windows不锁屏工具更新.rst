windows不锁屏工具更新
######################

:Title: windows不锁屏工具更新
:Date: 2022-08-01
:Modified: 2022-08-01
:tags: Windows
:Slug: keepawake
:Summary: 用autoit做了一个不锁屏工具....autoit真是一个被错过的好东西。

::

   #include <Timers.au3>

   Func _PowerKeepAlive()
       Local $aRet=DllCall('kernel32.dll','long','SetThreadExecutionState','long',0x80000003)
       If @error Then Return SetError(2,@error,0x80000000)
       Return $aRet[0]
   EndFunc

   Func _PowerResetState()
       Local $aRet=DllCall('kernel32.dll','long','SetThreadExecutionState','long',0x80000000)
       If @error Then Return SetError(2,@error,0x80000000)
       Return $aRet[0]    ; Previous state
   EndFunc


   _PowerKeepAlive()
   OnAutoItExitRegister("_PowerResetState")

   Opt("TrayOnEventMode", 0)
   Opt("TrayMenuMode", 1+2)
   TraySetClick(8+1)
   TraySetToolTip("不锁屏工具")

   Local $iTrayExit = TrayCreateItem("退出，并不再阻止锁屏。")

   TraySetState()

   Local $hStarttime = _Timer_Init()

   While 1
       IF TrayGetMsg() = $iTrayExit Then Exit

       if _Timer_Diff($hStarttime) > 1000 * 5 Then
           $pos = MouseGetPos()
           MouseMove($pos[0]+Random(-1,1,1),$pos[1]+Random(-1,1,1))
           $hStarttime = _Timer_Init()
       EndIf

   WEnd
