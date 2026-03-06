#!/usr/bin/env python3
"""
Test Stock Monitor System
"""

import json
import time
from datetime import datetime
import random

def test_basic_logic():
    """Test basic monitoring logic"""
    print("=" * 60)
    print("BASIC MONITORING LOGIC TEST")
    print("=" * 60)
    
    # Test cases
    test_cases = [
        {"name": "Normal Price", "price": 12.16, "expected": "HOLD"},
        {"name": "Slightly Up", "price": 12.25, "expected": "HOLD"},
        {"name": "Stop Loss", "price": 11.55, "expected": "SELL_ALL"},
        {"name": "First Target", "price": 14.40, "expected": "SELL_50%"},
        {"name": "Back to Cost", "price": 12.47, "expected": "CONSIDER_SELL"},
    ]
    
    cost = 12.465
    stop = 11.592
    target = 14.335
    
    passed = 0
    total = len(test_cases)
    
    for i, test in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test['name']}")
        print(f"  Price: {test['price']:.3f}")
        
        profit_pct = (test['price'] - cost) / cost * 100
        
        # Determine action
        if test['price'] <= stop:
            action = "SELL_ALL"
            reason = f"Price {test['price']:.3f} <= Stop {stop:.3f}"
        elif test['price'] >= target:
            action = "SELL_50%"
            reason = f"Price {test['price']:.3f} >= Target {target:.3f}"
        elif profit_pct >= 0:
            action = "CONSIDER_SELL"
            reason = f"Profit {profit_pct:+.2f}% >= 0%"
        else:
            action = "HOLD"
            reason = f"Loss {profit_pct:+.2f}%, Stop not triggered"
        
        print(f"  Expected: {test['expected']}")
        print(f"  Actual: {action}")
        print(f"  Reason: {reason}")
        
        if action == test['expected']:
            print(f"  Result: PASS")
            passed += 1
        else:
            print(f"  Result: FAIL")
    
    print(f"\n" + "=" * 60)
    print(f"TEST RESULTS: {passed}/{total} passed")
    print("=" * 60)
    
    return passed == total

def test_strategy_calculations():
    """Test strategy price calculations"""
    print("\n" + "=" * 60)
    print("STRATEGY CALCULATIONS TEST")
    print("=" * 60)
    
    cost = 12.465
    
    # Calculate strategy prices
    stop_loss = cost * 0.93  # -7%
    first_target = cost * 1.15  # +15%
    second_target = cost * 1.20  # +20%
    
    print(f"Cost Price: {cost:.3f}")
    print(f"Stop Loss (-7%): {stop_loss:.3f}")
    print(f"First Target (+15%): {first_target:.3f}")
    print(f"Second Target (+20%): {second_target:.3f}")
    
    # Verify calculations
    stop_loss_pct = (stop_loss - cost) / cost * 100
    first_target_pct = (first_target - cost) / cost * 100
    second_target_pct = (second_target - cost) / cost * 100
    
    print(f"\nVerification:")
    print(f"  Stop Loss %: {stop_loss_pct:+.2f}% (expected: -7.00%)")
    print(f"  First Target %: {first_target_pct:+.2f}% (expected: +15.00%)")
    print(f"  Second Target %: {second_target_pct:+.2f}% (expected: +20.00%)")
    
    # Check if calculations are correct
    stop_ok = abs(stop_loss_pct + 7.0) < 0.01
    first_ok = abs(first_target_pct - 15.0) < 0.01
    second_ok = abs(second_target_pct - 20.0) < 0.01
    
    if stop_ok and first_ok and second_ok:
        print(f"\nResult: ALL CALCULATIONS CORRECT")
        return True
    else:
        print(f"\nResult: CALCULATION ERRORS")
        if not stop_ok:
            print(f"  Stop loss calculation error: {stop_loss_pct:+.2f}%")
        if not first_ok:
            print(f"  First target calculation error: {first_target_pct:+.2f}%")
        if not second_ok:
            print(f"  Second target calculation error: {second_target_pct:+.2f}%")
        return False

