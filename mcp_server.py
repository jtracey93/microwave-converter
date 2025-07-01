#!/usr/bin/env python3
"""
MCP Server for Microwave Cooking Time Converter

This server provides a single tool to convert microwave cooking times between different wattages.
Uses the same conversion logic as the static web app.
"""

import asyncio
import json
from typing import Any, Dict

from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequestParams,
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)

# Initialize the MCP server
server = Server("microwave-converter")

@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="convert_microwave_time",
            description="Convert microwave cooking time from one wattage to another",
            inputSchema={
                "type": "object",
                "properties": {
                    "original_wattage": {
                        "type": "number",
                        "description": "The wattage specified in the recipe (watts)",
                        "minimum": 100,
                        "maximum": 2000
                    },
                    "target_wattage": {
                        "type": "number", 
                        "description": "Your microwave's wattage (watts)",
                        "minimum": 100,
                        "maximum": 2000
                    },
                    "original_minutes": {
                        "type": "number",
                        "description": "Original cooking time in minutes",
                        "minimum": 0,
                        "maximum": 60
                    },
                    "original_seconds": {
                        "type": "number",
                        "description": "Original cooking time in seconds",
                        "minimum": 0,
                        "maximum": 59
                    }
                },
                "required": ["original_wattage", "target_wattage", "original_minutes", "original_seconds"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> list[TextContent]:
    """Handle tool calls."""
    if name != "convert_microwave_time":
        raise ValueError(f"Unknown tool: {name}")
    
    # Extract and validate parameters
    original_wattage = arguments.get("original_wattage")
    target_wattage = arguments.get("target_wattage")
    original_minutes = arguments.get("original_minutes")
    original_seconds = arguments.get("original_seconds")
    
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
    
    # Perform the conversion using the same logic as the web app
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
    
    # Create result message
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
    
    return [TextContent(type="text", text=json.dumps(result, indent=2))]


def format_time(minutes: int, seconds: int) -> str:
    """Format time in a readable way."""
    if minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"

def get_power_level_recommendation(original_wattage: float, target_wattage: float) -> Dict[str, str]:
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

async def main():
    """Run the server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="microwave-converter",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities=None,
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())