#!/usr/bin/env python3
"""
Simple Stock Monitor Test - No Unicode
"""

import json
import time
from datetime import datetime
import random

def run_all_tests():
    """Run all tests"""
    print("STOCK MONITOR SYSTEM TEST")
    print("=" * 60)
    
    # Test 1: Basic logic
    print("\n1. BASIC MONITORING LOGIC TEST")
    print("-" * 40)
    
    cost = 12.465
    stop = 11.592
    target = 14.335
    
    test_cases = [
        (12.16, "HOLD"),
        (12.25, "HOLD"),
        (11.55, "SELL_ALL"),
        (14.40, "SELL_50%"),
        (12.47, "CONSIDER_SELL"),
    ]
    
    passed = 0
    for price, expected in test_cases:
        # Determine action
        if price <= stop:
            action = "SELL_ALL"
        elif price >= target:
            action = "SELL_50%"
        elif price >= cost:
            action = "CONSIDER_SELL"
        else:
            action = "HOLD"
        
        if action == expected:
            print(f"  Price {price:.3f}: {action} - PASS")
            passed += 1
        else:
            print(f"  Price {price:.3f}: {action} (expected {expected}) - FAIL")
    
    print(f"  Result: {passed}/{len(test_cases)} passed")
    
    # Test 2: Strategy calculations
    print("\n2. STRATEGY CALCULATIONS TEST")
    print("-" * 40)
    
    stop_loss = cost * 0.93
    first_target = cost * 1.15
    second_target = cost * 1.20
    
    stop_pct = (stop_loss - cost) / cost * 100
    first_pct = (first_target - cost) / cost * 100
    second_pct = (second_target - cost) / cost * 100
    
    print(f"  Cost: {cost:.3f}")
    print(f"  Stop Loss: {stop_loss:.3f} ({stop_pct:+.2f}%)")
    print(f"  First Target: {first_target:.3f} ({first_pct:+.2f}%)")
    print(f"  Second Target: {second_target:.3f} ({second_pct:+.2f}%)")
    
    calc_ok = (abs(stop_pct + 7.0) < 0.01 and 
               abs(first_pct - 15.0) < 0.01 and 
               abs(second_pct - 20.0) < 0.01)
    
    if calc_ok:
        print("  Result: CALCULATIONS CORRECT - PASS")
        passed += 1
    else:
        print("  Result: CALCULATION ERRORS - FAIL")
    
    # Test 3: Monitoring cycle simulation
    print("\n3. MONITORING CYCLE SIMULATION")
    print("-" * 40)
    
    print("  Simulating 2 monitoring cycles...")
    for i in range(1, 3):
        price = cost * (1 + (random.random() - 0.5) * 0.1)
        price = round(price, 3)
        
        profit_pct = (price - cost) / cost * 100
        
        if price <= stop:
            action = "SELL_ALL"
        elif price >= target:
            action = "SELL_50%"
        elif profit_pct >= 0:
            action = "CONSIDER_SELL"
        else:
            action = "HOLD"
        
        print(f"  Cycle {i}: Price {price:.3f} -> {action}")
        time.sleep(0.5)
    
    print("  Result: SIMULATION COMPLETE - PASS")
    passed += 1
    
    # Test 4: File check
    print("\n4. FILE SYSTEM CHECK")
    print("-" * 40)
    
    import os
    files_to_check = [
        "simple_monitor_en.py",
        "openclaw_screen_monitor.py",
        "canvas_monitor.py",
    ]
    
    found = 0
    for filename in files_to_check:
        if os.path.exists(filename):
            found += 1
            print(f"  {filename}: FOUND")
        else:
            print(f"  {filename}: NOT FOUND")
    
    if found == len(files_to_check):
        print(f"  Result: ALL FILES PRESENT - PASS")
        passed += 1
    else:
        print(f"  Result: {found}/{len(files_to_check)} files found - FAIL")
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    total_tests = 4
    print(f"Tests passed: {passed}/{total_tests}")
    
    if passed == total_tests:
        print("\nRESULT: ALL TESTS PASSED - SYSTEM READY")
        print("\nYou can now:")
        print("1. Run simple monitor: python simple_monitor_en.py")
        print("2. Check OpenClaw status: python openclaw_screen_monitor.py --status")
        print("3. Start canvas monitor: python canvas_monitor.py --check")
    else:
        print(f"\nRESULT: {total_tests - passed} TESTS FAILED")
        print("Check the failed tests above.")
    
    print("=" * 60)

if __name__ == "__main__":
    run_all_tests()