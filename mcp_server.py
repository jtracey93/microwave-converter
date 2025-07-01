#!/usr/bin/env python3
"""
MCP Server for Microwave Cooking Time Converter

This server provides a single tool to convert microwave cooking times between different wattages.
Uses the same conversion logic as the static web app.
"""

import asyncio
import json
import re
from typing import Any, Dict, Tuple, Optional

from mcp.server import Server
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
        ),
        Tool(
            name="convert_microwave_time_natural",
            description="Convert microwave cooking time using natural language. Ask questions like 'how long do I need to microwave my meal in my 700w microwave when the instructions expect a 950w microwave and a cooking time of 5 minutes'",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Natural language query about microwave time conversion. Should include the original wattage, your microwave's wattage, and the cooking time."
                    }
                },
                "required": ["query"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> list[TextContent]:
    """Handle tool calls."""
    if name == "convert_microwave_time":
        return await handle_structured_conversion(arguments)
    elif name == "convert_microwave_time_natural":
        return await handle_natural_language_conversion(arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")

async def handle_structured_conversion(arguments: Dict[str, Any]) -> list[TextContent]:
    """Handle structured conversion with explicit parameters."""
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
    
    # Perform conversion
    result = perform_conversion(original_wattage, target_wattage, original_minutes, original_seconds)
    return [TextContent(type="text", text=json.dumps(result, indent=2))]

async def handle_natural_language_conversion(arguments: Dict[str, Any]) -> list[TextContent]:
    """Handle natural language conversion by parsing the query."""
    query = arguments.get("query")
    if not query or not isinstance(query, str):
        raise ValueError("Query must be a non-empty string")
    
    # Parse the natural language query
    try:
        original_wattage, target_wattage, original_minutes, original_seconds = parse_natural_language_query(query)
    except ValueError as e:
        raise ValueError(f"Could not parse query: {str(e)}")
    
    # Perform conversion using the extracted parameters
    result = perform_conversion(original_wattage, target_wattage, original_minutes, original_seconds)
    
    # Add the original query for context
    result["original_query"] = query
    result["parsed_parameters"] = {
        "original_wattage": original_wattage,
        "target_wattage": target_wattage,
        "original_minutes": original_minutes,
        "original_seconds": original_seconds
    }
    
    return [TextContent(type="text", text=json.dumps(result, indent=2))]

def parse_natural_language_query(query: str) -> Tuple[float, float, float, float]:
    """Parse natural language query to extract conversion parameters."""
    query_lower = query.lower()
    
    # Extract wattages - be more specific about context
    original_wattage = extract_original_wattage(query_lower)
    target_wattage = extract_target_wattage(query_lower)
    
    # If we couldn't distinguish them clearly, try a different approach
    if original_wattage is None or target_wattage is None:
        all_wattages = extract_all_wattages(query_lower)
        if len(all_wattages) == 2:
            # Try to determine which is which based on context
            original_wattage, target_wattage = determine_wattage_roles(query_lower, all_wattages)
        elif len(all_wattages) == 1:
            # Only one wattage found - we need both
            if original_wattage is None and target_wattage is None:
                # We don't know which one it is
                raise ValueError("Found only one wattage. Please specify both the recipe wattage and your microwave's wattage.")
    
    # Extract time
    original_minutes, original_seconds = extract_time(query_lower)
    
    if original_wattage is None:
        raise ValueError("Could not find the original/recipe wattage in the query. Please specify something like 'recipe expects 950w' or 'instructions say 1000w'")
    
    if target_wattage is None:
        raise ValueError("Could not find your microwave's wattage in the query. Please specify something like 'my 700w microwave' or 'I have a 800w microwave'")
    
    if original_minutes is None and original_seconds is None:
        raise ValueError("Could not find the cooking time in the query. Please specify something like '5 minutes' or '2 minutes 30 seconds'")
    
    # Check if both wattages are the same (likely an error in parsing)
    if original_wattage == target_wattage:
        raise ValueError("Found the same wattage for both recipe and your microwave. Please specify both the recipe wattage and your microwave's wattage clearly.")
    
    # Set defaults
    if original_minutes is None:
        original_minutes = 0
    if original_seconds is None:
        original_seconds = 0
    
    return original_wattage, target_wattage, original_minutes, original_seconds

def extract_all_wattages(query: str) -> list[float]:
    """Extract all wattages mentioned in the query."""
    wattages = []
    pattern = r'(\d+)w'
    matches = re.findall(pattern, query)
    for match in matches:
        wattage = float(match)
        if 100 <= wattage <= 2000:
            wattages.append(wattage)
    return wattages

def determine_wattage_roles(query: str, wattages: list[float]) -> Tuple[float, float]:
    """Determine which wattage is original and which is target."""
    if len(wattages) != 2:
        raise ValueError("Expected exactly 2 wattages")
    
    wattage1, wattage2 = wattages
    
    # Look for context clues before each wattage
    w1_pos = query.find(f"{int(wattage1)}w")
    w2_pos = query.find(f"{int(wattage2)}w")
    
    # Check what comes before each wattage (look at a reasonable context window)
    w1_context = query[max(0, w1_pos-30):w1_pos].lower()
    w2_context = query[max(0, w2_pos-30):w2_pos].lower()
    
    # Keywords that indicate user's microwave
    user_keywords = ['my', 'i have', 'i own', 'using', 'with my', 'in my']
    # Keywords that indicate recipe/original
    recipe_keywords = ['recipe', 'instruction', 'expect', 'call', 'require', 'say']
    
    w1_is_user = any(keyword in w1_context for keyword in user_keywords)
    w2_is_user = any(keyword in w2_context for keyword in user_keywords)
    
    w1_is_recipe = any(keyword in w1_context for keyword in recipe_keywords)
    w2_is_recipe = any(keyword in w2_context for keyword in recipe_keywords)
    
    if w1_is_user and w2_is_recipe:
        return wattage2, wattage1  # original, target
    elif w2_is_user and w1_is_recipe:
        return wattage1, wattage2  # original, target
    elif w1_is_recipe and not w2_is_recipe:
        return wattage1, wattage2  # original, target
    elif w2_is_recipe and not w1_is_recipe:
        return wattage2, wattage1  # original, target
    elif w1_is_user and not w2_is_user:
        return wattage2, wattage1  # original, target
    elif w2_is_user and not w1_is_user:
        return wattage1, wattage2  # original, target
    else:
        # Default: first mentioned is original, second is target
        if w1_pos < w2_pos:
            return wattage1, wattage2
        else:
            return wattage2, wattage1

def extract_original_wattage(query: str) -> Optional[float]:
    """Extract the original/recipe wattage from the query."""
    # Patterns for recipe/original wattage
    patterns = [
        r'(?:recipe|instruction|original|expect|specified?|calls?\s+for|require)s?\s+(?:a\s+)?(\d+)w',
        r'(?:recipe|instruction)s?\s+(?:say|calls?\s+for|require|expect)\s+(?:a\s+)?(\d+)w',
        r'(\d+)w\s+(?:recipe|instruction|microwave)',
        r'instructions?\s+say\s+(\d+)w',
        r'recipe\s+(?:that\s+)?expects?\s+(\d+)w'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, query)
        if match:
            wattage = float(match.group(1))
            if 100 <= wattage <= 2000:
                return wattage
    
    return None

def extract_target_wattage(query: str) -> Optional[float]:
    """Extract the target/user's microwave wattage from the query."""
    # Patterns for user's microwave wattage
    patterns = [
        r'(?:my|i have|i own|using|i.*have)\s+(?:a\s+)?(\d+)w\s+microwave',
        r'(?:my|i have|i own|using)\s+(?:a\s+)?microwave\s+(?:is\s+)?(\d+)w',
        r'(?:in|with)\s+(?:a\s+)?(\d+)w\s+microwave',
        r'(\d+)w\s+(?:microwave\s+)?(?:that\s+)?(?:i|we)\s+(?:have|own|use)',
        r'my\s+microwave\s+is\s+(\d+)w',
        r'i\s+own\s+a\s+(\d+)w\s+microwave'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, query)
        if match:
            wattage = float(match.group(1))
            if 100 <= wattage <= 2000:
                return wattage
    
    return None

def extract_time(query: str) -> Tuple[Optional[float], Optional[float]]:
    """Extract cooking time from the query."""
    minutes = None
    seconds = None
    
    # Pattern for "X minutes and Y seconds" or "X minutes Y seconds"
    time_pattern = r'(\d+(?:\.\d+)?)\s*(?:minute|min)s?\s*(?:and\s+)?(?:(\d+(?:\.\d+)?)\s*(?:second|sec)s?)?'
    match = re.search(time_pattern, query)
    if match:
        minutes = float(match.group(1))
        if match.group(2):
            seconds = float(match.group(2))
        else:
            seconds = 0
        return minutes, seconds
    
    # Pattern for "90 seconds" - convert to minutes and seconds
    seconds_only_pattern = r'(\d+(?:\.\d+)?)\s*(?:second|sec)s?(?:\s|$|,|\.)'
    match = re.search(seconds_only_pattern, query)
    if match:
        total_seconds = float(match.group(1))
        if total_seconds >= 60:
            minutes = total_seconds // 60
            seconds = total_seconds % 60
        else:
            minutes = 0
            seconds = total_seconds
        return minutes, seconds
    
    return None, None

def perform_conversion(original_wattage: float, target_wattage: float, original_minutes: float, original_seconds: float) -> Dict[str, Any]:
    """Perform the microwave time conversion."""
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
    
    return result


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
                    notification_options=None,
                    experimental_capabilities=None,
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())