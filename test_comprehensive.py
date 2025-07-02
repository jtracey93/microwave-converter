#!/usr/bin/env python3
"""
Comprehensive test suite for the microwave converter MCP server
"""

import asyncio
from mcp_server import handle_list_tools, handle_call_tool
import json

async def run_comprehensive_tests():
    """Run comprehensive tests for the microwave converter."""
    
    print("🧪 COMPREHENSIVE MICROWAVE CONVERTER TESTS")
    print("=" * 50)
    
    # Test 1: Tool listing
    print("\n1. Testing tool listing...")
    tools = await handle_list_tools()
    assert len(tools) == 1, f"Expected 1 tool, got {len(tools)}"
    assert tools[0].name == "convert_microwave_time", f"Expected tool name 'convert_microwave_time', got {tools[0].name}"
    print("✅ Tool listing test passed")
    
    # Test 2: Basic conversion (1000W to 700W)
    print("\n2. Testing basic conversion (1000W → 700W, 2m 0s)...")
    result = await handle_call_tool("convert_microwave_time", {
        "original_wattage": 1000,
        "target_wattage": 700,
        "original_minutes": 2,
        "original_seconds": 0
    })
    data = json.loads(result[0].text)
    expected_seconds = round((120 * 1000) / 700)  # Should be 171 seconds = 2m 51s
    assert data["converted_time"]["total_seconds"] == expected_seconds, f"Expected {expected_seconds}s, got {data['converted_time']['total_seconds']}s"
    print(f"✅ Converts 2m 0s @ 1000W → {data['converted_time']['formatted']} @ 700W")
    
    # Test 3: Reverse conversion (700W to 1000W)
    print("\n3. Testing reverse conversion (700W → 1000W, 3m 0s)...")
    result = await handle_call_tool("convert_microwave_time", {
        "original_wattage": 700,
        "target_wattage": 1000,
        "original_minutes": 3,
        "original_seconds": 0
    })
    data = json.loads(result[0].text)
    expected_seconds = round((180 * 700) / 1000)  # Should be 126 seconds = 2m 6s
    assert data["converted_time"]["total_seconds"] == expected_seconds, f"Expected {expected_seconds}s, got {data['converted_time']['total_seconds']}s"
    print(f"✅ Converts 3m 0s @ 700W → {data['converted_time']['formatted']} @ 1000W")
    
    # Test 4: Small time conversion (seconds only)
    print("\n4. Testing small time conversion (30 seconds)...")
    result = await handle_call_tool("convert_microwave_time", {
        "original_wattage": 800,
        "target_wattage": 600,
        "original_minutes": 0,
        "original_seconds": 30
    })
    data = json.loads(result[0].text)
    expected_seconds = round((30 * 800) / 600)  # Should be 40 seconds
    assert data["converted_time"]["total_seconds"] == expected_seconds, f"Expected {expected_seconds}s, got {data['converted_time']['total_seconds']}s"
    print(f"✅ Converts 30s @ 800W → {data['converted_time']['formatted']} @ 600W")
    
    # Test 5: Power level recommendations - High power difference
    print("\n5. Testing power recommendations (high power microwave)...")
    result = await handle_call_tool("convert_microwave_time", {
        "original_wattage": 600,
        "target_wattage": 1200,  # Much higher power
        "original_minutes": 2,
        "original_seconds": 0
    })
    data = json.loads(result[0].text)
    assert "70-80%" in data["power_recommendation"]["power_level"], "Should recommend lower power for high-power microwave"
    print(f"✅ Recommends {data['power_recommendation']['power_level']} power for 1200W microwave")
    
    # Test 6: Power level recommendations - Low power difference  
    print("\n6. Testing power recommendations (low power microwave)...")
    result = await handle_call_tool("convert_microwave_time", {
        "original_wattage": 1000,
        "target_wattage": 600,  # Much lower power
        "original_minutes": 2,
        "original_seconds": 0
    })
    data = json.loads(result[0].text)
    assert "100%" in data["power_recommendation"]["power_level"], "Should recommend full power for low-power microwave"
    print(f"✅ Recommends {data['power_recommendation']['power_level']} power for 600W microwave")
    
    # Test 7: Edge case - Very short time (1 second)
    print("\n7. Testing edge case (1 second)...")
    result = await handle_call_tool("convert_microwave_time", {
        "original_wattage": 1000,
        "target_wattage": 800,
        "original_minutes": 0,
        "original_seconds": 1
    })
    data = json.loads(result[0].text)
    print(f"✅ Converts 1s @ 1000W → {data['converted_time']['formatted']} @ 800W")
    
    # Test 8: Error handling - Invalid wattage (too low)
    print("\n8. Testing error handling (wattage too low)...")
    try:
        await handle_call_tool("convert_microwave_time", {
            "original_wattage": 50,  # Too low
            "target_wattage": 700,
            "original_minutes": 2,
            "original_seconds": 0
        })
        assert False, "Should have raised ValueError for low wattage"
    except ValueError as e:
        assert "between 100 and 2000" in str(e), f"Expected wattage error, got: {e}"
        print("✅ Correctly rejects wattage too low")
    
    # Test 9: Error handling - Invalid wattage (too high)
    print("\n9. Testing error handling (wattage too high)...")
    try:
        await handle_call_tool("convert_microwave_time", {
            "original_wattage": 1000,
            "target_wattage": 2500,  # Too high
            "original_minutes": 2,
            "original_seconds": 0
        })
        assert False, "Should have raised ValueError for high wattage"
    except ValueError as e:
        assert "between 100 and 2000" in str(e), f"Expected wattage error, got: {e}"
        print("✅ Correctly rejects wattage too high")
    
    # Test 10: Error handling - Zero time
    print("\n10. Testing error handling (zero time)...")
    try:
        await handle_call_tool("convert_microwave_time", {
            "original_wattage": 1000,
            "target_wattage": 700,
            "original_minutes": 0,
            "original_seconds": 0
        })
        assert False, "Should have raised ValueError for zero time"
    except ValueError as e:
        assert "greater than 0 seconds" in str(e), f"Expected time error, got: {e}"
        print("✅ Correctly rejects zero cooking time")
    
    # Test 11: Error handling - Invalid tool name
    print("\n11. Testing error handling (invalid tool name)...")
    try:
        await handle_call_tool("invalid_tool", {
            "original_wattage": 1000,
            "target_wattage": 700,
            "original_minutes": 2,
            "original_seconds": 0
        })
        assert False, "Should have raised ValueError for invalid tool"
    except ValueError as e:
        assert "Unknown tool" in str(e), f"Expected tool error, got: {e}"
        print("✅ Correctly rejects invalid tool name")
    
    # Test 12: Data integrity - Check all required fields
    print("\n12. Testing data integrity...")
    result = await handle_call_tool("convert_microwave_time", {
        "original_wattage": 900,
        "target_wattage": 1100,
        "original_minutes": 4,
        "original_seconds": 15
    })
    data = json.loads(result[0].text)
    
    required_fields = [
        "converted_time", "original_time", "wattages", 
        "power_recommendation", "explanation"
    ]
    for field in required_fields:
        assert field in data, f"Missing required field: {field}"
    
    # Check nested fields
    assert "formatted" in data["converted_time"], "Missing formatted time"
    assert "ratio" in data["wattages"], "Missing wattage ratio"
    print("✅ All required data fields present")
    
    print("\n" + "=" * 50)
    print("🎉 ALL TESTS PASSED! MCP Server is working correctly!")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(run_comprehensive_tests())
