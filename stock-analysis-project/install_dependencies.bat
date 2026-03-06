@echo off
echo ========================================
echo  桌面炒股软件监控系统 - 依赖安装脚本
echo ========================================
echo.

echo [1/5] 检查Python环境...
python --version
if errorlevel 1 (
    echo ❌ Python未安装或不在PATH中
    echo 请先安装Python 3.8+ 并添加到系统PATH
    pause
    exit /b 1
)

echo ✅ Python环境正常
echo.

echo [2/5] 安装Python基础依赖...
pip install pillow schedule
if errorlevel 1 (
    echo ❌ 依赖安装失败
    pause
    exit /b 1
)

echo ✅ 基础依赖安装完成
echo.

echo [3/5] 选择截图库（三选一）...
echo 1. pyautogui (简单易用，推荐)
echo 2. mss (性能更好)
echo 3. pyscreenshot (跨平台)
echo.
set /p choice="请选择截图库 (1/2/3, 默认1): "
if "%choice%"=="1" (
    echo 安装 pyautogui...
    pip install pyautogui
) else if "%choice%"=="2" (
    echo 安装 mss...
    pip install mss
) else if "%choice%"=="3" (
    echo 安装 pyscreenshot...
    pip install pyscreenshot
) else (
    echo 安装 pyautogui (默认)...
    pip install pyautogui
)

if errorlevel 1 (
    echo ❌ 截图库安装失败
    pause
    exit /b 1
)

echo ✅ 截图库安装完成
echo.

echo [4/5] 安装OCR识别库...
pip install pytesseract
if errorlevel 1 (
    echo ❌ pytesseract安装失败
    pause
    exit /b 1
)

echo ✅ OCR库安装完成
echo.

echo [5/5] 安装Tesseract OCR引擎...
echo.
echo ⚠️  重要：需要手动安装Tesseract OCR
echo.
echo 安装步骤：
echo 1. 下载地址：https://github.com/UB-Mannheim/tesseract/wiki
echo 2. 下载最新版本（如 tesseract-ocr-w64-setup-5.3.3.20231005.exe）
echo 3. 运行安装程序
echo 4. 安装时务必勾选中文语言包
echo 5. 记住安装路径（如 C:\Program Files\Tesseract-OCR）
echo.
echo 安装完成后，需要：
echo 1. 将Tesseract添加到系统PATH
echo 2. 或修改代码中的tesseract_cmd路径
echo.
pause

echo ========================================
echo  依赖安装完成！
echo ========================================
echo.
echo 下一步：
echo 1. 完成Tesseract OCR安装
echo 2. 运行测试：python test_ocr.py
echo 3. 设置监控区域：python desktop_monitor.py --setup
echo.
pause