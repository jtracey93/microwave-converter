#!/usr/bin/env python3
"""
Standalone test to validate the microwave conversion functionality without MCP dependencies.
"""

import json

def convert_microwave_time(original_wattage, target_wattage, original_minutes, original_seconds):
    """
    Convert microwave cooking time from one wattage to another.
    Uses the same logic as the web app and MCP server.
    """
    # Validate inputs
    if not all(isinstance(x, (int, float)) for x in [original_wattage, target_wattage, original_minutes, original_seconds]):
        raise ValueError("All parameters must be numbers")
    
    if original_wattage < 100 or original_wattage > 2000:
        raise ValueError("Original wattage must be between 100 and 2000 watts")
    
    if target_wattage < 100 or target_wattage > 2000:
        raise ValueError("Target wattage must be between 100 and 2000 watts")
        
    if original_minutes < 0 or original_minutes > 60:
        raise ValueError("Minutes must be between 0 and 60")
        
    if original_seconds < 0 or original_seconds > 59:
        raise ValueError("Seconds must be between 0 and 59")
    
    # Convert original time to total seconds
    original_total_seconds = (original_minutes * 60) + original_seconds
    
    if original_total_seconds == 0:
        raise ValueError("Cooking time must be greater than 0 seconds")
    
    # Apply the conversion formula: New Time = (Original Time × Recipe Wattage) ÷ Your Wattage
    new_total_seconds = round((original_total_seconds * original_wattage) / target_wattage)
    
    # Convert back to minutes and seconds
    new_minutes = new_total_seconds // 60
    new_seconds = new_total_seconds % 60
    
    # Calculate ratio for additional insights
    ratio = original_wattage / target_wattage
    
    # Format time strings for display
    original_time_str = format_time(original_minutes, original_seconds)
    new_time_str = format_time(new_minutes, new_seconds)
    
    # Get power level recommendation
    power_recommendation = get_power_level_recommendation(original_wattage, target_wattage)
    
    # Create result
    result = {
        "converted_time": {
            "minutes": new_minutes,
            "seconds": new_seconds,
            "total_seconds": new_total_seconds,
            "formatted": new_time_str
        },
        "original_time": {
            "minutes": original_minutes,
            "seconds": original_seconds, 
            "total_seconds": original_total_seconds,
            "formatted": original_time_str
        },
        "wattages": {
            "original": original_wattage,
            "target": target_wattage,
            "ratio": round(ratio, 2)
        },
        "power_recommendation": power_recommendation,
        "explanation": f"Cook for {new_time_str} instead of {original_time_str} when using a {target_wattage}W microwave instead of {original_wattage}W"
    }
    
    return result

def format_time(minutes, seconds):
    """Format time in a readable way."""
    if minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"

def get_power_level_recommendation(original_wattage, target_wattage):
    """Get power level recommendations based on wattage difference."""
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

def main():
    """Test the conversion functionality with various scenarios."""
    print("Testing Microwave Time Conversion Tool")
    print("=" * 50)
    
    # Test cases that match common usage scenarios
    test_cases = [
        {
            "name": "High to Low Power (1000W to 700W, 2 minutes)",
            "original_wattage": 1000,
            "target_wattage": 700,
            "original_minutes": 2,
            "original_seconds": 0
        },
        {
            "name": "Low to High Power (800W to 1200W, 3m 30s)",
            "original_wattage": 800,
            "target_wattage": 1200,
            "original_minutes": 3,
            "original_seconds": 30
        },
        {
            "name": "Similar Power (900W to 850W, 1m 45s)",
            "original_wattage": 900,
            "target_wattage": 850,
            "original_minutes": 1,
            "original_seconds": 45
        },
        {
            "name": "Very Different Power (1200W to 600W, 1 minute)",
            "original_wattage": 1200,
            "target_wattage": 600,
            "original_minutes": 1,
            "original_seconds": 0
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['name']}")
        print("-" * 30)
        
        try:
            result = convert_microwave_time(
                test_case["original_wattage"],
                test_case["target_wattage"], 
                test_case["original_minutes"],
                test_case["original_seconds"]
            )
            
            print(f"Input: {result['original_time']['formatted']} at {result['wattages']['original']}W")
            print(f"Output: {result['converted_time']['formatted']} at {result['wattages']['target']}W")
            print(f"Power Level: {result['power_recommendation']['power_level']}")
            print(f"Reason: {result['power_recommendation']['reason']}")
            print(f"Ratio: {result['wattages']['ratio']}")
            
        except Exception as e:
            print(f"Error: {e}")
    
    # Test error cases
    print(f"\n\nTesting Error Cases")
    print("=" * 30)
    
    error_cases = [
        {"original_wattage": 50, "target_wattage": 700, "original_minutes": 2, "original_seconds": 0, "expected": "wattage too low"},
        {"original_wattage": 1000, "target_wattage": 2500, "original_minutes": 2, "original_seconds": 0, "expected": "wattage too high"},
        {"original_wattage": 1000, "target_wattage": 700, "original_minutes": 0, "original_seconds": 0, "expected": "zero time"},
        {"original_wattage": 1000, "target_wattage": 700, "original_minutes": -1, "original_seconds": 0, "expected": "negative time"},
    ]
    
    for i, test_case in enumerate(error_cases, 1):
        print(f"\nError Test {i}: {test_case['expected']}")
        try:
            convert_microwave_time(
                test_case["original_wattage"],
                test_case["target_wattage"], 
                test_case["original_minutes"],
                test_case["original_seconds"]
            )
            print("ERROR: Should have thrown an exception!")
        except Exception as e:
            print(f"✓ Correctly caught error: {e}")
    
    print("\n\nAll tests completed!")

if __name__ == "__main__":
    main()