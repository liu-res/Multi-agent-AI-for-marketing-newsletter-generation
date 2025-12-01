"""
Agent Definitions
This module contains all agent definitions used in the newsletter automation workflow.
"""

import os

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("Loaded environment variables from .env file")
except ImportError:
    pass

# Try to get API key from environment
if "GOOGLE_API_KEY" in os.environ and os.environ["GOOGLE_API_KEY"]:
    print("Using GOOGLE_API_KEY from environment.")
else:
    print("Warning: GOOGLE_API_KEY not found.")
    print("   Please set it in the .env file or as an environment variable.")

# Import ADK components
from google.adk.models.google_llm import Gemini
from google.genai import types
from google.adk.agents import Agent, SequentialAgent
from google.adk.runners import InMemoryRunner
from google.adk.tools import AgentTool, FunctionTool, google_search

from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

from google.adk.apps.app import App, ResumabilityConfig
from pathlib import Path

# Import prompts
from prompts import (
    Data_Collection_Agent_Prompt,
    Trend_Finding_Agent_Prompt,
    Content_Writing_Agent_Prompt,
    Visual_Design_Agent_Prompt
)

# Import tools
from func_tools.html_reader_tools import read_html_tool, list_html_files_tool
from func_tools.mcp_pdf_reader import mcp_pdf_reader_server
from func_tools.newsletter_file_tools import (
    write_file_tool,
    check_content_file_tool,
    read_content_file_tool
)

# Import image gen tool if available
try:
    from func_tools.mcp_image_gen import mcp_image_gen_server
    MCP_IMAGE_GEN_AVAILABLE = mcp_image_gen_server is not None
except ImportError:
    mcp_image_gen_server = None
    MCP_IMAGE_GEN_AVAILABLE = False
    print("Warning: mcp_image_gen not available - image generation will be described in text.")

import warnings
warnings.filterwarnings("ignore")

print("ADK components imported successfully.")

retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

# Create Data_Collection_Agent
Data_Collection_Agent = Agent(
    name="DataCollectionAgent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    instruction=Data_Collection_Agent_Prompt,
    tools=[mcp_pdf_reader_server],
    output_key="internal_insights",
)
print("Data_Collection_Agent created.")

# Create Trend_Finding_Agent
Trend_Finding_Agent = Agent(
    name="TrendFindingAgent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    instruction=Trend_Finding_Agent_Prompt,
    tools=[google_search],
    output_key="external_trends",
)
print("Trend_Finding_Agent created.")

# Create Sequential Research Team
Sequential_Research_Team = SequentialAgent(
    name="SequentialResearchTeam",
    sub_agents=[Data_Collection_Agent, Trend_Finding_Agent],
)

# Create Content_Writing_Agent
Content_Writing_Agent = Agent(
    name="ContentWritingAgent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    instruction=Content_Writing_Agent_Prompt,
    tools=[write_file_tool],  # Add write_file tool so it can save newsletter_content.txt
    output_key="text_content",
)
print("Content_Writing_Agent created.")

# Create Visual_Design_Agent

visual_design_tools = [google_search, read_html_tool, list_html_files_tool]
# Add file reading and writing tools to visual design tools
visual_design_tools_with_file_read = visual_design_tools + [read_content_file_tool, write_file_tool]

Visual_Design_Agent = Agent(
    name="VisualDesignAgent",
    model=Gemini(
        model="gemini-2.5-flash-lite",  # Changed from gemini-2.0-flash-vision (not available)
        retry_options=retry_config
    ),
    instruction=Visual_Design_Agent_Prompt,
    tools=visual_design_tools_with_file_read,  # Includes file reading capability
    output_key="final_design",
)

# Create Marketing_Coordinator_Agent (simplified - only coordinates content and design)
Marketing_Coordinator_Agent = Agent(
    name="marketing_coordinator",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    instruction="""You are Marketing_Coordinator_Agent for Step 2: Content Generation.

    CRITICAL - Check file existence first:
    1. FIRST: Call the check_newsletter_content_exists tool to check if ./output/newsletter_content.txt exists
    
    Based on the file check result:
    
    IF ./output/newsletter_content.txt DOES NOT EXIST:
        Run all agents sequentially:
        1. Call Sequential_Research_Team to get both internal product insights (from Data_Collection_Agent) and external trends (from Trend_Finding_Agent)
        2. Call ContentWritingAgent that uses the output from Sequential_Research_Team to write the newsletter content
        3. Call VisualDesignAgent that uses the output from ContentWritingAgent to create the newsletter HTML
    
    IF ./output/newsletter_content.txt EXISTS:
        Skip the first 2 agents and only:
        1. Call VisualDesignAgent directly (it will use the existing ./output/newsletter_content.txt file as input)

    IMPORTANT: 
    - Do NOT describe what you will do - just check the file and call the appropriate agents immediately
    - Always check the file first before deciding which agents to call
    - The VisualDesignAgent can read from ./output/newsletter_content.txt if it exists
    - Use Sequential_Research_Team instead of calling Data_Collection_Agent and Trend_Finding_Agent separately

    """,
    tools=[
        check_content_file_tool,
        AgentTool(agent=Sequential_Research_Team),
        AgentTool(agent=Content_Writing_Agent),
        AgentTool(agent=Visual_Design_Agent),
    ],
)

# Define a runner
runner = InMemoryRunner(agent=Marketing_Coordinator_Agent)

async def main():
    """Main async function to run the agent."""
    print("\n" + "="*60)
    print("Starting Newsletter Generation Workflow")
    print("="*60 + "\n")
    
    try:
        response = await runner.run_debug(
            "Generate a newsletter HTML file. Show me the intermediate steps."
        )
        
        print("\n" + "="*60)
        print("Agent Execution Completed")
        print("="*60)
        
        # Log the response
        if response:
            print(f"\nResponse type: {type(response)}")
            if hasattr(response, 'content'):
                print(f"Response has content: {response.content is not None}")
                if hasattr(response.content, 'parts'):
                    print(f"Number of parts: {len(response.content.parts) if response.content.parts else 0}")
                    for i, part in enumerate(response.content.parts if response.content.parts else []):
                        print(f"\nPart {i+1}:")
                        if hasattr(part, 'text') and part.text:
                            print(f"  Text (first 500 chars): {part.text[:500]}...")
                        if hasattr(part, 'function_call'):
                            print(f"  Function call: {part.function_call}")
            
            # Try to get text content
            try:
                if hasattr(response, 'text'):
                    print(f"\nResponse text (first 1000 chars):\n{response.text[:1000]}...")
            except Exception as e:
                print(f"Could not extract text: {e}")
        
        # Check output directory
        output_dir = Path("./output")
        if output_dir.exists():
            files = list(output_dir.glob("*"))
            print(f"\nFiles in output directory: {len(files)}")
            for f in files:
                print(f"  - {f.name} ({f.stat().st_size} bytes)")
        else:
            print("\nOutput directory does not exist!")
        
        return response
        
    except Exception as e:
        print(f"\nError during agent execution: {e}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == "__main__":
    import asyncio
    import logging
    
    # Set up logging for more verbose output
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Enable verbose logging for ADK
    logger = logging.getLogger('google.adk')
    logger.setLevel(logging.DEBUG)
    
    asyncio.run(main())