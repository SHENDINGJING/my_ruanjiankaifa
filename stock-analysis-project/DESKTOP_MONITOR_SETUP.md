# 🖥️ 桌面炒股软件监控系统 - 安装与设置指南

## 🎯 系统概述

这个系统可以直接监控您电脑桌面上炒股软件的实时显示，通过屏幕截图和OCR识别技术，实现真正的"所见即所得"监控。

## 📋 系统功能

### ✅ 核心功能
1. **屏幕区域监控**：指定监控炒股软件的特定区域
2. **OCR识别**：自动识别股票价格、涨跌幅、成交量
3. **实时分析**：基于您的交易策略分析当前状态
4. **智能提醒**：发现交易机会或风险时立即提醒
5. **自动截图**：定时截图保存历史记录

### ✅ 支持软件
- **同花顺** ✓
- **东方财富** ✓  
- **大智慧** ✓
- **通达信** ✓
- **其他炒股软件** ✓（需要简单配置）

### ✅ 监控内容
- 股票当前价格
- 涨跌幅百分比
- 成交量变化
- 买卖盘口（可选）
- 技术指标（可选）

## 🔧 安装步骤

### 第一步：安装Python依赖

```bash
# 基础依赖
pip install pillow schedule

# 截图库（选择一种）
pip install pyautogui      # 简单易用
# 或
pip install mss            # 性能更好
# 或
pip install pyscreenshot   # 跨平台

# OCR识别（必须）
pip install pytesseract

# 还需要安装Tesseract OCR引擎
```

### 第二步：安装Tesseract OCR

#### Windows系统：
1. 下载安装包：https://github.com/UB-Mannheim/tesseract/wiki
2. 安装时勾选中文语言包
3. 添加到系统PATH

#### 验证安装：
```bash
tesseract --version
# 应该显示版本信息和语言支持
```

### 第三步：安装中文语言包
```bash
# 下载中文语言数据
# 或通过Tesseract安装程序安装

# 验证中文支持
tesseract --list-langs
# 应该包含 chi_sim（简体中文）
```

## 🚀 快速开始

### 1. 设置监控区域

```bash
# 设置同花顺软件的监控区域
python desktop_monitor.py --setup 同花顺,中国石油区域
```

**操作流程：**
1. 打开您的炒股软件（如同花顺）
2. 找到中国石油的显示区域
3. 按照提示记录区域坐标
4. 系统会保存这个区域配置

### 2. 添加监控股票

```bash
# 添加中国石油到监控
python desktop_monitor.py --add-stock 601857,中国石油,800,12.465
```

### 3. 测试监控

```bash
# 立即测试一次
python desktop_monitor.py --check

# 应该看到类似输出：
# 📸 已截取区域: 同花顺_601857 -> screenshots/...
# 📊 中国石油 (601857)
#    当前价: 12.160元
#    成本价: 12.465元
#    盈亏: -2.45% (亏损)
#    💡 建议: 持有
```

### 4. 开始实时监控

```bash
# 开始每30秒监控一次
python desktop_monitor.py --monitor --interval 30

# 监控期间会：
# 1. 每30秒截图一次指定区域
# 2. OCR识别价格信息
# 3. 分析并显示结果
# 4. 按Ctrl+C停止
```

## ⚙️ 详细配置

### 配置文件：`desktop_config.json`

```json
{
  "monitor_settings": {
    "screenshot_interval": 30,
    "monitor_regions": {
      "同花顺_601857": [100, 100, 200, 100]
    },
    "alert_thresholds": {
      "price_change_percent": 1.0,
      "volume_spike_percent": 50.0
    }
  },
  "monitored_stocks": [
    {
      "symbol": "601857",
      "name": "中国石油",
      "user_data": {
        "shares": 800,
        "cost_price": 12.465,
        "stop_loss": 11.592,
        "first_target": 14.335
      },
      "monitor_region": "同花顺_601857"
    }
  ]
}
```

### 区域坐标说明
- `[x, y, width, height]`
- x, y: 区域左上角坐标
- width, height: 区域宽度和高度
- 单位：像素

## 🖼️ 如何选择监控区域

### 最佳实践：
1. **价格显示区域**：包含当前价、涨跌幅
2. **大小适中**：200x100像素左右
3. **避免干扰**：不要包含太多无关信息
4. **固定位置**：确保软件窗口位置固定

### 区域示例：
```
同花顺软件：
┌─────────────────┐
│ 中国石油 601857 │ ← 包含这个区域
│ 12.16 -0.25(-2%)│
│ 成交量: 45.2万手│
└─────────────────┘
```

## 🔍 OCR识别优化

### 提高识别准确率：
1. **清晰截图**：确保区域清晰无模糊
2. **合适大小**：文字不能太小
3. **高对比度**：文字与背景对比明显
4. **简单背景**：避免复杂背景干扰

