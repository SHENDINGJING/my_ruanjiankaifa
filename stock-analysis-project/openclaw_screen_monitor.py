#!/usr/bin/env python3
"""
OpenClaw屏幕监控系统
使用OpenClaw的nodes screen和browser功能实现实时监控
"""

import json
import time
import os
import sys
import subprocess
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import schedule

class OpenClawScreenMonitor:
    """OpenClaw屏幕监控器"""
    
    def __init__(self, config_path: str = "openclaw_monitor_config.json"):
        self.config_path = config_path
        self.config = self.load_config()
        self.screen_recordings_dir = "screen_recordings"
        self.setup_directories()
        
    def load_config(self) -> Dict:
        """加载配置"""
        default_config = {
            "openclaw_settings": {
                "gateway_url": "ws://localhost:18765",
                "gateway_token": "",
                "monitor_method": "browser_snapshot",  # browser_snapshot | screen_record | canvas
                "monitor_interval": 30,
                "browser_profile": "openclaw"
            },
            "monitoring_targets": [
                {
                    "name": "炒股软件监控",
                    "type": "browser_window",
                    "target_url": "about:blank",  # 实际应该是炒股软件URL
                    "region": "auto",  # 监控区域
                    "stocks": [
                        {
                            "symbol": "601857",
                            "name": "中国石油",
                            "user_data": {
                                "shares": 800,
                                "cost_price": 12.465,
                                "stop_loss": 11.592,
                                "first_target": 14.335
                            },
                            "screen_region": (100, 100, 300, 150)  # x,y,width,height
                        }
                    ]
                }
            ],
            "analysis_settings": {
                "enable_ai_analysis": True,
                "ai_model": "deepseek/deepseek-chat",
                "analysis_prompt": "分析炒股软件截图中的股票信息",
                "save_recordings": True,
                "max_recordings": 100
            },
            "notification_settings": {
                "enable_alerts": True,
                "alert_channels": ["feishu", "desktop"],
                "urgent_triggers": ["stop_loss", "target_reached", "abnormal_volume"]
            }
        }
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
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
        os.makedirs(self.screen_recordings_dir, exist_ok=True)
        os.makedirs("logs/openclaw_monitor", exist_ok=True)
    
    def run_openclaw_command(self, command: List[str], timeout: int = 30) -> Tuple[bool, str]:
        """运行OpenClaw命令"""
        try:
            full_command = ["openclaw"] + command
            
            print(f"运行命令: {' '.join(full_command)}")
            
            result = subprocess.run(
                full_command,
                capture_output=True,
                text=True,
                timeout=timeout,
                encoding='utf-8'
            )
            
            if result.returncode == 0:
                return True, result.stdout.strip()
            else:
                return False, f"错误: {result.stderr.strip()}"
                
        except subprocess.TimeoutExpired:
            return False, "命令执行超时"
        except Exception as e:
            return False, f"执行失败: {str(e)}"
    
    def check_openclaw_status(self) -> bool:
        """检查OpenClaw状态"""
        print("检查OpenClaw状态...")
        
        # 检查gateway状态
        success, output = self.run_openclaw_command(["gateway", "status"])
        
        if success:
            if "online" in output.lower():
                print("✅ OpenClaw Gateway在线")
                return True
            else:
                print("⚠️  Gateway状态异常")
                return False
        else:
            print(f"❌ 检查Gateway失败: {output}")
            
            # 尝试启动gateway
            print("尝试启动Gateway...")
            success, output = self.run_openclaw_command(["gateway", "start"], timeout=60)
            
            if success:
                print("✅ Gateway启动成功")
                time.sleep(5)  # 等待启动完成
                return True
            else:
                print(f"❌ Gateway启动失败: {output}")
                return False
    
    def capture_browser_snapshot(self) -> Optional[str]:
        """使用OpenClaw browser snapshot捕获屏幕"""
        print("使用OpenClaw browser snapshot捕获屏幕...")
        
        # 首先检查browser状态
        success, output = self.run_openclaw_command(["browser", "status"])
        
        if not success or "not running" in output.lower():
            print("启动OpenClaw browser...")
            success, output = self.run_openclaw_command(["browser", "start"], timeout=60)
            
            if not success:
                print(f"❌ 启动browser失败: {output}")
                return None
        
        # 打开炒股软件（如果需要）
        target_url = self.config["monitoring_targets"][0]["target_url"]
        if target_url != "about:blank":
            print(f"导航到: {target_url}")
            success, output = self.run_openclaw_command(["browser", "navigate", target_url])
            time.sleep(3)  # 等待页面加载
        
        # 捕获快照
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"{self.screen_recordings_dir}/browser_snapshot_{timestamp}.txt"
        
        print("捕获浏览器快照...")
        success, output = self.run_openclaw_command(["browser", "snapshot", "--format", "ai"])
        
        if success:
            # 保存快照数据
            snapshot_data = {
                "timestamp": datetime.now().isoformat(),
                "method": "browser_snapshot",
                "data": output[:5000]  # 保存前5000字符
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(snapshot_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ 浏览器快照已保存: {output_file}")
            return output_file
        else:
            print(f"❌ 捕获快照失败: {output}")
            return None
    
    def capture_screen_record(self) -> Optional[str]:
        """使用OpenClaw nodes screen record录制屏幕"""
        print("使用OpenClaw nodes screen record录制屏幕...")
        
        # 检查是否有已配对的节点
        success, output = self.run_openclaw_command(["nodes", "status"])
        
        if success and "Paired: 0" in output:
            print("⚠️  没有已配对的节点，无法录制屏幕")
            print("请先配对节点：")
            print("1. 在其他设备上安装OpenClaw Node")
            print("2. 使用配对码配对")
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"{self.screen_recordings_dir}/screen_record_{timestamp}.mp4"
        
        # 录制10秒屏幕
        print("录制10秒屏幕...")
        success, output = self.run_openclaw_command([
            "nodes", "screen", "record",
            "--duration", "10000",
            "--fps", "5",
            "--out", output_file
        ], timeout=15000)  # 15秒超时
        
        if success:
            print(f"✅ 屏幕录制已保存: {output_file}")
            
            # 记录元数据
            meta_file = f"{output_file}.json"
            meta_data = {
                "timestamp": datetime.now().isoformat(),
                "method": "screen_record",
                "duration_ms": 10000,
                "fps": 5,
                "file_path": output_file
            }
            
            with open(meta_file, 'w', encoding='utf-8') as f:
                json.dump(meta_data, f, indent=2, ensure_ascii=False)
            
            return output_file
        else:
            print(f"❌ 屏幕录制失败: {output}")
            return None
    
    def analyze_screen_content(self, capture_file: str, stock_config: Dict) -> Dict:
        """分析屏幕内容"""
        print(f"分析 {stock_config['name']} 的屏幕内容...")
        
        # 这里可以集成AI分析
        # 暂时使用模拟分析
        
        # 模拟从屏幕内容提取数据
        current_price = 12.16 + (time.time() % 10) * 0.01 - 0.05
        
        stock_data = stock_config["user_data"]
        cost_price = stock_data["cost_price"]
        stop_loss = stock_data["stop_loss"]
        first_target = stock_data["first_target"]
        
        profit_pct = (current_price - cost_price) / cost_price * 100
        to_stop_loss_pct = (current_price - stop_loss) / stop_loss * 100 if stop_loss > 0 else 0
        to_target_pct = (first_target - current_price) / current_price * 100 if current_price > 0 else 0
        
        # 分析结果
        alerts = []
        recommendation = "持有"
        
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
        
        result = {
            "symbol": stock_config["symbol"],
            "name": stock_config["name"],
            "analysis_time": datetime.now().isoformat(),
            "capture_method": os.path.basename(capture_file).split('_')[0],
            "current_price": current_price,
            "cost_price": cost_price,
            "profit_pct": profit_pct,
            "status": status,
            "to_stop_loss_pct": to_stop_loss_pct,
            "to_target_pct": to_target_pct,
            "alerts": alerts,
            "recommendation": recommendation,
            "risk_reward_ratio": abs(to_target_pct / to_stop_loss_pct) if to_stop_loss_pct != 0 else 0
        }
        
        # 保存分析结果
        result_file = f"{self.screen_recordings_dir}/analysis_{stock_config['symbol']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        return result
    
    def display_analysis(self, result: Dict):
        """显示分析结果"""
        print(f"\n{'='*60}")
        print(f"📊 OpenClaw屏幕监控分析 - {result['name']} ({result['symbol']})")
        print(f"{'='*60}")
        
        print(f"\n📈 市场数据:")
        print(f"   当前价格: {result['current_price']:.3f}元")
        print(f"   成本价格: {result['cost_price']:.3f}元")
        print(f"   盈亏状态: {result['profit_pct']:.1f}% ({result['status']})")
        
        print(f"\n🎯 策略分析:")
        print(f"   距止损: {result['to_stop_loss_pct']:+.1f}%")
        print(f"   距目标: {result['to_target_pct']:+.1f}%")
        print(f"   风险收益比: 1:{result['risk_reward_ratio']:.1f}")
        
        if result['alerts']:
            print(f"\n⚠️  提醒:")
            for alert in result['alerts']:
                print(f"    • {alert}")
        
        print(f"\n💡 操作建议: {result['recommendation']}")
        
        # 检查紧急情况
        if "立即卖出" in result['recommendation']:
            print(f"\n🚨 紧急情况！需要立即处理！")
        
        print(f"\n⏰ 分析时间: {result['analysis_time']}")
        print(f"📋 捕获方法: {result['capture_method']}")
        print(f"{'='*60}")
    
    def send_alert(self, result: Dict):
        """发送提醒"""
        if not self.config['notification_settings']['enable_alerts']:
            return
        
        # 检查是否需要发送紧急提醒
        urgent = any("止损" in alert for alert in result['alerts'])
        
        if urgent or "立即卖出" in result['recommendation']:
            message = f"🚨 紧急股票提醒: {result['name']} ({result['symbol']})\n"
            message += f"当前价: {result['current_price']:.3f}元\n"
            message += f"建议: {result['recommendation']}\n"
            message += f"时间: {datetime.now().strftime('%H:%M:%S')}"
            
            print(f"\n发送紧急提醒: {message}")
            
            # 这里可以集成OpenClaw message发送
            # openclaw message send --channel feishu --message "..."
    
    def monitor_stock(self, stock_config: Dict):
        """监控单只股票"""
        print(f"\n🔍 监控 {stock_config['name']} ({stock_config['symbol']})...")
        
        # 选择监控方法
        method = self.config["openclaw_settings"]["monitor_method"]
        
        capture_file = None
        if method == "browser_snapshot":
            capture_file = self.capture_browser_snapshot()
        elif method == "screen_record":
            capture_file = self.capture_screen_record()
        else:
            print(f"❌ 未知的监控方法: {method}")
            return None
        
        if not capture_file:
            print("❌ 屏幕捕获失败")
            return None
        
        # 分析屏幕内容
        result = self.analyze_screen_content(capture_file, stock_config)
        
        # 显示结果
        self.display_analysis(result)
        
        # 发送提醒
        self.send_alert(result)
        
        # 记录日志
        self.log_monitoring(result)
        
        return result
    
    def log_monitoring(self, result: Dict):
        """记录监控日志"""
        log_file = f"logs/openclaw_monitor/{datetime.now().strftime('%Y%m%d')}.log"
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "symbol": result['symbol'],
            "name": result['name'],
            "price": result['current_price'],
            "recommendation": result['recommendation'],
            "alerts": result['alerts']
        }
        
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"日志记录失败: {e}", file=sys.stderr)
    
    def start_monitoring(self, interval_seconds: int = 30):
        """开始监控"""
        print(f"🖥️ 启动OpenClaw屏幕监控系统")
        print(f"   监控方法: {self.config['openclaw_settings']['monitor_method']}")
        print(f"   监控间隔: {interval_seconds}秒")
        print("   按 Ctrl+C 停止")
        print("=" * 60)
        
        # 检查OpenClaw状态
        if not self.check_openclaw_status():
            print("❌ OpenClaw状态检查失败，无法启动监控")
            return
        
        # 立即检查一次
        print("\n🔍 首次检查...")
        for target in self.config["monitoring_targets"]:
            for stock in target["stocks"]:
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
        print(f"\n⏰ {datetime.now().strftime('%H:%M:%S')} 监控检查...")
        for target in self.config["monitoring_targets"]:
            for stock in target["stocks"]:
                self.monitor_stock(stock)

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="OpenClaw屏幕监控系统")
    parser.add_argument("--setup", choices=["browser_snapshot", "screen_record"], 
                       default="browser_snapshot", help="设置监控方法")
    parser.add_argument("--add-stock", help="添加监控股票，格式：代码,名称,股数,成本价")
    parser.add_argument("--check", action="store_true", help="立即检查一次")
    parser.add_argument("--monitor", action="store_true", help="开始持续监控")
    parser.add_argument("--interval", type=int, default=30, help="监控间隔秒数")
    parser.add_argument("--status", action="store_true", help="检查OpenClaw状态")
    
    args = parser.parse_args()
    
    monitor = OpenClawScreenMonitor()
    
    if args.setup:
        monitor.config["openclaw_settings"]["monitor_method"] = args.setup
        monitor.save_config()
        print(f"✅ 监控方法已设置为: {args.setup}")
    
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
                "screen_region": (100, 100, 300, 150)
            }
            
            # 添加到第一个监控目标
            if monitor.config["monitoring_targets"]:
                monitor.config["monitoring_targets"][0]["stocks"].append(new_stock)
            else:
                monitor.config["monitoring_targets"] = [{
                    "name": "炒股软件监控",
                    "type": "browser_window",
                    "target_url": "about:blank",
                    "region": "auto",
                    "stocks": [new_stock]
                }]
            
            monitor.save_config()
            print(f"✅ 已添加 {name} ({symbol}) 到监控列表")
        else:
            print("参数格式错误，应为：代码,名称,股数,成本价")
    
    elif args.status:
        monitor.check_openclaw_status()
    
    elif args.check:
        print("🔍 立即检查...")
        if monitor.check_openclaw_status():
            for target in monitor.config["monitoring_targets"]:
                for stock in target["stocks"]:
                    monitor.monitor_stock(stock)
    
    elif args.monitor:
        monitor.start_monitoring(args.interval)
    
    else:
        print("🖥️ OpenClaw屏幕监控系统")
        print("=" * 50)
        print("使用方法:")
        print("  --setup browser_snapshot   设置浏览器快照监控")
        print("  --setup screen_record      设置屏幕录制监控")
        print("  --add-stock 601857,中国石油,800,12.465  添加股票")
        print("  --status                   检查OpenClaw状态")
        print("  --check                    立即检查一次")
        print("  --monitor --interval 30    开始持续监控")
        print("\n推荐步骤:")
        print("  1. --status 检查OpenClaw状态")
        print("  2. --add-stock 添加您的股票")
        print("  3. --check 测试监控")
        print("  4. --monitor 开始实时监控")

if __name__ == "__main__":
    main()