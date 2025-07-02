# Microwave Converter MCP Server

A Model Context Protocol (MCP) server that provides microwave cooking time conversion between different wattages.

## Features

- Convert cooking times between different microwave wattages
- Smart power level recommendations based on wattage differences
- Comprehensive input validation
- Detailed conversion results with explanations

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the MCP Server

```bash
python mcp_server.py
```

The server communicates via stdin/stdout using the MCP protocol.

### Available Tools

#### `convert_microwave_time`

Converts microwave cooking time from one wattage to another.

**Parameters:**
- `original_wattage` (number): The wattage specified in the recipe (100-2000 watts)
- `target_wattage` (number): Your microwave's wattage (100-2000 watts)  
- `original_minutes` (number): Original cooking time in minutes (0-60)
- `original_seconds` (number): Original cooking time in seconds (0-59)

**Returns:**
- Converted cooking time (minutes and seconds)
- Power level recommendations
- Conversion ratio and explanation
- Formatted time strings

### Example Conversion

Converting a recipe that calls for 2 minutes at 1000W to work with a 700W microwave:

```json
{
  "converted_time": {
    "minutes": 2,
    "seconds": 51,
    "total_seconds": 171,
    "formatted": "2m 51s"
  },
  "original_time": {
    "minutes": 2,
    "seconds": 0,
    "total_seconds": 120,
    "formatted": "2m 0s"
  },
  "wattages": {
    "original": 1000,
    "target": 700,
    "ratio": 1.43
  },
  "power_recommendation": {
    "power_level": "100%",
    "reason": "Your microwave power is similar to the recipe. Use normal power."
  },
  "explanation": "Cook for 2m 51s instead of 2m 0s when using a 700W microwave instead of 1000W"
}
```

## Power Level Recommendations

The server provides intelligent power level recommendations:

- **70-80% Power**: When your microwave is much more powerful than the recipe (>1.5x)
- **100% Power**: When your microwave is similar or less powerful than the recipe

## Testing

Run the test suite to verify functionality:

```bash
# Basic functionality test
python test_mcp_server.py

# Comprehensive test suite
python test_comprehensive.py

# MCP protocol test
python test_mcp_client.py
```

## Conversion Formula

The conversion uses the formula:
```
New Time = (Original Time × Recipe Wattage) ÷ Your Wattage
```

This ensures proper energy delivery for consistent cooking results.

## Error Handling

The server validates all inputs:
- Wattage must be between 100-2000 watts
- Time must be greater than 0 seconds
- All parameters must be numeric

## Requirements

- Python 3.7+
- mcp >= 1.0.0

## License

MIT License - see LICENSE file for details.
