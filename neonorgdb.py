from typing import Any, Dict, List, Optional
import httpx
from fastmcp import FastMCP
import os
import json

# Initialize FastMCP server
mcp = FastMCP("neonorgdb",host="localhost", port=8000, debug=True)

# Constants
NEON_API_BASE = "https://console.neon.tech/api/v2"
USER_AGENT = "neonorgdb-mcp/1.0"

class NeonAPIClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": USER_AGENT
        }
    
    async def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make authenticated request to Neon API"""
        url = f"{NEON_API_BASE}/{endpoint.lstrip('/')}"
        
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=method,
                url=url,
                headers=self.headers,
                **kwargs
            )
            response.raise_for_status()
            return response.json()
    
    async def get_projects(self, cursor: Optional[str] = None, limit: int = 10) -> Dict[str, Any]:
        """Get all projects in the organization"""
        params = {"limit": limit}
        if cursor:
            params["cursor"] = cursor
        return await self._make_request("GET", "/projects", params=params)
    
    async def get_project(self, project_id: str) -> Dict[str, Any]:
        """Get specific project details"""
        return await self._make_request("GET", f"/projects/{project_id}")
    
    async def get_branches(self, project_id: str) -> Dict[str, Any]:
        """Get branches for a project"""
        return await self._make_request("GET", f"/projects/{project_id}/branches")
    
    async def get_databases(self, project_id: str, branch_id: str) -> Dict[str, Any]:
        """Get databases for a specific branch"""
        return await self._make_request("GET", f"/projects/{project_id}/branches/{branch_id}/databases")
    
    async def get_roles(self, project_id: str, branch_id: str) -> Dict[str, Any]:
        """Get roles for a specific branch"""
        return await self._make_request("GET", f"/projects/{project_id}/branches/{branch_id}/roles")
    
    async def get_operations(self, project_id: str, cursor: Optional[str] = None, limit: int = 10) -> Dict[str, Any]:
        """Get operations for a project"""
        params = {"limit": limit}
        if cursor:
            params["cursor"] = cursor
        return await self._make_request("GET", f"/projects/{project_id}/operations", params=params)
    
    async def get_endpoints(self, project_id: str) -> Dict[str, Any]:
        """Get compute endpoints for a project"""
        return await self._make_request("GET", f"/projects/{project_id}/endpoints")
    
    async def get_organization(self) -> Dict[str, Any]:
        """Get organization details"""
        return await self._make_request("GET", "/users/me")
    
    async def get_consumption_history(self, cursor: Optional[str] = None, limit: int = 10, 
                                    from_date: Optional[str] = None, to_date: Optional[str] = None) -> Dict[str, Any]:
        """Get consumption history for the organization"""
        params = {"limit": limit}
        if cursor:
            params["cursor"] = cursor
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        return await self._make_request("GET", "/consumption_history/account", params=params)

# Initialize API client
def get_neon_client() -> NeonAPIClient:
    api_key = os.getenv("NEON_API_KEY")
    if not api_key:
        raise ValueError("NEON_API_KEY environment variable is required")
    return NeonAPIClient(api_key)

@mcp.tool()
async def list_projects(cursor: Optional[str] = None, limit: int = 10) -> Dict[str, Any]:
    """
    List all projects in the Neon organization.
    
    Args:
        cursor: Pagination cursor for fetching next page
        limit: Maximum number of projects to return (default: 10)
    
    Returns:
        Dictionary containing projects list and pagination info
    """
    client = get_neon_client()
    return await client.get_projects(cursor=cursor, limit=limit)

@mcp.tool()
async def get_project_details(project_id: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific project.
    
    Args:
        project_id: The unique identifier of the project
    
    Returns:
        Dictionary containing project details
    """
    client = get_neon_client()
    return await client.get_project(project_id)

@mcp.tool()
async def list_project_branches(project_id: str) -> Dict[str, Any]:
    """
    List all branches for a specific project.
    
    Args:
        project_id: The unique identifier of the project
    
    Returns:
        Dictionary containing branches list
    """
    client = get_neon_client()
    return await client.get_branches(project_id)

@mcp.tool()
async def list_branch_databases(project_id: str, branch_id: str) -> Dict[str, Any]:
    """
    List all databases for a specific branch.
    
    Args:
        project_id: The unique identifier of the project
        branch_id: The unique identifier of the branch
    
    Returns:
        Dictionary containing databases list
    """
    client = get_neon_client()
    return await client.get_databases(project_id, branch_id)

@mcp.tool()
async def list_branch_roles(project_id: str, branch_id: str) -> Dict[str, Any]:
    """
    List all roles for a specific branch.
    
    Args:
        project_id: The unique identifier of the project
        branch_id: The unique identifier of the branch
    
    Returns:
        Dictionary containing roles list
    """
    client = get_neon_client()
    return await client.get_roles(project_id, branch_id)

@mcp.tool()
async def get_project_operations(project_id: str, cursor: Optional[str] = None, limit: int = 10) -> Dict[str, Any]:
    """
    Get recent operations for a specific project.
    
    Args:
        project_id: The unique identifier of the project
        cursor: Pagination cursor for fetching next page
        limit: Maximum number of operations to return (default: 10)
    
    Returns:
        Dictionary containing operations list and pagination info
    """
    client = get_neon_client()
    return await client.get_operations(project_id, cursor=cursor, limit=limit)

@mcp.tool()
async def list_project_endpoints(project_id: str) -> Dict[str, Any]:
    """
    List all compute endpoints for a specific project.
    
    Args:
        project_id: The unique identifier of the project
    
    Returns:
        Dictionary containing endpoints list
    """
    client = get_neon_client()
    return await client.get_endpoints(project_id)

@mcp.tool()
async def get_organization_info() -> Dict[str, Any]:
    """
    Get organization information and current user details.
    
    Returns:
        Dictionary containing organization and user information
    """
    client = get_neon_client()
    return await client.get_organization()

@mcp.tool()
async def get_consumption_metrics(cursor: Optional[str] = None, limit: int = 10, 
                                from_date: Optional[str] = None, to_date: Optional[str] = None) -> Dict[str, Any]:
    """
    Get consumption history and metrics for the organization.
    
    Args:
        cursor: Pagination cursor for fetching next page
        limit: Maximum number of consumption records to return (default: 10)
        from_date: Start date for consumption data (ISO 8601 format)
        to_date: End date for consumption data (ISO 8601 format)
    
    Returns:
        Dictionary containing consumption metrics and pagination info
    """
    client = get_neon_client()
    return await client.get_consumption_history(cursor=cursor, limit=limit, 
                                              from_date=from_date, to_date=to_date)

@mcp.tool()
async def search_projects_by_name(name_pattern: str) -> List[Dict[str, Any]]:
    """
    Search for projects by name pattern.
    
    Args:
        name_pattern: Pattern to search for in project names (case-insensitive)
    
    Returns:
        List of projects matching the name pattern
    """
    client = get_neon_client()
    all_projects = []
    cursor = None
    
    # Fetch all projects (with pagination)
    while True:
        result = await client.get_projects(cursor=cursor, limit=100)
        projects = result.get("projects", [])
        all_projects.extend(projects)
        
        cursor = result.get("pagination", {}).get("cursor")
        if not cursor:
            break
    
    # Filter projects by name pattern
    matching_projects = [
        project for project in all_projects 
        if name_pattern.lower() in project.get("name", "").lower()
    ]
    
    return matching_projects

if __name__ == "__main__":
    mcp.run()