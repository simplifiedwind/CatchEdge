@echo off
rem 双击即可启动 CatchEdge，不依赖当前目录。
rem 用 pythonw 启动不会弹黑窗口；出错会写进 output\ui_error.log

set "PYTHONW=C:\Users\xukaiguo\miniconda3\envs\CatchEdge\pythonw.exe"

if not exist "%PYTHONW%" (
    echo 找不到 Python 环境：
    echo   %PYTHONW%
    echo 请确认 conda 环境 CatchEdge 还在，或修改本文件里的路径。
    pause
    exit /b 1
)

start "" "%PYTHONW%" "%~dp0ui.py"
