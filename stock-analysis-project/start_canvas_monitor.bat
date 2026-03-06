@echo off
echo ========================================
echo  OpenClaw Canvas监控系统 - 一键启动
echo ========================================
echo.

echo [1/5] 检查Python环境...
python --version
if errorlevel 1 (
    echo ❌ Python未安装
    echo 请先安装Python 3.8+
    pause
    exit /b 1
)

echo ✅ Python环境正常
echo.

echo [2/5] 检查OpenClaw Gateway...
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

echo [3/5] 检查节点状态...
python canvas_monitor.py --nodes
if errorlevel 1 (
    echo ⚠️  节点检查失败
    echo.
    echo 📱 需要先配对节点设备：
    echo 1. 在手机/平板安装OpenClaw Node应用
    echo 2. 在本机运行: openclaw nodes pending
    echo 3. 批准配对: openclaw nodes approve ^<请求ID^>
    echo.
    pause
    exit /b 1
)

echo.

echo [4/5] 添加中国石油到监控...
python canvas_monitor.py --add-stock "601857,中国石油,800,12.465"
if errorlevel 1 (
    echo ⚠️  添加股票失败，可能已存在
)

echo.

echo [5/5] 启动Canvas实时监控...
echo.
echo 🎨 监控信息：
echo    方案：Canvas画布监控（方案3）
echo    股票：中国石油 (601857)
echo    成本：12.465元
echo    股数：800股
echo    间隔：30秒
echo.
echo 📱 设备要求：
echo    1. 已配对的iOS/Android设备
echo    2. 设备在前台运行
echo    3. 稳定的网络连接
echo.
echo 🎯 监控内容：
echo    1. Canvas实时监控界面
echo    2. 定期快照捕获
echo    3. 智能策略分析
echo    4. 风险预警提醒
echo.
echo ⚠️  按 Ctrl+C 停止监控
echo.

python canvas_monitor.py --monitor --interval 30

echo.
echo ========================================
echo  Canvas监控已停止
echo ========================================
echo.
echo 📋 下一步操作：
echo    1. 查看快照：dir canvas_screenshots\
echo    2. 查看日志：type logs\canvas\*.log
echo    3. 查看界面：canvas\index.html
echo    4. 重新启动：运行本脚本
echo.
pause