# GitHub Agent with Google ADK and OpenAPI Tools using Gemini 2.5 Pro

A GitHub gent built using Google's Agent Development Kit (ADK) and OpenAPI Specification tools that provides a natural language interface to GitHub's REST API using Google Gemini 2.5 Pro

## Introduction

This project demonstrates how to build an GitHub agent using Google's [Agent Development Kit (ADK)](https://google.github.io/adk-docs/) and OpenAPI integration. The agent leverages the GitHub REST API through an OpenAPI specification to perform various GitHub operations via natural language commands.

## Demo

![Screenshot](https://github.com/darshil89/adk-github-agent/blob/main/Images/ss.png)

[Watch the demo](https://drive.google.com/file/d/1v6abeJ3sbVlH5b2Au69lkC5Q73CKkefM/view?usp=sharing)


### Core Components:

* **[Google ADK](https://google.github.io/adk-docs/)** — Provides the agent framework and infrastructure (Agent class)
* **[OpenAPI Tools](https://google.github.io/adk-docs/tools/openapi-tools/)** — Transforms API specifications into executable tools
* **OpenAPI Specification** — GitHub's v3 API defined in JSON format
* **Authentication Handler** — Manages GitHub personal access tokens
* **Gemini 2.5 Pro** — Powers the language understanding & generation
* **OpenAPIToolset** — Dynamically generates API tools from the spec

### 🔄 Workflow: How a User Query is Processed

1. **User Input**  
   The user types a natural language request — for example:  
   _"Show my repositories"_

2. **Routing & Context Preparation**  
   - The query is routed to the **GitHub agent**.  
   - **ADK (Agent Development Kit)** prepares the execution context by including:  
     - The relevant **API specification**  
     - The user's **authentication token**

3. **LLM Interpretation (Gemini 2.5 Pro)**  
   - The **LLM (Large Language Model)** analyzes the user’s intent.  
   - It maps the input to potential **GitHub API operations** that can fulfill the request.

4. **Tool Discovery & Parameter Handling**  
   - The **OpenAPIToolset** identifies the most suitable API endpoints.  
   - If required parameters are missing (e.g., username, repo name), it:  
     - Extracts them from the query, or  
     - Asks the user for more information.
     - 
5. **API Execution**  
   - The chosen GitHub API endpoint is called with the correct parameters and **authorization headers**.  
   - The request is sent to GitHub’s servers and executed.

6. **Response Formatting & Output**  
   - The raw API response is formatted for readability.  
   - The final result is presented back to the user in a clear, structured format.


## Implementation

This section provides a step-by-step guide to setting up and using the GitHub agent.

### Prerequisites

1. **Python 3.10+** installed
2. **Google Gemini Generative AI** access via API key
3. **GitHub account** and personal access token
4. **GitHub OpenAPI Spec**: [GitHub REST API Description](https://raw.githubusercontent.com/github/rest-api-description/main/descriptions/api.github.com/api.github.com.json)

### Project Structure

- `github-agent/agent.py`: Main agent implementation
- `github-agent/api.github.com.fixed.json`: GitHub API OpenAPI specification

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/darshil89/adk-github-agent
   cd adk-github-agent
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv .venv
   .venv/Scripts/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install google-adk
   ```

4. Obtain a GitHub API token

5. Run the agent:
   ```bash
   adk web
   ```

## Resources

- [Google Agent Development Kit Documentation](https://google.github.io/adk-docs/)
- [OpenAPI Tools in ADK](https://google.github.io/adk-docs/tools/openapi-tools/)


## GitHub Repository

You can access all the code used in this project at:
[github.com/darshil89/adk-github-agent](https://github.com/darshil89/adk-github-agent)