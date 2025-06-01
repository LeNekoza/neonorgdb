#!/usr/bin/env python3
"""
Test script to verify the Neon DB MCP server structure.
"""

import os
import sys
import asyncio
from unittest.mock import patch, AsyncMock

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_neon_client():
    """Test the NeonAPIClient without making real API calls"""
    from neonorgdb import NeonAPIClient
    
    # Mock API key for testing
    client = NeonAPIClient("test-api-key")
    
    print("✓ NeonAPIClient initialized successfully")
    print(f"✓ API base URL: {client.headers}")
    return True

async def test_tools_registration():
    """Test that all MCP tools are properly registered"""
    from neonorgdb import mcp
    
    # Get all registered tools
    tools = mcp._tools
    tool_names = list(tools.keys())
    
    expected_tools = [
        'list_projects',
        'get_project_details', 
        'list_project_branches',
        'list_branch_databases',
        'list_branch_roles',
        'get_project_operations',
        'list_project_endpoints',
        'get_organization_info',
        'get_consumption_metrics',
        'search_projects_by_name'
    ]
    
    print(f"✓ Found {len(tool_names)} registered tools:")
    for tool_name in tool_names:
        print(f"  - {tool_name}")
    
    missing_tools = set(expected_tools) - set(tool_names)
    if missing_tools:
        print(f"✗ Missing tools: {missing_tools}")
        return False
    
    extra_tools = set(tool_names) - set(expected_tools)
    if extra_tools:
        print(f"ℹ Extra tools found: {extra_tools}")
    
    print("✓ All expected tools are registered")
    return True

async def test_environment_validation():
    """Test environment variable handling"""
    from neonorgdb import get_neon_client
    
    # Test with missing API key
    original_key = os.environ.get('NEON_API_KEY')
    if 'NEON_API_KEY' in os.environ:
        del os.environ['NEON_API_KEY']
    
    try:
        client = get_neon_client()
        print("✗ Should have raised ValueError for missing API key")
        return False
    except ValueError as e:
        print(f"✓ Correctly handles missing API key: {e}")
    
    # Restore original key if it existed
    if original_key:
        os.environ['NEON_API_KEY'] = original_key
    
    return True

async def main():
    """Run all tests"""
    print("🧪 Testing Neon DB MCP Server Implementation\n")
    
    tests = [
        ("NeonAPIClient initialization", test_neon_client),
        ("MCP tools registration", test_tools_registration),
        ("Environment validation", test_environment_validation),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"Running: {test_name}")
        try:
            result = await test_func()
            results.append(result)
            print(f"✓ {test_name} passed\n")
        except Exception as e:
            print(f"✗ {test_name} failed: {e}\n")
            results.append(False)
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The MCP server is ready to use.")
        print("\nNext steps:")
        print("1. Set your NEON_API_KEY environment variable")
        print("2. Run: python neonorgdb.py")
        print("3. Connect your MCP client to use the Neon DB tools")
    else:
        print("❌ Some tests failed. Please check the implementation.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
