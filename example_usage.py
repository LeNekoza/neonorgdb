#!/usr/bin/env python3
"""
Example usage of the Neon DB MCP Server tools.
This demonstrates how to use the MCP tools programmatically.
"""

import asyncio
import os
from neonorgdb import get_neon_client

async def example_usage():
    """Example of using the Neon API client directly"""
    
    # Check if API key is set
    if not os.getenv('NEON_API_KEY'):
        print("❌ Please set NEON_API_KEY environment variable")
        print("   PowerShell: $env:NEON_API_KEY = 'your-api-key'")
        return
    
    try:
        print("🔌 Connecting to Neon API...")
        client = get_neon_client()
        
        print("📋 Fetching organization info...")
        org_info = await client.get_organization()
        print(f"✓ Organization: {org_info.get('email', 'N/A')}")
        
        print("📁 Fetching projects...")
        projects_result = await client.get_projects(limit=5)
        projects = projects_result.get('projects', [])
        
        if not projects:
            print("ℹ No projects found in your organization")
            return
            
        print(f"✓ Found {len(projects)} projects:")
        
        for project in projects:
            project_id = project['id']
            project_name = project['name']
            print(f"\n📂 Project: {project_name} ({project_id})")
            
            # Get branches for this project
            branches_result = await client.get_branches(project_id)
            branches = branches_result.get('branches', [])
            print(f"  📍 Branches: {len(branches)}")
            
            for branch in branches[:2]:  # Show first 2 branches
                branch_id = branch['id']
                branch_name = branch['name']
                print(f"    🌿 {branch_name} ({branch_id})")
                
                # Get databases for this branch
                try:
                    databases_result = await client.get_databases(project_id, branch_id)
                    databases = databases_result.get('databases', [])
                    print(f"      💾 Databases: {[db['name'] for db in databases]}")
                except Exception as e:
                    print(f"      ⚠ Could not fetch databases: {e}")
        
        print("\n🎉 Example completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main function"""
    print("🧪 Neon DB MCP Server - Usage Example\n")
    asyncio.run(example_usage())

if __name__ == "__main__":
    main()
