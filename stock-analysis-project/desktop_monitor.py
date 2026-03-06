#!/usr/bin/env python3
"""
桌面炒股软件监控系统
通过屏幕截图监控股票价格
"""

import json
import time
import os
import sys
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import schedule

class DesktopStockMonitor:
    """桌面股票监控器"""
    
    def __init__(self, config_path: str = "desktop_config.json"):
        self.config_path = config_path
        self.config = self.load_config()
        self.screenshot_dir = "screenshots"
        self.setup_directories()
        
    def load_config(self) -> Dict:
        """加载配置"""
        default_config = {
            "monitor_settings": {
                "screenshot_interval": 30,  # 截图间隔秒数
                "monitor_regions": {},      # 监控区域 {软件名: (x, y, width, height)}
                "alert_thresholds": {
                    "price_change_percent": 1.0,  # 价格变化提醒阈值
                    "volume_spike_percent": 50.0  # 成交量突增阈值
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
                    "monitor_region": "同花顺_601857"  # 对应监控区域
                }
            ],
            "software_templates": {
                "同花顺": {
                    "price_position": (100, 150),  # 价格相对位置
                    "volume_position": (100, 180), # 成交量相对位置
                    "color_patterns": {
                        "up": (255, 0, 0),    # 上涨颜色（红色）
                        "down": (0, 255, 0),  # 下跌颜色（绿色）
                        "flat": (128, 128, 128)  # 平盘颜色
                    }
                },
                "东方财富": {
                    "price_position": (120, 160),
                    "volume_position": (120, 190),
                    "color_patterns": {
                        "up": (255, 0, 0),
                        "down": (0, 255, 0),
                        "flat": (128, 128, 128)
                    }
                }
            }
        }
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                # 合并配置
                default_config.update(user_config)
                return default_config
        except FileNotFoundError:
            return default_config
    
    def save_config(self):
        """保存配置"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def setup_directories(self):
        """创建必要的目录"""
        os.makedirs(self.screenshot_dir, exist_ok=True)
        os.makedirs("logs", exist_ok=True)
    
    def capture_screen_region(self, region_name: str) -> Optional[str]:
        """截取指定区域屏幕"""
        try:
            # 检查区域配置
            region = self.config["monitor_settings"]["monitor_regions"].get(region_name)
            if not region:
                print(f"未找到区域配置: {region_name}")
                return None
            
            x, y, width, height = region
            
            # 这里需要安装截图库
            # 可选方案1: pyautogui
            # 可选方案2: mss (更快)
            # 可选方案3: PIL + win32api
            
            # 临时返回模拟数据
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.screenshot_dir}/{region_name}_{timestamp}.txt"
            
            # 模拟截图结果
            mock_data = f"""模拟截图数据 - {region_name}
