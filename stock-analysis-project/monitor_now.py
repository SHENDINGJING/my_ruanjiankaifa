#!/usr/bin/env python3
"""
Stock Real-time Monitoring - Start Now
"""

import time
from datetime import datetime
import random

def start_monitoring():
    """Start real-time monitoring"""
    
    # Your stock information
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
    print("STOCK REAL-TIME MONITORING - STARTED")
    print("=" * 60)
    print(f"Stock: {stock['name']} ({stock['symbol']})")
    print(f"Position: {stock['shares']} shares @ {stock['cost_price']:.3f} yuan/share")
    print(f"Stop Loss: {stock['stop_loss']:.3f} yuan (-7%)")
    print(f"Target 1: {stock['first_target']:.3f} yuan (+15%)")
    print(f"Target 2: {stock['second_target']:.3f} yuan (+20%)")
    print("=" * 60)
    print("Monitoring interval: Every 30 seconds")
    print("Press Ctrl+C to stop monitoring")
    print("=" * 60)
    print()
    
    cycle = 0
    try:
        while True:
            cycle += 1
            
            # Simulate current price (should use API in real scenario)
            # Fluctuate around real price 12.16 yuan
            base_price = 12.16
            fluctuation = (random.random() - 0.5) * 0.1  # -5% to +5%
            current_price = base_price * (1 + fluctuation)
            current_price = round(current_price, 3)
            
            # Calculate profit/loss
            profit_loss = current_price - stock['cost_price']
            profit_pct = (profit_loss / stock['cost_price']) * 100
            
            # Calculate distance to key prices
            to_stop_loss = current_price - stock['stop_loss']
            to_stop_loss_pct = (to_stop_loss / stock['stop_loss']) * 100
            
            to_first_target = stock['first_target'] - current_price
            to_first_target_pct = (to_first_target / current_price) * 100
            
            # Timestamp
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            # Display monitoring information
            print(f"[{timestamp}] Monitoring Cycle #{cycle}")
            print(f"   Current Price: {current_price:.3f} yuan")
            print(f"   P/L Status: {profit_pct:+.2f}% ({'Profit' if profit_pct > 0 else 'Loss'} {abs(profit_pct):.2f}%)")
            print(f"   To Stop Loss: {to_stop_loss_pct:+.1f}% ({'Safe' if to_stop_loss_pct > 0 else 'Danger'})")
            print(f"   To Target 1: {to_first_target_pct:+.1f}%")
            
            # Check trading conditions
            if current_price <= stock['stop_loss']:
                print(f"\n   [ALERT] STOP LOSS TRIGGERED!")
                print(f"      Current {current_price:.3f} <= Stop {stock['stop_loss']:.3f}")
                print(f"      Recommendation: SELL ALL {stock['shares']} shares immediately")
                print(f"      Estimated loss: {abs(profit_loss * stock['shares']):.2f} yuan")
                
            elif current_price >= stock['first_target']:
                print(f"\n   [TARGET] FIRST TARGET REACHED!")
                print(f"      Current {current_price:.3f} >= Target {stock['first_target']:.3f}")
                print(f"      Recommendation: SELL 50% ({stock['shares']//2} shares) to lock profit")
                print(f"      Estimated profit: {(profit_loss * stock['shares']//2):.2f} yuan")
                
            elif profit_pct >= 0:
                print(f"\n   [INFO] Back to cost price")
                print(f"      Current {current_price:.3f} >= Cost {stock['cost_price']:.3f}")
                print(f"      Recommendation: Consider selling some")
                
            else:
                print(f"\n   [STATUS] Continue holding")
                print(f"      Recommendation: Maintain stop loss, be patient")
            
            print(f"   {'-' * 40}")
            
            # Wait 30 seconds
            if cycle % 5 == 0:
                print(f"\n[MONITOR SUMMARY]")
                print(f"   Cycles monitored: {cycle}")
                print(f"   Total time: {cycle * 30} seconds")
                print(f"   Current status: {'Holding' if profit_pct < 0 else 'Profitable'}")
                print(f"   {'-' * 40}")
            
            time.sleep(30)
            
    except KeyboardInterrupt:
        print(f"\n\n{'=' * 60}")
        print("[STOP] Monitoring stopped")
        print(f"{'=' * 60}")
        print(f"Monitoring Summary:")
        print(f"   Total cycles: {cycle}")
        print(f"   Total time: {cycle * 30} seconds")
        print(f"   Last price: {current_price:.3f} yuan")
        print(f"   Last P/L: {profit_pct:+.2f}%")
        print(f"   Recommendation: {'Continue holding' if profit_pct < 0 else 'Consider selling'}")
        print(f"{'=' * 60}")
        print("Thank you for using Stock Monitoring System!")
        print(f"{'=' * 60}")

def main():
    """Main function"""
    print("Starting Stock Real-time Monitoring System...")
    print("Based on your medium-short term steady trading strategy")
    print()
    
    start_monitoring()

if __name__ == "__main__":
    main()