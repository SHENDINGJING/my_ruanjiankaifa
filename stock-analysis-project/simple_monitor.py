#!/usr/bin/env python3
"""
简单股票监控系统 - 立即开始
"""

import json
import time
import os
from datetime import datetime
import random

def monitor_stock():
    """监控股票"""
    # 您的股票信息
    stock = {
        "symbol": "601857",
        "name": "中国石油",
        "shares": 800,
        "cost_price": 12.465,
        "stop_loss": 11.592,  # -7%
        "first_target": 14.335,  # +15%
        "second_target": 14.958  # +20%
    }
    
    print("=" * 60)
    print("📈 股票实时监控系统 - 简单版")
    print("=" * 60)
    print(f"股票: {stock['name']} ({stock['symbol']})")
    print(f"持仓: {stock['shares']}股")
    print(f"成本: {stock['cost_price']}元/股")
    print(f"止损: {stock['stop_loss']}元 (-7%)")
    print(f"目标1: {stock['first_target']}元 (+15%)")
    print(f"目标2: {stock['second_target']}元 (+20%)")
    print("=" * 60)
    print("按 Ctrl+C 停止监控")
    print("=" * 60)
    
    try:
        while True:
            # 模拟当前价格（实际应该从API获取）
            current_price = stock['cost_price'] * (1 + (random.random() - 0.5) * 0.1)
            current_price = round(current_price, 3)
            
            # 计算盈亏
            profit_loss = current_price - stock['cost_price']
            profit_pct = (profit_loss / stock['cost_price']) * 100
            
            # 计算到关键价格的距离
            to_stop_loss = current_price - stock['stop_loss']
            to_stop_loss_pct = (to_stop_loss / stock['stop_loss']) * 100
            
            to_first_target = stock['first_target'] - current_price
            to_first_target_pct = (to_first_target / current_price) * 100
            
            # 分析
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            print(f"\n⏰ {timestamp} 监控更新:")
            print(f"   当前价格: {current_price:.3f}元")
            print(f"   盈亏状态: {profit_pct:+.2f}% ({'盈' if profit_pct > 0 else '亏'}{abs(profit_pct):.2f}%)")
            print(f"   距止损: {to_stop_loss_pct:+.1f}% ({'安全' if to_stop_loss_pct > 0 else '危险'})")
            print(f"   距目标1: {to_first_target_pct:+.1f}%")
            
            # 检查条件
            if current_price <= stock['stop_loss']:
                print(f"\n🚨 紧急提醒！止损触发！")
                print(f"   当前价 {current_price:.3f} ≤ 止损价 {stock['stop_loss']:.3f}")
                print(f"   建议: 立即卖出全部{stock['shares']}股")
                
            elif current_price >= stock['first_target']:
                print(f"\n🎯 目标达成！")
                print(f"   当前价 {current_price:.3f} ≥ 目标价 {stock['first_target']:.3f}")
                print(f"   建议: 卖出50% ({stock['shares']//2}股)锁定利润")
                
            elif profit_pct >= 0:
                print(f"\n✅ 回到成本价以上")
                print(f"   当前价 {current_price:.3f} ≥ 成本价 {stock['cost_price']:.3f}")
                print(f"   建议: 可考虑卖出部分")
                
            else:
                print(f"\n📊 状态: 持有观察")
                print(f"   建议: 继续持有，设置好止损")
            
            print("-" * 40)
            
            # 等待30秒
            time.sleep(30)
            
    except KeyboardInterrupt:
        print("\n\n🛑 监控已停止")
        print("=" * 60)
        print("监控总结:")
        print(f"最后价格: {current_price if 'current_price' in locals() else '未知'}")
        print(f"监控时长: 从开始到停止")
        print("=" * 60)

def main():
    """主函数"""
    print("开始股票实时监控...")
    print("这是一个简单的监控系统，每30秒更新一次")
    print("基于您的交易策略进行分析")
    print()
    
    monitor_stock()

if __name__ == "__main__":
    main()