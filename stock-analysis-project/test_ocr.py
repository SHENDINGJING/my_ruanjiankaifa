#!/usr/bin/env python3
"""
OCR识别测试脚本
测试Tesseract OCR是否正常工作
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont
import tempfile

def test_basic_ocr():
    """测试基本OCR功能"""
    print("🧪 测试OCR识别功能...")
    
    try:
        import pytesseract
        
        # 检查Tesseract路径
        tesseract_cmd = None
        
        # 常见安装路径
        possible_paths = [
            r'C:\Program Files\Tesseract-OCR\tesseract.exe',
            r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
            r'D:\Program Files\Tesseract-OCR\tesseract.exe',
            '/usr/bin/tesseract',  # Linux/Mac
            '/usr/local/bin/tesseract'
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                tesseract_cmd = path
                print(f"✅ 找到Tesseract: {path}")
                pytesseract.pytesseract.tesseract_cmd = path
                break
        
        if not tesseract_cmd:
            print("❌ 未找到Tesseract，请检查安装")
            print("   尝试在PATH中查找...")
            try:
                # 尝试使用PATH中的tesseract
                pytesseract.get_tesseract_version()
                print("✅ 在PATH中找到Tesseract")
            except:
                print("❌ PATH中也没有Tesseract")
                print("\n💡 解决方案:")
                print("1. 安装Tesseract OCR")
                print("2. 设置环境变量PATH")
                print("3. 或在代码中指定路径:")
                print('   pytesseract.pytesseract.tesseract_cmd = r"C:\\路径\\tesseract.exe"')
                return False
        
        # 创建测试图片
        print("\n🖼️ 创建测试图片...")
        img = Image.new('RGB', (300, 100), color='white')
        draw = ImageDraw.Draw(img)
        
        try:
            # 尝试使用系统字体
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            # 使用默认字体
            font = ImageFont.load_default()
        
        # 绘制测试文字
        test_text = "中国石油 12.16 -2.45%"
        draw.text((10, 10), test_text, fill='black', font=font)
        
        # 保存测试图片
        test_file = "test_ocr_image.png"
        img.save(test_file)
        print(f"✅ 测试图片已保存: {test_file}")
        
        # OCR识别测试
        print("\n🔍 开始OCR识别...")
        
        # 测试英文识别
        print("测试英文识别...")
        try:
            text = pytesseract.image_to_string(img, lang='eng')
            print(f"英文识别结果: {text.strip()}")
        except Exception as e:
            print(f"英文识别失败: {e}")
        
        # 测试中文识别
        print("\n测试中文识别...")
        try:
            text = pytesseract.image_to_string(img, lang='chi_sim')
            print(f"中文识别结果: {text.strip()}")
        except Exception as e:
            print(f"中文识别失败: {e}")
            print("\n💡 可能原因:")
            print("1. 未安装中文语言包")
            print("2. 语言包路径不正确")
            print("3. Tesseract版本问题")
        
        # 列出支持的语言
        print("\n🌐 检查支持的语言...")
        try:
            langs = pytesseract.get_languages()
            print(f"支持的语言: {langs}")
            
            if 'chi_sim' in langs:
                print("✅ 支持简体中文")
            else:
                print("❌ 不支持简体中文，需要安装语言包")
        except:
            print("无法获取语言列表")
        
        return True
        
    except ImportError as e:
        print(f"❌ 导入pytesseract失败: {e}")
        print("\n💡 请安装: pip install pytesseract")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_screenshot():
    """测试截图功能"""
    print("\n📸 测试截图功能...")
    
    # 测试不同的截图库
    screenshot_libs = ['pyautogui', 'mss', 'pyscreenshot']
    
    for lib_name in screenshot_libs:
        try:
            if lib_name == 'pyautogui':
                import pyautogui
                print("测试pyautogui截图...")
                screenshot = pyautogui.screenshot()
                screenshot.save('test_screenshot_pyautogui.png')
                print(f"✅ pyautogui截图成功: {screenshot.size}")
                return True
                
            elif lib_name == 'mss':
                import mss
                print("测试mss截图...")
                with mss.mss() as sct:
                    monitor = sct.monitors[1]  # 主显示器
                    screenshot = sct.grab(monitor)
                    mss.tools.to_png(screenshot.rgb, screenshot.size, output='test_screenshot_mss.png')
                    print(f"✅ mss截图成功: {screenshot.size}")
                    return True
                    
            elif lib_name == 'pyscreenshot':
                import pyscreenshot as ImageGrab
                print("测试pyscreenshot截图...")
                screenshot = ImageGrab.grab()
                screenshot.save('test_screenshot_pyscreenshot.png')
                print(f"✅ pyscreenshot截图成功: {screenshot.size}")
                return True
                
        except ImportError:
            print(f"  {lib_name} 未安装")
        except Exception as e:
            print(f"  {lib_name} 失败: {e}")
    
    print("❌ 所有截图库测试失败")
    return False

def main():
    """主测试函数"""
    print("=" * 60)
    print("桌面监控系统 - OCR和截图功能测试")
    print("=" * 60)
    
    # 测试OCR
    ocr_ok = test_basic_ocr()
    
    # 测试截图
    screenshot_ok = test_screenshot()
    
    print("\n" + "=" * 60)
    print("测试结果汇总:")
    print("=" * 60)
    
    if ocr_ok:
        print("✅ OCR功能: 正常")
    else:
        print("❌ OCR功能: 需要修复")
    
    if screenshot_ok:
        print("✅ 截图功能: 正常")
    else:
        print("❌ 截图功能: 需要修复")
    
    print("\n下一步:")
    if ocr_ok and screenshot_ok:
        print("🎉 所有功能正常，可以开始使用桌面监控系统!")
        print("   运行: python desktop_monitor.py --setup")
    else:
        print("🔧 需要修复的问题:")
        if not ocr_ok:
            print("  1. 安装或配置Tesseract OCR")
            print("  2. 安装中文语言包")
        if not screenshot_ok:
            print("  1. 安装截图库: pip install pyautogui")
            print("  2. 或选择其他截图库")
    
    print("\n测试文件:")
    if os.path.exists("test_ocr_image.png"):
        print("  test_ocr_image.png - OCR测试图片")
    if os.path.exists("test_screenshot_pyautogui.png"):
        print("  test_screenshot_pyautogui.png - 截图测试")
    
    print("\n按Enter退出...")
    input()

if __name__ == "__main__":
    main()