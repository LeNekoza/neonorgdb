# Neon DB Organization MCP Server

A **Model Context Protocol (MCP)** server for querying **Neon DB organization-level API** endpoints.  
This server provides tools to manage and query your Neon projects, branches, databases, roles, and operations programmatically.

---

## Features

- **Project Management**: List all projects, get project details, search projects by name  
- **Branch Operations**: List branches for projects  
- **Database Management**: List databases for specific branches  
- **Role Management**: List roles for specific branches  
- **Operations Monitoring**: Get recent operations for projects  
- **Endpoint Management**: List compute endpoints for projects  
- **Organization Info**: Get organization and user details  
- **Consumption Metrics**: Query usage and billing data

---

## Setup

### 1. Install Dependencies

```bash
pip install httpx mcp
```

### 2. Get Neon API Key

1. Log in to the [Neon Console](https://console.neon.tech/)
2. Go to **Account Settings → API Keys**
3. Create a new API key
4. Copy the API key

### 3. Set Environment Variable

Set your Neon API key as an environment variable:

```bash
# Windows PowerShell
$env:NEON_API_KEY = "your-api-key-here"

# Windows Command Prompt
set NEON_API_KEY=your-api-key-here

# Linux/macOS
export NEON_API_KEY=your-api-key-here
```

### 4. Run the MCP Server

```bash
python neonorgdb.py
```

---

## Available Tools

### 🗂️ Project Management

- `list_projects(cursor?, limit?)` – List all projects in the organization  
- `get_project_details(project_id)` – Get detailed information about a specific project  
- `search_projects_by_name(name_pattern)` – Search projects by name pattern

### 🌿 Branch Management

- `list_project_branches(project_id)` – List all branches for a project

### 🗄️ Database Management

- `list_branch_databases(project_id, branch_id)` – List databases for a specific branch

### 👤 Role Management

- `list_branch_roles(project_id, branch_id)` – List roles for a specific branch

### 🧾 Operations

- `get_project_operations(project_id, cursor?, limit?)` – Get recent operations for a project

### 🌐 Endpoints

- `list_project_endpoints(project_id)` – List compute endpoints for a project

### 🏢 Organization

- `get_organization_info()` – Get organization and user information  
- `get_consumption_metrics(cursor?, limit?, from_date?, to_date?)` – Get consumption history

---

## API Reference

This MCP server uses the [Neon API v2](https://api-docs.neon.tech/reference/getting-started-with-neon-api).

### 🔐 Authentication

Uses **Bearer token** authentication with your Neon API key.  
Ensure the `NEON_API_KEY` environment variable is set before running the server.

### 🚦 Rate Limiting

The Neon API has rate limits.  
This server includes basic error handling for HTTP errors. For production use, implement:

- Retry logic
- Backoff strategies

### 🔄 Pagination

Many endpoints use **cursor-based pagination**.  
Use the `cursor` parameter to retrieve additional pages of results.

---

## Example Usage

Once the MCP server is running, MCP-compatible clients can:

1. **List all projects** – Get an overview of all projects in your organization  
2. **Monitor operations** – Check the status of recent operations  
3. **Analyze consumption** – Query usage metrics and billing data  
4. **Manage resources** – List branches, databases, and roles across projects

---

## Error Handling

Basic error handling covers:

- Missing API key
- HTTP errors from the Neon API
- Invalid project/branch IDs

### ✅ For Production

Consider adding:

- Retry logic for transient errors  
- Detailed error logging  
- Rate limit handling

---

## Contributing

Feel free to submit issues and enhancement requests!

---

## License

MIT License
