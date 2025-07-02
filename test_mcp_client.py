#!/usr/bin/env python3
"""
Simple MCP client to test the microwave converter server
"""

import asyncio
import json
import subprocess
import sys
from typing import Any, Dict

async def test_mcp_server():
    """Test the MCP server using the actual MCP protocol."""
    
    # Start the MCP server as a subprocess
    server_process = subprocess.Popen(
        [sys.executable, "mcp_server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd="."
    )
    
    try:
        # Initialize the server
        init_message = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        print("Sending initialize message...")
        server_process.stdin.write(json.dumps(init_message) + "\n")
        server_process.stdin.flush()
        
        # Read response
        response_line = server_process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            print(f"Initialize response: {json.dumps(response, indent=2)}")
        
        # Send initialized notification
        initialized_notification = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized"
        }
        
        print("\nSending initialized notification...")
        server_process.stdin.write(json.dumps(initialized_notification) + "\n")
        server_process.stdin.flush()
        
        # List tools
        list_tools_message = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list"
        }
        
        print("\nListing tools...")
        server_process.stdin.write(json.dumps(list_tools_message) + "\n")
        server_process.stdin.flush()
        
        # Read tools response
        response_line = server_process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            print(f"Tools list response: {json.dumps(response, indent=2)}")
        
        # Call the conversion tool
        call_tool_message = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "convert_microwave_time",
                "arguments": {
                    "original_wattage": 800,
                    "target_wattage": 1000,
                    "original_minutes": 3,
                    "original_seconds": 30
                }
            }
        }
        
        print("\nCalling conversion tool...")
        server_process.stdin.write(json.dumps(call_tool_message) + "\n")
        server_process.stdin.flush()
        
        # Read tool call response
        response_line = server_process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            print(f"Tool call response: {json.dumps(response, indent=2)}")
        
        print("\nMCP protocol test completed successfully!")
        
    except Exception as e:
        print(f"Error during MCP test: {e}")
        
    finally:
        # Clean up
        server_process.terminate()
        try:
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_process.kill()
            server_process.wait()

if __name__ == "__main__":
    asyncio.run(test_mcp_server())