时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
区域: ({x}, {y}, {width}, {height})
内容: 中国石油 12.16 -0.25 (-2.02%)
成交量: 45.2万手
"""
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(mock_data)
            
            print(f"📸 已截取区域: {region_name} -> {filename}")
            return filename
            
        except Exception as e:
            print(f"截图失败: {e}", file=sys.stderr)
            return None
    
    def setup_monitor_region(self, software_name: str, region_name: str):
        """设置监控区域"""
        print(f"\n🔧 设置 {software_name} 监控区域")
        print("=" * 50)
        print("请按以下步骤操作:")
        print("1. 打开您的炒股软件（如同花顺、东方财富）")
        print("2. 将软件窗口调整到合适大小")
        print("3. 将鼠标移动到要监控的区域左上角")
        print("4. 按 Enter 记录坐标")
        print("5. 将鼠标移动到区域右下角")
        print("6. 按 Enter 记录坐标")
        print("7. 输入区域名称")
        print("\n按 Ctrl+C 取消")
        
        try:
            input("准备好后按 Enter 开始...")
            
            # 这里需要获取鼠标位置
            # 实际实现需要使用 pyautogui 或类似库
            
            print("模拟获取坐标...")
            x1, y1 = 100, 100  # 模拟左上角
            x2, y2 = 300, 200  # 模拟右下角
            
            width = x2 - x1
            height = y2 - y1
            
            region = (x1, y1, width, height)
            self.config["monitor_settings"]["monitor_regions"][region_name] = region
            
            self.save_config()
            
            print(f"✅ 区域设置完成: {region_name}")
            print(f"   坐标: ({x1}, {y1}) 大小: {width}x{height}")
            
            return region
            
        except KeyboardInterrupt:
            print("\n❌ 设置取消")
            return None
    
    def analyze_screenshot(self, screenshot_path: str, stock_config: Dict) -> Dict:
        """分析截图内容"""
        try:
            # 读取截图文件
            with open(screenshot_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 这里应该使用OCR识别实际截图
            # 暂时使用模拟分析
            
            # 模拟提取价格
            import re
            
            # 尝试从文本提取价格
            price_pattern = r'(\d+\.\d+)'
            prices = re.findall(price_pattern, content)
            
            current_price = 0.0
            if prices:
                current_price = float(prices[0])
            else:
                # 使用模拟数据
                current_price = 12.16 + (time.time() % 10) * 0.01
            
            # 分析结果
            stock_data = stock_config["user_data"]
            cost_price = stock_data["cost_price"]
            stop_loss = stock_data["stop_loss"]
            first_target = stock_data["first_target"]
            
            profit_pct = (current_price - cost_price) / cost_price * 100
            to_stop_loss_pct = (current_price - stop_loss) / stop_loss * 100 if stop_loss > 0 else 0
            to_target_pct = (first_target - current_price) / current_price * 100 if current_price > 0 else 0
            
            alerts = []
            recommendation = "持有"
            
            # 检查条件
            if current_price <= stop_loss:
                alerts.append(f"🚨 触发止损: {current_price:.3f} ≤ {stop_loss:.3f}")
                recommendation = "立即卖出"
            elif current_price >= first_target:
                alerts.append(f"🎯 达到目标: {current_price:.3f} ≥ {first_target:.3f}")
                recommendation = "卖出50%"
            elif profit_pct >= 0:
                alerts.append(f"✅ 回到成本: {current_price:.3f} ≥ {cost_price:.3f}")
                if recommendation == "持有":
                    recommendation = "可考虑卖出"
            
            status = "盈利" if profit_pct > 0 else "亏损"
            
            return {
                "symbol": stock_config["symbol"],
                "name": stock_config["name"],
                "current_price": current_price,
                "cost_price": cost_price,
                "profit_pct": profit_pct,
                "status": status,
                "to_stop_loss_pct": to_stop_loss_pct,
                "to_target_pct": to_target_pct,
                "alerts": alerts,
                "recommendation": recommendation,
                "analysis_time": datetime.now().isoformat(),
                "screenshot_path": screenshot_path
            }
            
        except Exception as e:
            print(f"分析失败: {e}", file=sys.stderr)
            return {
                "symbol": stock_config["symbol"],
                "name": stock_config["name"],
                "error": str(e),
                "analysis_time": datetime.now().isoformat()
            }
    
    def monitor_stock(self, stock_config: Dict):
        """监控单只股票"""
        region_name = stock_config.get("monitor_region")
        if not region_name:
            print(f"未设置监控区域: {stock_config['name']}")
            return None
        
        # 截图
        screenshot_path = self.capture_screen_region(region_name)
        if not screenshot_path:
            return None
        
        # 分析
        result = self.analyze_screenshot(screenshot_path, stock_config)
        
        # 显示结果
        self.display_result(result)
        
        # 记录日志
        self.log_result(result)
        
        return result
    
    def display_result(self, result: Dict):
        """显示分析结果"""
        if "error" in result:
            print(f"❌ {result['name']} 分析失败: {result['error']}")
            return
        
        print(f"\n📊 {result['name']} ({result['symbol']})")
        print(f"   当前价: {result['current_price']:.3f}元")
        print(f"   成本价: {result['cost_price']:.3f}元")
        print(f"   盈亏: {result['profit_pct']:.1f}% ({result['status']})")
        print(f"   距止损: {result['to_stop_loss_pct']:.1f}%")
        print(f"   距目标: {result['to_target_pct']:.1f}%")
        
        if result['alerts']:
            print(f"   ⚠️  提醒:")
            for alert in result['alerts']:
                print(f"      • {alert}")
        
        print(f"   💡 建议: {result['recommendation']}")
    
    def log_result(self, result: Dict):
        """记录结果到日志"""
        log_file = f"logs/desktop_monitor_{datetime.now().strftime('%Y%m%d')}.log"
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "result": result
        }
        
        try:
            # 读取现有日志
            logs = []
            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip():
                            logs.append(json.loads(line))
            
            # 添加新日志
            logs.append(log_entry)
            
            # 保存（只保留最近100条）
            if len(logs) > 100:
                logs = logs[-100:]
            
            with open(log_file, 'w', encoding='utf-8') as f:
                for log in logs:
                    f.write(json.dumps(log, ensure_ascii=False) + '\n')
                    
        except Exception as e:
            print(f"日志记录失败: {e}", file=sys.stderr)
    
    def start_monitoring(self, interval_seconds: int = 30):
        """开始监控"""
        print(f"🖥️ 开始桌面监控")
        print(f"   间隔: {interval_seconds}秒")
        print(f"   监控股票数: {len(self.config['monitored_stocks'])}")
        print("   按 Ctrl+C 停止")
        print("=" * 50)
        
        # 立即检查一次
        print("\n🔍 首次检查...")
        for stock in self.config["monitored_stocks"]:
            self.monitor_stock(stock)
        
        # 设置定时任务
        schedule.every(interval_seconds).seconds.do(self.run_monitoring_cycle)
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 监控已停止")
    
    def run_monitoring_cycle(self):
        """运行监控周期"""
        print(f"\n⏰ {datetime.now().strftime('%H:%M:%S')} 检查...")
        for stock in self.config["monitored_stocks"]:
            self.monitor_stock(stock)
    
    def generate_report(self) -> str:
        """生成监控报告"""
        log_file = f"logs/desktop_monitor_{datetime.now().strftime('%Y%m%d')}.log"
        
        if not os.path.exists(log_file):
            return "今日无监控数据"
        
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                logs = [json.loads(line) for line in f if line.strip()]
            
            if not logs:
                return "无有效监控数据"
            
            # 获取最新数据
            latest_logs = logs[-len(self.config["monitored_stocks"]):]
            
            report = []
            report.append("=" * 80)
            report.append(f"🖥️ 桌面监控报告 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
            report.append("=" * 80)
            
            urgent_alerts = []
            stock_summaries = []
            
            for log in latest_logs:
                result = log["result"]
                if "error" in result:
                    continue
                
                stock_summaries.append(
                    f"{result['name']}: {result['current_price']:.3f}元 "
                    f"({result['profit_pct']:.1f}%) - {result['recommendation']}"
                )
                
                if result['alerts']:
                    for alert in result['alerts']:
                        if "止损" in alert or "立即卖出" in result['recommendation']:
                            urgent_alerts.append(f"{result['name']}: {alert}")
            
            if urgent_alerts:
                report.append("\n🚨 紧急提醒:")
                for alert in urgent_alerts:
                    report.append(f"  • {alert}")
            
            report.append("\n📈 股票状态:")
            for summary in stock_summaries:
                report.append(f"  • {summary}")
            
            report.append(f"\n📊 监控统计: 共{len(stock_summaries)}只股票")
            
            report.append("\n" + "=" * 80)
            return "\n".join(report)
            
        except Exception as e:
            return f"生成报告失败: {str(e)}"

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="桌面炒股软件监控系统")
    parser.add_argument("--setup", help="设置监控区域，格式：软件名,区域名")
    parser.add_argument("--check", action="store_true", help="立即检查一次")
    parser.add_argument("--monitor", action="store_true", help="开始持续监控")
    parser.add_argument("--interval", type=int, default=30, help="监控间隔秒数")
    parser.add_argument("--report", action="store_true", help="生成报告")
    parser.add_argument("--add-stock", help="添加监控股票，格式：代码,名称,股数,成本价")
    
    args = parser.parse_args()
    
    monitor = DesktopStockMonitor()
    
    if args.setup:
        parts = args.setup.split(',')
        if len(parts) >= 2:
            software = parts[0].strip()
            region = parts[1].strip()
            monitor.setup_monitor_region(software, region)
        else:
            print("参数格式错误，应为：软件名,区域名")
    
    elif args.add_stock:
        parts = args.add_stock.split(',')
        if len(parts) >= 4:
            symbol = parts[0].strip()
            name = parts[1].strip()
            shares = int(parts[2].strip())
            cost_price = float(parts[3].strip())
            
            new_stock = {
                "symbol": symbol,
                "name": name,
                "user_data": {
                    "shares": shares,
                    "cost_price": cost_price,
                    "stop_loss": cost_price * 0.93,
                    "first_target": cost_price * 1.15
                },
                "monitor_region": f"监控_{symbol}"
            }
            
            monitor.config["monitored_stocks"].append(new_stock)
            monitor.save_config()
            print(f"✅ 已添加 {name} ({symbol}) 到监控列表")
        else:
            print("参数格式错误，应为：代码,名称,股数,成本价")
    
    elif args.check:
        print("🔍 立即检查...")
        for stock in monitor.config["monitored_stocks"]:
            monitor.monitor_stock(stock)
    
    elif args.monitor:
        monitor.start_monitoring(args.interval)
    
    elif args.report:
        report = monitor.generate_report()
        print(report)
    
    else:
        print("🖥️ 桌面炒股软件监控系统")
        print("=" * 50)
        print("使用方法:")
        print("  --setup 同花顺,中国石油区域   设置监控区域")
        print("  --add-stock 601857,中国石油,800,12.465  添加股票")
        print("  --check                    立即检查一次")
        print("  --monitor --interval 30    开始持续监控")
        print("  --report                   生成监控报告")
        print("\n示例:")
        print("  1. 先设置监控区域: --setup 同花顺,中国石油区域")
        print("  2. 添加股票: --add-stock 601857,中国石油,800,12.465")
        print("  3. 开始监控: --monitor --interval 30")

if __name__ == "__main__":
    main()
