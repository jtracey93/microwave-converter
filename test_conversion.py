#!/usr/bin/env python3
"""
Simple test script to verify the microwave conversion logic.
"""

import json
import sys
import os

# Add the current directory to the path to import from mcp_server
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_conversion_logic():
    """Test the core conversion logic without MCP dependencies."""
    
    # Test case 1: 1000W to 700W for 2 minutes
    original_wattage = 1000
    target_wattage = 700
    original_minutes = 2
    original_seconds = 0
    
    # Convert original time to total seconds
    original_total_seconds = (original_minutes * 60) + original_seconds
    
    # Apply the conversion formula
    new_total_seconds = round((original_total_seconds * original_wattage) / target_wattage)
    
    # Convert back to minutes and seconds
    new_minutes = new_total_seconds // 60
    new_seconds = new_total_seconds % 60
    
    print(f"Test 1: {original_wattage}W to {target_wattage}W")
    print(f"Original time: {original_minutes}m {original_seconds}s ({original_total_seconds} seconds)")
    print(f"Converted time: {new_minutes}m {new_seconds}s ({new_total_seconds} seconds)")
    print(f"Expected: approximately 2m 51s (171 seconds)")
    print()
    
    # Test case 2: 800W to 1200W for 3 minutes 30 seconds
    original_wattage = 800
    target_wattage = 1200
    original_minutes = 3
    original_seconds = 30
    
    original_total_seconds = (original_minutes * 60) + original_seconds
    new_total_seconds = round((original_total_seconds * original_wattage) / target_wattage)
    new_minutes = new_total_seconds // 60
    new_seconds = new_total_seconds % 60
    
    print(f"Test 2: {original_wattage}W to {target_wattage}W")
    print(f"Original time: {original_minutes}m {original_seconds}s ({original_total_seconds} seconds)")
    print(f"Converted time: {new_minutes}m {new_seconds}s ({new_total_seconds} seconds)")
    print(f"Expected: approximately 2m 20s (140 seconds)")
    print()
    
    # Test power level recommendation
    def get_power_level_recommendation(original_wattage, target_wattage):
        ratio = original_wattage / target_wattage
        
        if ratio > 1.5:
            return {
                "power_level": "70-80%",
                "reason": "Your microwave is much more powerful. Consider using a lower power level."
            }
        elif ratio < 0.7:
            return {
                "power_level": "100%", 
                "reason": "Your microwave is less powerful. Use full power and check frequently."
            }
        else:
            return {
                "power_level": "100%",
                "reason": "Your microwave power is similar to the recipe. Use normal power."
            }
    
    # Test power recommendations
    print("Power level recommendations:")
    print(f"500W to 1000W: {get_power_level_recommendation(500, 1000)}")
    print(f"1200W to 700W: {get_power_level_recommendation(1200, 700)}")
    print(f"800W to 750W: {get_power_level_recommendation(800, 750)}")

if __name__ == "__main__":
    test_conversion_logic()