#!/usr/bin/env python3
"""
OpenClaw集成 - 股票监控消息推送
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, List
import subprocess

class OpenClawNotifier:
    """OpenClaw消息通知器"""
    
    def __init__(self, config_path: str = "monitor_config.json"):
        self.config_path = config_path
        self.config = self.load_config()
        
    def load_config(self) -> Dict:
        """加载配置"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def send_openclaw_message(self, message: str, urgent: bool = False):
        """通过OpenClaw发送消息"""
        try:
            # 这里可以集成OpenClaw的消息发送API
            # 目前先打印到控制台
            
            prefix = "🚨 " if urgent else "📢 "
            formatted_message = f"{prefix}{datetime.now().strftime('%H:%M')} - {message}"
            
            print(formatted_message)
            
            # 在实际集成中，可以调用OpenClaw的API
            # 例如：openclaw message send --channel feishu --message "提醒内容"
            
            return True
            
        except Exception as e:
            print(f"发送消息失败: {e}", file=sys.stderr)
            return False
    
    def format_stock_alert(self, stock_result: Dict) -> str:
        """格式化股票提醒消息"""
        symbol = stock_result['symbol']
        name = stock_result['name']
        current_price = stock_result['current_price']
        recommendation = stock_result['recommendation']
        
        # 构建消息
        message = f"股票提醒: {name} ({symbol})\n"
        message += f"当前价格: {current_price:.3f}元\n"
        
        if stock_result.get('cost_price', 0) > 0:
            cost = stock_result['cost_price']
            profit_pct = (current_price - cost) / cost * 100
            message += f"成本价格: {cost:.3f}元 ({'盈' if profit_pct > 0 else '亏'}{abs(profit_pct):.1f}%)\n"
        
        # 添加具体提醒
        if stock_result['alerts']:
            message += "提醒事项:\n"
            for alert in stock_result['alerts'][:3]:  # 最多显示3条
                message += f"• {alert}\n"
        
        message += f"操作建议: {recommendation}"
        
        return message
    
    def check_and_notify(self):
        """检查并发送通知"""
        try:
            # 运行监控检查
            from stock_monitor import StockMonitor
            monitor = StockMonitor(self.config_path)
            results = monitor.check_all_stocks()
            
            # 发送重要提醒
            urgent_sent = False
            for result in results:
                # 检查是否需要紧急通知
                is_urgent = any(
                    "止损触发" in alert or 
                    "立即卖出" in result['recommendation']
                    for alert in result['alerts']
                )
                
                if is_urgent or result['alerts']:
                    message = self.format_stock_alert(result)
                    self.send_openclaw_message(message, urgent=is_urgent)
                    
                    if is_urgent:
                        urgent_sent = True
            
            # 如果没有紧急提醒，发送摘要
            if not urgent_sent and results:
                total = len(results)
                with_alerts = len([r for r in results if r['alerts']])
                
                if with_alerts > 0:
                    summary = f"监控摘要: 检查{total}只股票，{with_alerts}只有提醒"
                    self.send_openclaw_message(summary)
            
            return results
            
        except Exception as e:
            error_msg = f"监控检查失败: {str(e)}"
            self.send_openclaw_message(error_msg, urgent=True)
            return []

def setup_cron_job():
    """设置定时任务"""
    script_path = os.path.abspath(__file__)
    project_dir = os.path.dirname(script_path)
    
    cron_config = f"""# 股票监控定时任务
# 每30分钟检查一次（交易日）
*/30 9-15 * * 1-5 cd {project_dir} && python {script_path} --check > /tmp/stock_monitor.log 2>&1

# 每日收盘后报告
30 15 * * 1-5 cd {project_dir} && python {script_path} --report > /tmp/stock_report.log 2>&1
"""
    
    cron_file = os.path.join(project_dir, "cron_setup.txt")
    with open(cron_file, 'w', encoding='utf-8') as f:
        f.write(cron_config)
    
    print(f"✅ 定时任务配置已保存到: {cron_file}")
    print("\n📋 配置说明:")
    print("1. 交易日每30分钟检查一次股票")
    print("2. 每日收盘后生成报告")
    print("3. 日志保存到 /tmp/stock_monitor.log")
    print("\n🔧 设置方法:")
    print(f"  执行: crontab {cron_file}")
    print("  或手动添加到crontab")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="OpenClaw股票监控集成")
    parser.add_argument("--check", action="store_true", help="检查并发送通知")
    parser.add_argument("--report", action="store_true", help="生成报告")
    parser.add_argument("--setup-cron", action="store_true", help="设置定时任务")
    parser.add_argument("--test-message", help="测试发送消息")
    
    args = parser.parse_args()
    
    notifier = OpenClawNotifier()
    
    if args.check:
        print("🔍 开始检查股票并发送通知...")
        results = notifier.check_and_notify()
        print(f"✅ 检查完成，处理了 {len(results)} 只股票")
    
    elif args.report:
        from stock_monitor import StockMonitor
        monitor = StockMonitor()
        report = monitor.generate_daily_report()
        print(report)
        
        # 也可以通过OpenClaw发送报告
        # notifier.send_openclaw_message(f"每日报告:\\n{report}")
    
    elif args.setup_cron:
        setup_cron_job()
    
    elif args.test_message:
        notifier.send_openclaw_message(args.test_message, urgent=True)
        print("✅ 测试消息已发送")
    
    else:
        print("OpenClaw股票监控集成")
        print("=" * 50)
        print("使用方法:")
        print("  --check          检查并发送通知")
        print("  --report         生成每日报告")
        print("  --setup-cron     设置定时任务")
        print("  --test-message '内容'  测试发送消息")
        print("\n集成说明:")
        print("1. 需要配置OpenClaw消息发送权限")
        print("2. 可以集成到Feishu、Telegram等渠道")
        print("3. 支持定时自动监控")

if __name__ == "__main__":
    main()