### 识别配置：
```python
# 在代码中可以调整OCR参数
import pytesseract

# 设置中文识别
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 识别配置
config = '--psm 6 -l chi_sim'  # 页面分割模式6，简体中文
text = pytesseract.image_to_string(image, config=config)
```

## 📊 监控输出示例

### 正常监控：
```
⏰ 14:30:15 检查...
📸 已截取区域: 同花顺_601857
📊 中国石油 (601857)
   当前价: 12.180元
   成本价: 12.465元
   盈亏: -2.29% (亏损)
   距止损: +5.1%
   距目标: +17.7%
   💡 建议: 持有
```

### 紧急提醒：
```
🚨 紧急提醒！
中国石油跌破止损价！
当前价: 11.550元 ≤ 止损价: 11.592元
建议: 立即卖出全部800股
```

### 目标达成：
```
🎯 达到盈利目标！
中国石油达到第一目标价！
当前价: 14.350元 ≥ 目标价: 14.335元
建议: 卖出50%锁定利润
```

## 🛠️ 故障排除

### 常见问题1：OCR识别失败
**症状**：识别不出价格或识别错误
**解决**：
1. 调整监控区域大小和位置
2. 检查Tesseract中文包是否安装
3. 增加截图延迟，确保页面加载完成
4. 调整OCR参数（--psm模式）

### 常见问题2：截图区域不对
**症状**：截图内容不是预期的股票信息
**解决**：
1. 重新设置监控区域
2. 确保软件窗口位置固定
3. 检查屏幕分辨率是否变化
4. 使用窗口标题定位而非坐标

### 常见问题3：性能问题
**症状**：监控卡顿或延迟
**解决**：
1. 增加监控间隔（如60秒）
2. 缩小监控区域
3. 关闭不必要的监控股票
4. 优化OCR识别参数

## 🔄 与之前系统的集成

### 可以同时使用：
1. **桌面监控**：实时监控您看到的界面
2. **API监控**：通过Yahoo Finance获取数据
3. **策略分析**：使用trading_strategy.py分析
4. **每日复盘**：使用daily_review.py复盘

### 集成示例：
```bash
# 桌面实时监控
python desktop_monitor.py --monitor --interval 30

# 同时使用API数据验证
python stock_monitor.py --check

# 收盘后生成综合报告
python daily_review.py --report
```

## 📈 高级功能

### 1. 多区域监控
```bash
# 监控多个区域
python desktop_monitor.py --setup 同花顺,价格区域
python desktop_monitor.py --setup 同花顺,成交量区域
python desktop_monitor.py --setup 同花顺,买卖盘区域
```

### 2. 自定义识别规则
```json
{
  "recognition_rules": {
    "price_pattern": "\\d+\\.\\d+",
    "change_pattern": "[+-]\\d+\\.\\d+%",
    "volume_pattern": "\\d+(\\.\\d+)?[万千]手"
  }
}
```

### 3. 智能预警
- 价格异常波动预警
- 成交量突增预警
- 买卖盘口异常预警
- 技术指标背离预警

## 🎯 使用建议

### 最佳实践：
1. **先测试后使用**：先用模拟数据测试
2. **小范围开始**：先监控1-2只股票
3. **定期校准**：每周检查区域是否准确
4. **备份配置**：定期备份desktop_config.json

### 风险控制：
1. **双重验证**：重要决策前用API数据验证
2. **人工确认**：自动提醒后仍需人工确认
3. **设置上限**：监控股票数量不超过10只
4. **定期检查**：每天检查系统是否正常工作

## 🏁 立即开始

### 完整流程：
```bash
# 1. 安装依赖
pip install pillow pyautogui pytesseract schedule

# 2. 安装Tesseract OCR（手动）

# 3. 设置监控区域
python desktop_monitor.py --setup 同花顺,中国石油区域

# 4. 添加股票
python desktop_monitor.py --add-stock 601857,中国石油,800,12.465

# 5. 测试
python desktop_monitor.py --check

# 6. 开始监控
python desktop_monitor.py --monitor --interval 30
```

### 验证安装：
```python
# 测试OCR识别
import pytesseract
from PIL import Image
import pyautogui

# 截图测试
screenshot = pyautogui.screenshot()
screenshot.save('test.png')

# OCR识别测试
text = pytesseract.image_to_string('test.png', lang='chi_sim')
print(f"识别结果: {text}")
```

## 📞 技术支持

### 遇到问题？
1. **查看日志**：`logs/desktop_monitor_*.log`
2. **检查截图**：`screenshots/` 目录
3. **测试OCR**：运行上面的验证脚本
4. **检查配置**：`desktop_config.json`

### 需要帮助？
1. OCR识别问题：检查Tesseract安装和语言包
2. 截图问题：调整区域坐标或使用其他截图库
3. 性能问题：增加监控间隔或优化识别参数
4. 其他问题：提供错误信息和截图

---

**重要提示**：这个系统是辅助工具，不能替代您的判断。任何投资决策都需要您自己的分析和风险控制。

**开始您的桌面监控之旅吧！** 🚀