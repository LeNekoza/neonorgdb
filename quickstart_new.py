#!/usr/bin/env python3
"""
Quick start script for the Neon DB MCP Server.
This script helps users get started quickly.
"""

import os
import sys
import subprocess

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 13):
        print(f"X Python 3.13+ required, found {sys.version_info.major}.{sys.version_info.minor}")
        return False
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import httpx
        import mcp.server.fastmcp
        print("✓ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"X Missing dependency: {e}")
        print("Run: pip install httpx mcp")
        return False

def check_api_key():
    """Check if API key is configured"""
    api_key = os.getenv('NEON_API_KEY')
    if not api_key:
        print("X NEON_API_KEY environment variable not set")
        print("Get your API key from: https://console.neon.tech/")
        print("Set it with: $env:NEON_API_KEY = 'your-api-key'")
        return False
    print("✓ NEON_API_KEY is configured")
    return True

def run_verification():
    """Run the verification script"""
    try:
        result = subprocess.run([sys.executable, "verify.py"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Server verification passed")
            return True
        else:
            print(f"X Verification failed")
            return False
    except Exception as e:
        print(f"X Could not run verification: {e}")
        return False

def main():
    """Main quick start function"""
    print("Neon DB MCP Server - Quick Start\n")
    
    checks = [
        ("Python version", check_python_version),
        ("Dependencies", check_dependencies),
        ("API key", check_api_key),
        ("Server verification", run_verification),
    ]
    
    all_passed = True
    for check_name, check_func in checks:
        print(f"Checking {check_name}...")
        if not check_func():
            all_passed = False
        print()
    
    if all_passed:
        print("All checks passed! You're ready to start the MCP server.")
        print("\nTo start the server:")
        print("  python neonorgdb.py")
        print("\nTo test the server:")
        print("  python example_usage.py")
    else:
        print("X Some checks failed. Please fix the issues above before starting.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