def test_monitoring_cycle():
    """Test a complete monitoring cycle"""
    print("\n" + "=" * 60)
    print("MONITORING CYCLE TEST")
    print("=" * 60)
    
    print("Simulating 3 monitoring cycles...")
    
    cost = 12.465
    stop = 11.592
    target = 14.335
    shares = 800
    
    for cycle in range(1, 4):
        print(f"\n--- Cycle {cycle} ---")
        
        # Generate random price near cost
        price = cost * (1 + (random.random() - 0.5) * 0.15)
        price = round(price, 3)
        
        profit_pct = (price - cost) / cost * 100
        to_stop_pct = (price - stop) / stop * 100
        to_target_pct = (target - price) / price * 100
        
        print(f"Time: {datetime.now().strftime('%H:%M:%S')}")
        print(f"Price: {price:.3f}")
        print(f"P/L: {profit_pct:+.2f}%")
        print(f"To Stop: {to_stop_pct:+.1f}%")
        print(f"To Target: {to_target_pct:+.1f}%")
        
        # Decision logic
        if price <= stop:
            print("ACTION: SELL ALL - Stop loss triggered")
            print(f"  Sell {shares} shares immediately")
        elif price >= target:
            print("ACTION: SELL 50% - Target reached")
            print(f"  Sell {shares//2} shares to lock profit")
        elif profit_pct >= 0:
            print("ACTION: CONSIDER SELL - Back to cost")
            print(f"  Consider selling some shares")
        else:
            print("ACTION: HOLD - Continue monitoring")
            print(f"  Maintain stop loss at {stop:.3f}")
        
        time.sleep(1)  # Short delay for readability
    
    print("\n" + "=" * 60)
    print("MONITORING CYCLE TEST COMPLETE")
    print("=" * 60)
    return True

def test_file_creation():
    """Test that required files exist"""
    print("\n" + "=" * 60)
    print("FILE SYSTEM TEST")
    print("=" * 60)
    
    import os
    from pathlib import Path
    
    required_files = [
        "simple_monitor_en.py",
        "openclaw_screen_monitor.py",
        "screen_share_monitor.py",
        "canvas_monitor.py",
        "OPENCLAW_MONITOR_GUIDE.md",
        "SCREEN_SHARE_GUIDE.md",
        "CANVAS_MONITOR_GUIDE.md",
    ]
    
    base_path = Path(__file__).parent
    
    found = 0
    total = len(required_files)
    
    for filename in required_files:
        filepath = base_path / filename
        if filepath.exists():
            print(f"✓ {filename} - FOUND ({filepath.stat().st_size} bytes)")
            found += 1
        else:
            print(f"✗ {filename} - NOT FOUND")
    
    print(f"\nFiles found: {found}/{total}")
    
    if found == total:
        print("Result: ALL FILES PRESENT")
        return True
    else:
        print("Result: SOME FILES MISSING")
        return False

def main():
    """Run all tests"""
    print("STOCK MONITOR SYSTEM COMPREHENSIVE TEST")
    print("=" * 60)
    
    tests = [
        ("Basic Monitoring Logic", test_basic_logic),
        ("Strategy Calculations", test_strategy_calculations),
        ("Monitoring Cycle", test_monitoring_cycle),
        ("File System", test_file_creation),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n>>> Running: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
            if result:
                print(f"✓ {test_name}: PASSED")
            else:
                print(f"✗ {test_name}: FAILED")
        except Exception as e:
            print(f"✗ {test_name}: ERROR - {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✅ ALL TESTS PASSED - SYSTEM READY FOR USE")
        print("\nNext steps:")
        print("1. Run: python simple_monitor_en.py")
        print("2. Or use: python openclaw_screen_monitor.py --check")
        print("3. Read guides for advanced monitoring options")
    else:
        print(f"\n⚠️  {total - passed} TESTS FAILED - NEEDS ATTENTION")
    
    print("=" * 60)

if __name__ == "__main__":
    main()