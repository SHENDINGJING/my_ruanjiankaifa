#!/usr/bin/env python3
"""
股票实时监控系统
基于中短线稳健型交易策略
"""

import json
import time
import schedule
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import yfinance as yf
import sys
import os

class StockMonitor:
    """股票监控器"""
    
    def __init__(self, config_path: str = "monitor_config.json"):
        self.config_path = config_path
        self.config = self.load_config()
        self.monitoring_history = []
        
    def load_config(self) -> Dict:
        """加载监控配置"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"配置文件 {self.config_path} 不存在，使用默认配置")
            return self.create_default_config()
    
    def create_default_config(self) -> Dict:
        """创建默认配置"""
        return {
            "monitoring_stocks": [],
            "alert_rules": {
                "buy_signals": ["所有条件同时满足"],
                "sell_signals": ["触发止损", "技术破位", "达到目标"],
                "hold_signals": ["未触发任何卖出信号"]
            }
        }
    
    def save_config(self):
        """保存配置"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def add_stock_to_monitor(self, symbol: str, name: str = None, 
                            shares: int = 0, cost_price: float = 0):
        """添加股票到监控列表"""
        if not name:
            # 尝试获取股票名称
            try:
                stock = yf.Ticker(symbol)
                info = stock.info
                name = info.get('longName', info.get('shortName', symbol))
            except:
                name = symbol
        
        # 检查是否已存在
        for stock in self.config.get('monitoring_stocks', []):
            if stock['symbol'] == symbol:
                print(f"股票 {symbol} 已在监控列表中")
                return False
        
        # 添加新股票
        new_stock = {
            "symbol": symbol,
            "name": name,
            "user_position": {
                "shares": shares,
                "cost_price": cost_price,
                "current_price": 0,
                "status": "监控中"
            },
            "strategy_settings": {
                "stop_loss_percent": 7,
                "stop_loss_price": cost_price * 0.93 if cost_price > 0 else 0,
                "first_target_percent": 15,
                "first_target_price": cost_price * 1.15 if cost_price > 0 else 0,
                "second_target_percent": 20,
                "second_target_price": cost_price * 1.20 if cost_price > 0 else 0
            },
            "monitoring_frequency": "每30分钟",
            "alert_channels": ["openclaw_feishu"],
            "added_time": datetime.now().isoformat()
        }
        
        if 'monitoring_stocks' not in self.config:
            self.config['monitoring_stocks'] = []
        
        self.config['monitoring_stocks'].append(new_stock)
        self.save_config()
        
        print(f"✅ 已添加 {name} ({symbol}) 到监控列表")
        return True
    
    def remove_stock_from_monitor(self, symbol: str):
        """从监控列表移除股票"""
        if 'monitoring_stocks' not in self.config:
            print("监控列表为空")
            return False
        
        new_list = [s for s in self.config['monitoring_stocks'] if s['symbol'] != symbol]
        
        if len(new_list) == len(self.config['monitoring_stocks']):
            print(f"未找到股票 {symbol}")
            return False
        
        removed_count = len(self.config['monitoring_stocks']) - len(new_list)
        self.config['monitoring_stocks'] = new_list
        self.save_config()
        
        print(f"✅ 已移除 {removed_count} 只股票")
        return True
    
    def list_monitored_stocks(self):
        """列出监控中的股票"""
        if not self.config.get('monitoring_stocks'):
            print("当前没有监控中的股票")
            return
        
        print(f"\n📋 监控股票列表 ({len(self.config['monitoring_stocks'])}只):")
        print("=" * 80)
        for i, stock in enumerate(self.config['monitoring_stocks'], 1):
            pos = stock['user_position']
            settings = stock['strategy_settings']
            
            print(f"{i}. {stock['name']} ({stock['symbol']})")
            print(f"   持仓: {pos['shares']}股 | 成本: {pos['cost_price']:.3f}元")
            print(f"   止损: {settings['stop_loss_price']:.3f}元 | 目标: {settings['first_target_price']:.3f}元")
            print(f"   状态: {pos['status']}")
            print()
    
    def fetch_current_price(self, symbol: str) -> Optional[float]:
        """获取当前价格"""
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(period='1d')
            
            if hist.empty:
                # 尝试获取实时价格
                info = stock.info
                current = info.get('regularMarketPrice', 
                                 info.get('currentPrice', 0))
                return current
            
            return hist['Close'].iloc[-1]
            
        except Exception as e:
            print(f"获取 {symbol} 价格失败: {e}", file=sys.stderr)
            return None
    
    def check_stock_conditions(self, stock_config: Dict) -> Dict:
        """检查股票条件"""
        symbol = stock_config['symbol']
        current_price = self.fetch_current_price(symbol)
        
        if current_price is None:
            return {
                "symbol": symbol,
                "current_price": 0,
                "status": "数据获取失败",
                "alerts": [],
                "recommendation": "无法分析"
            }
        
        # 更新当前价格
        stock_config['user_position']['current_price'] = current_price
        
        alerts = []
        recommendation = "持有"
        
        pos = stock_config['user_position']
        settings = stock_config['strategy_settings']
        
        cost_price = pos['cost_price']
        stop_loss = settings['stop_loss_price']
        first_target = settings['first_target_price']
        
        # 检查止损
        if cost_price > 0 and current_price <= stop_loss:
            alerts.append(f"🚨 止损触发: 当前价{current_price:.3f} ≤ 止损价{stop_loss:.3f}")
            recommendation = "立即卖出"
        
        # 检查第一目标
        elif cost_price > 0 and current_price >= first_target:
            alerts.append(f"🎯 达到第一目标: 当前价{current_price:.3f} ≥ 目标价{first_target:.3f}")
            recommendation = "卖出50%锁定利润"
        
        # 检查回本
        elif cost_price > 0 and current_price >= cost_price:
            alerts.append(f"✅ 回到成本价: 当前价{current_price:.3f} ≥ 成本价{cost_price:.3f}")
            if recommendation == "持有":
                recommendation = "可考虑卖出"
        
        # 计算盈亏
        if cost_price > 0:
            profit_pct = (current_price - cost_price) / cost_price * 100
            profit_status = f"盈利{profit_pct:.1f}%" if profit_pct > 0 else f"亏损{abs(profit_pct):.1f}%"
            alerts.append(f"📊 盈亏状态: {profit_status}")
        
        return {
            "symbol": symbol,
            "name": stock_config['name'],
            "current_price": current_price,
            "cost_price": cost_price,
            "stop_loss_price": stop_loss,
            "first_target_price": first_target,
            "alerts": alerts,
            "recommendation": recommendation,
            "check_time": datetime.now().isoformat()
        }
    
    def check_all_stocks(self) -> List[Dict]:
        """检查所有监控股票"""
        results = []
        
        if not self.config.get('monitoring_stocks'):
            print("没有需要监控的股票")
            return results
        
        print(f"\n⏰ 开始检查 {len(self.config['monitoring_stocks'])} 只股票...")
        print("=" * 80)
        
        for stock in self.config['monitoring_stocks']:
            result = self.check_stock_conditions(stock)
            results.append(result)
            
            # 显示结果
            print(f"\n📈 {result['name']} ({result['symbol']})")
            print(f"   当前价: {result['current_price']:.3f}元")
            
            if result['cost_price'] > 0:
                profit_pct = (result['current_price'] - result['cost_price']) / result['cost_price'] * 100
                print(f"   成本价: {result['cost_price']:.3f}元 ({'盈' if profit_pct > 0 else '亏'}{abs(profit_pct):.1f}%)")
                print(f"   止损价: {result['stop_loss_price']:.3f}元")
                print(f"   目标价: {result['first_target_price']:.3f}元")
            
            if result['alerts']:
                print(f"   ⚠️  提醒:")
                for alert in result['alerts']:
                    print(f"      • {alert}")
            
            print(f"   💡 建议: {result['recommendation']}")
        
        # 保存检查历史
        self.monitoring_history.append({
            "check_time": datetime.now().isoformat(),
            "results": results
        })
        
        # 保存最近10次检查
        if len(self.monitoring_history) > 10:
            self.monitoring_history = self.monitoring_history[-10:]
        
        return results
    
    def generate_daily_report(self) -> str:
        """生成每日报告"""
        if not self.monitoring_history:
            return "暂无监控数据"
        
        latest_check = self.monitoring_history[-1]
        results = latest_check['results']
        
        report = []
        report.append("=" * 80)
        report.append(f"📊 股票监控每日报告 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        report.append("=" * 80)
        
        urgent_alerts = []
        normal_alerts = []
        
        for result in results:
            if result['alerts']:
                for alert in result['alerts']:
                    if "止损触发" in alert or "立即卖出" in result['recommendation']:
                        urgent_alerts.append(f"{result['name']}: {alert}")
                    else:
                        normal_alerts.append(f"{result['name']}: {alert}")
        
        if urgent_alerts:
            report.append("\n🚨 紧急提醒:")
            for alert in urgent_alerts:
                report.append(f"  • {alert}")
        
        if normal_alerts:
            report.append("\n⚠️  一般提醒:")
            for alert in normal_alerts:
                report.append(f"  • {alert}")
        
        if not urgent_alerts and not normal_alerts:
            report.append("\n✅ 所有股票状态正常，无特别提醒")
        
        # 汇总统计
        total_stocks = len(results)
        stocks_with_alerts = len([r for r in results if r['alerts']])
        
        report.append(f"\n📈 监控统计: 共{total_stocks}只股票，{stocks_with_alerts}只有提醒")
        
        report.append("\n" + "=" * 80)
        report.append("💡 操作建议:")
        report.append("1. 紧急提醒：立即处理")
        report.append("2. 一般提醒：今日内处理")
        report.append("3. 无提醒：继续持有观察")
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def setup_scheduled_monitoring(self, interval_minutes: int = 30):
        """设置定时监控"""
        print(f"🕐 设置定时监控: 每{interval_minutes}分钟检查一次")
        print("监控时间: 交易日 09:30-15:00")
        print("按 Ctrl+C 停止监控")
        
        # 立即检查一次
        self.check_all_stocks()
        
        # 设置定时任务
        schedule.every(interval_minutes).minutes.do(self.check_all_stocks)
        
        # 设置每日报告
        schedule.every().day.at("15:30").do(
            lambda: print(f"\n📅 每日报告:\n{self.generate_daily_report()}")
        )
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # 每分钟检查一次任务
        except KeyboardInterrupt:
            print("\n🛑 监控已停止")
    
    def run_once(self):
        """运行一次检查"""
        return self.check_all_stocks()

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="股票实时监控系统")
    parser.add_argument("--add", help="添加股票到监控列表，格式：代码,名称,股数,成本价")
    parser.add_argument("--remove", help="从监控列表移除股票")
    parser.add_argument("--list", action="store_true", help="列出监控中的股票")
    parser.add_argument("--check", action="store_true", help="立即检查所有股票")
    parser.add_argument("--report", action="store_true", help="生成每日报告")
    parser.add_argument("--monitor", action="store_true", help="启动定时监控")
    parser.add_argument("--interval", type=int, default=30, help="监控间隔分钟数")
    
    args = parser.parse_args()
    
    monitor = StockMonitor()
    
    if args.add:
        # 解析参数
        parts = args.add.split(',')
        symbol = parts[0].strip()
        name = parts[1].strip() if len(parts) > 1 else None
        shares = int(parts[2].strip()) if len(parts) > 2 else 0
        cost_price = float(parts[3].strip()) if len(parts) > 3 else 0
        
        monitor.add_stock_to_monitor(symbol, name, shares, cost_price)
    
    elif args.remove:
        monitor.remove_stock_from_monitor(args.remove)
    
    elif args.list:
        monitor.list_monitored_stocks()
    
    elif args.check:
        monitor.run_once()
    
    elif args.report:
        print(monitor.generate_daily_report())
    
    elif args.monitor:
        monitor.setup_scheduled_monitoring(args.interval)
    
    else:
        # 默认显示帮助
        print("股票实时监控系统")
        print("=" * 50)
        print("使用方法:")
        print("  --add 601857.SS,中国石油,800,12.465  添加股票")
        print("  --remove 601857.SS                   移除股票")
        print("  --list                               列出监控股票")
        print("  --check                              立即检查")
        print("  --report                             生成报告")
        print("  --monitor --interval 30              启动定时监控")
        print("\n示例:")
        print("  python stock_monitor.py --add 601857.SS,中国石油,800,12.465")
        print("  python stock_monitor.py --check")
        print("  python stock_monitor.py --monitor --interval 30")

if __name__ == "__main__":
    main()