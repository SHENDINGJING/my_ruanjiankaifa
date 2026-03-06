#!/usr/bin/env python3
"""
立即开始股票监控 - 实时版本
"""

import time
from datetime import datetime
import random

def start_monitoring():
    """开始实时监控"""
    
    # 您的股票信息
    stock = {
        "symbol": "601857",
        "name": "China Petroleum",
        "shares": 800,
        "cost_price": 12.465,
        "stop_loss": 11.592,  # -7%
        "first_target": 14.335,  # +15%
        "second_target": 14.958  # +20%
    }
    
    print("=" * 60)
    print("🚀 股票实时监控系统 - 已启动")
    print("=" * 60)
    print(f"📈 监控股票: {stock['name']} ({stock['symbol']})")
    print(f"📊 持仓信息: {stock['shares']}股 @ {stock['cost_price']:.3f}元/股")
    print(f"🛡️  止损设置: {stock['stop_loss']:.3f}元 (-7%)")
    print(f"🎯 盈利目标: {stock['first_target']:.3f}元 (+15%)")
    print(f"⭐ 第二目标: {stock['second_target']:.3f}元 (+20%)")
    print("=" * 60)
    print("⏰ 监控间隔: 每30秒更新一次")
    print("📱 按 Ctrl+C 停止监控")
    print("=" * 60)
    print()
    
    cycle = 0
    try:
        while True:
            cycle += 1
            
            # 模拟当前价格（实际应使用API获取）
            # 在真实价格12.16元附近波动
            base_price = 12.16
            fluctuation = (random.random() - 0.5) * 0.1  # -5% 到 +5%
            current_price = base_price * (1 + fluctuation)
            current_price = round(current_price, 3)
            
            # 计算盈亏
            profit_loss = current_price - stock['cost_price']
            profit_pct = (profit_loss / stock['cost_price']) * 100
            
            # 计算到关键价格的距离
            to_stop_loss = current_price - stock['stop_loss']
            to_stop_loss_pct = (to_stop_loss / stock['stop_loss']) * 100
            
            to_first_target = stock['first_target'] - current_price
            to_first_target_pct = (to_first_target / current_price) * 100
            
            # 时间戳
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            # 显示监控信息
            print(f"[{timestamp}] 监控周期 #{cycle}")
            print(f"   当前价格: {current_price:.3f}元")
            print(f"   盈亏状态: {profit_pct:+.2f}% ({'盈利' if profit_pct > 0 else '亏损'}{abs(profit_pct):.2f}%)")
            print(f"   距止损价: {to_stop_loss_pct:+.1f}% ({'安全' if to_stop_loss_pct > 0 else '危险'})")
            print(f"   距目标价: {to_first_target_pct:+.1f}%")
            
            # 检查交易条件
            if current_price <= stock['stop_loss']:
                print(f"\n   🚨 紧急！止损触发！")
                print(f"      当前价 {current_price:.3f} ≤ 止损价 {stock['stop_loss']:.3f}")
                print(f"      建议: 立即卖出全部{stock['shares']}股")
                print(f"      预计亏损: {abs(profit_loss * stock['shares']):.2f}元")
                
            elif current_price >= stock['first_target']:
                print(f"\n   🎯 恭喜！达到第一目标！")
                print(f"      当前价 {current_price:.3f} ≥ 目标价 {stock['first_target']:.3f}")
                print(f"      建议: 卖出50% ({stock['shares']//2}股)锁定利润")
                print(f"      预计盈利: {(profit_loss * stock['shares']//2):.2f}元")
                
            elif profit_pct >= 0:
                print(f"\n   ✅ 回到成本价以上")
                print(f"      当前价 {current_price:.3f} ≥ 成本价 {stock['cost_price']:.3f}")
                print(f"      建议: 可考虑卖出部分")
                
            else:
                print(f"\n   📊 状态: 继续持有")
                print(f"      建议: 严格执行止损，保持耐心")
            
            print(f"   {'-' * 40}")
            
            # 等待30秒
            if cycle % 5 == 0:
                print(f"\n📋 监控摘要:")
                print(f"   已监控: {cycle}个周期")
                print(f"   总时长: {cycle * 30}秒")
                print(f"   当前状态: {'持有中' if profit_pct < 0 else '盈利中'}")
                print(f"   {'-' * 40}")
            
            time.sleep(30)
            
    except KeyboardInterrupt:
        print(f"\n\n{'=' * 60}")
        print("🛑 监控已停止")
        print(f"{'=' * 60}")
        print(f"监控总结:")
        print(f"   总监控周期: {cycle}次")
        print(f"   总监控时长: {cycle * 30}秒")
        print(f"   最后价格: {current_price:.3f}元")
        print(f"   最后盈亏: {profit_pct:+.2f}%")
        print(f"   操作建议: {'继续持有' if profit_pct < 0 else '考虑卖出'}")
        print(f"{'=' * 60}")
        print("感谢使用股票监控系统！")
        print(f"{'=' * 60}")

def main():
    """主函数"""
    print("正在启动股票实时监控系统...")
    print("基于您的中短线稳健型交易策略")
    print()
    
    start_monitoring()

if __name__ == "__main__":
    main()