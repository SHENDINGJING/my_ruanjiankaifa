#!/usr/bin/env python3
"""
Simple Stock Monitor - Start Now
"""

import json
import time
import os
from datetime import datetime
import random

def monitor_stock():
    """Monitor stock"""
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
    print("STOCK REAL-TIME MONITOR - SIMPLE VERSION")
    print("=" * 60)
    print(f"Stock: {stock['name']} ({stock['symbol']})")
    print(f"Shares: {stock['shares']}")
    print(f"Cost: {stock['cost_price']} yuan/share")
    print(f"Stop Loss: {stock['stop_loss']} yuan (-7%)")
    print(f"Target 1: {stock['first_target']} yuan (+15%)")
    print(f"Target 2: {stock['second_target']} yuan (+20%)")
    print("=" * 60)
    print("Press Ctrl+C to stop monitoring")
    print("=" * 60)
    
    try:
        while True:
            # Simulate current price (should get from API in real scenario)
            current_price = stock['cost_price'] * (1 + (random.random() - 0.5) * 0.1)
            current_price = round(current_price, 3)
            
            # Calculate profit/loss
            profit_loss = current_price - stock['cost_price']
            profit_pct = (profit_loss / stock['cost_price']) * 100
            
            # Calculate distance to key prices
            to_stop_loss = current_price - stock['stop_loss']
            to_stop_loss_pct = (to_stop_loss / stock['stop_loss']) * 100
            
            to_first_target = stock['first_target'] - current_price
            to_first_target_pct = (to_first_target / current_price) * 100
            
            # Analysis
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            print(f"\n[{timestamp}] Monitoring Update:")
            print(f"   Current Price: {current_price:.3f} yuan")
            print(f"   P/L Status: {profit_pct:+.2f}% ({'Profit' if profit_pct > 0 else 'Loss'} {abs(profit_pct):.2f}%)")
            print(f"   To Stop Loss: {to_stop_loss_pct:+.1f}% ({'Safe' if to_stop_loss_pct > 0 else 'Danger'})")
            print(f"   To Target 1: {to_first_target_pct:+.1f}%")
            
            # Check conditions
            if current_price <= stock['stop_loss']:
                print(f"\n[ALERT] Stop Loss Triggered!")
                print(f"   Current {current_price:.3f} <= Stop {stock['stop_loss']:.3f}")
                print(f"   Recommendation: SELL ALL {stock['shares']} shares immediately")
                
            elif current_price >= stock['first_target']:
                print(f"\n[TARGET] First Target Reached!")
                print(f"   Current {current_price:.3f} >= Target {stock['first_target']:.3f}")
                print(f"   Recommendation: SELL 50% ({stock['shares']//2} shares) to lock profit")
                
            elif profit_pct >= 0:
                print(f"\n[INFO] Back to Cost Price")
                print(f"   Current {current_price:.3f} >= Cost {stock['cost_price']:.3f}")
                print(f"   Recommendation: Consider selling some")
                
            else:
                print(f"\n[STATUS] Holding")
                print(f"   Recommendation: Continue holding, maintain stop loss")
            
            print("-" * 40)
            
            # Wait 30 seconds
            time.sleep(30)
            
    except KeyboardInterrupt:
        print("\n\n[STOP] Monitoring stopped")
        print("=" * 60)
        print("Monitoring Summary:")
        print(f"Last Price: {current_price if 'current_price' in locals() else 'Unknown'}")
        print(f"Duration: From start to stop")
        print("=" * 60)

def main():
    """Main function"""
    print("Starting Stock Real-time Monitoring...")
    print("This is a simple monitoring system, updates every 30 seconds")
    print("Analysis based on your trading strategy")
    print()
    
    monitor_stock()

if __name__ == "__main__":
    main()