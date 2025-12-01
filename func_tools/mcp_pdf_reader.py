# mcp_pdf_reader.py
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters
import os

# MCP PDF Reader Server
# Using pdf-reader-mcp from PyPI - extracts text from PDFs
# Supports: text extraction, OCR, directory processing

# Exclude GOOGLE_API_KEY from env to avoid any validation errors
env_vars = {k: v for k, v in os.environ.items() if k != "GOOGLE_API_KEY"}

mcp_pdf_reader_server = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="uvx",  # Run MCP server via uvx
            args=[
                "--from=pdf-reader-mcp",
                "pdf-reader-mcp",  # Executable name
                "--transport=stdio",  # Use stdio transport (required for ADK)
            ],
            # Don't filter - let all tools be available
            # The agent will discover available tools automatically
            env=env_vars,
        ),
        timeout=120,  # PDF processing may take time
    )
)

print("MCP PDF Reader Tool created")

