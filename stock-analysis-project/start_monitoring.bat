@echo off
echo ========================================
echo  OpenClaw股票实时监控系统 - 一键启动
echo ========================================
echo.

echo [1/4] 检查Python环境...
python --version
if errorlevel 1 (
    echo ❌ Python未安装
    echo 请先安装Python 3.8+
    pause
    exit /b 1
)

echo ✅ Python环境正常
echo.

echo [2/4] 检查OpenClaw Gateway...
openclaw gateway status > nul 2>&1
if errorlevel 1 (
    echo ⚠️  Gateway未运行，正在启动...
    start /B openclaw gateway start
    timeout /t 5 /nobreak > nul
    echo ✅ Gateway启动完成
) else (
    echo ✅ Gateway已在运行
)

echo.

echo [3/4] 添加中国石油到监控...
python openclaw_screen_monitor.py --add-stock "601857,中国石油,800,12.465"
if errorlevel 1 (
    echo ⚠️  添加股票失败，可能已存在
)

echo.

echo [4/4] 启动实时监控...
echo.
echo 📊 监控信息：
echo    股票：中国石油 (601857)
echo    成本：12.465元
echo    股数：800股
echo    间隔：30秒
echo.
echo 🎯 监控内容：
echo    1. 价格变化监控
echo    2. 7%止损监控
echo    3. 15%止盈监控
echo    4. 风险收益比计算
echo.
echo ⚠️  按 Ctrl+C 停止监控
echo.

python openclaw_screen_monitor.py --monitor --interval 30

echo.
echo ========================================
echo  监控已停止
echo ========================================
echo.
echo 📋 下一步操作：
echo    1. 查看日志：type logs\openclaw_monitor\*.log
echo    2. 查看截图：dir screen_recordings\
echo    3. 重新启动：运行本脚本
echo.
pause