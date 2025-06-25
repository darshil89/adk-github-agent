import os
import json
from google.adk.agents import Agent
from google.adk.tools.openapi_tool.openapi_spec_parser.openapi_toolset import OpenAPIToolset
from google.adk.tools.openapi_tool.auth.auth_helpers import token_to_scheme_credential
import logging
import sys
import asyncio
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure basic logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("github_agent")

def load_api_spec(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading API spec: {e}")
        return None

async def create_github_agent(api_spec_path=os.path.join(os.path.dirname(__file__), "api.github.com.fixed.json"), token_env_var="GITHUB_TOKEN", auth_prefix="token"):
    token = os.getenv(token_env_var)
    if not token:
        logger.error(f"GitHub token missing from environment variable: {token_env_var}")
        return None
        
    if not os.path.exists(api_spec_path):
        logger.error(f"GitHub API spec file not found: {api_spec_path}")
        return None
        
    spec = load_api_spec(api_spec_path)
    if not spec:
        return None
        
    try:
        auth_scheme, auth_credential = token_to_scheme_credential(
            "apikey", "header", "Authorization", f"{auth_prefix} {token}"
        )
        
        toolset = OpenAPIToolset(
            spec_str=json.dumps(spec),
            spec_str_type="json",
            auth_scheme=auth_scheme,
            auth_credential=auth_credential
        )
        
        all_tools = await toolset.get_tools()
        if not all_tools:
            logger.error("No tools found in GitHub API spec")
            return None
            
        logger.info(f"Found {len(all_tools)} total GitHub API tools")
        
        # Filter to most commonly used GitHub API endpoints to stay under 512 limit
        important_keywords = [
            # Repository operations
            'repos', 'repository', 'create_repo', 'get_repo', 'list_repos',
            # Issues and PRs
            'issues', 'issue', 'pull', 'pulls', 'create_issue', 'get_issue', 'list_issues',
            # Content operations
            'contents', 'content', 'create_file', 'update_file', 'get_content',
            # Branches and commits
            'branches', 'branch', 'commits', 'commit', 'refs', 'ref',
            # User operations
            'user', 'users', 'get_user', 'authenticated',
            # Organization operations  
            'orgs', 'org', 'organization',
            # Search operations
            'search',
            # Releases
            'releases', 'release',
            # Actions and workflows
            'actions', 'workflows', 'workflow',
            # Collaborators
            'collaborators', 'collaborator',
            # Labels and milestones
            'labels', 'label', 'milestones', 'milestone'
        ]
        
        # Filter tools based on important keywords
        filtered_tools = []
        for tool in all_tools:
            tool_name_lower = tool.name.lower()
            if any(keyword in tool_name_lower for keyword in important_keywords):
                filtered_tools.append(tool)
                
        # If we still have too many tools, take the first 500 to leave some buffer
        if len(filtered_tools) > 500:
            filtered_tools = filtered_tools[:500]
            logger.warning(f"Limiting tools to 500 out of {len(all_tools)} total tools")
        
        tools = filtered_tools
        logger.info(f"Using {len(tools)} filtered GitHub API tools")
        
        return Agent(
            name="github_agent",
            description="GitHub API Agent",
            instruction="""
            You are a GitHub API agent that interacts with GitHub's REST API.
            
            When working with the GitHub API:
            - Use parameters provided by the user
            - Ask for clarification if required parameters are missing
            - Format responses clearly for the user
            - Handle errors gracefully and explain issues in simple terms
            
            For content creation operations:
            - Use names and identifiers exactly as specified by the user
            - Add helpful descriptions when allowed by the API
            - Apply sensible defaults for optional parameters when not specified
            
            Always inform the user about the actions you're taking and the results received.
            """,
            model="gemini-2.0-flash",
            tools=tools
        )
    except Exception as e:
        logger.error(f"Error creating GitHub agent: {e}")
        return None

# Initialize root_agent at module level for adk web
def _create_root_agent():
    """Create root_agent synchronously for module import"""
    try:
        # Try to create the agent in a way that works with existing event loops
        import threading
        import concurrent.futures
        
        def run_in_thread():
            # Create a new event loop in a separate thread
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            try:
                return new_loop.run_until_complete(create_github_agent())
            finally:
                new_loop.close()
        
        # Check if we can run asyncio.run directly
        try:
            # Try to see if there's a running loop
            asyncio.get_running_loop()
            # If we get here, there's a running loop, so use thread
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(run_in_thread)
                return future.result(timeout=30)  # 30 second timeout
        except RuntimeError:
            # No running loop, we can use asyncio.run
            return asyncio.run(create_github_agent())
            
    except Exception as e:
        logger.error(f"Error creating root_agent: {e}")
        return None

# Create root_agent for adk web
root_agent = _create_root_agent()

async def main():
    global root_agent
    if root_agent is None:
        root_agent = await create_github_agent()
    
    if root_agent:
        logger.info(f"GitHub agent created successfully")

    else:
        logger.error("Failed to create GitHub agent")

if __name__ == "__main__":
    asyncio.run(main())

