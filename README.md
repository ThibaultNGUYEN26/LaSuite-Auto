# Auto: AI Assistant for La Suite

> An intelligent AI assistant that orchestrates La Suite APIs, local files, and AI capabilities to automate complex workflows.

## 🎯 What is Auto?

**Auto** is an AI-powered orchestrator designed to help public-sector agents automate tasks that normally require multiple tools, documents, and manual steps.

Instead of manually navigating between applications, searching through documents, comparing information, and producing reports, users can describe a task in natural language. Auto analyzes the request, determines the actions required, selects the appropriate tools, and executes the workflow.

Auto combines **LLMs, API integrations, tool orchestration, file processing, and code execution** to turn complex multi-step tasks into a single interaction.

## 🚀 Key Features

### 🤖 AI-Powered Orchestration

Auto interprets natural-language requests and breaks them down into actionable steps. It can select and orchestrate different tools depending on the task and its context.

### 🔗 La Suite Integration

Auto interacts with La Suite services through their APIs, allowing it to retrieve information and perform actions across multiple services as part of the same workflow.

The project currently integrates with services such as:

- **Drive**
- **Grist**

### 📄 File & Document Processing

Auto can work with local files and documents, including PDF files.

It can:

- Read and extract information from documents
- Analyze and compare multiple files
- Cross-reference documents against a given reference or set of requirements
- Identify relevant evidence and information
- Use the results as input for further reasoning and analysis

### 🔍 Document Auditing & Compliance Analysis

Auto can automate document-based auditing workflows by comparing collected information and evidence against a predefined reference framework or set of requirements.

This enables workflows such as:

- Requirement-by-requirement analysis
- Evidence collection
- Document comparison
- Compliance assessment
- Generation of structured audit reports

### 🐍 Python Code Execution

When a task requires additional analysis or computation, Auto can execute Python code as part of the workflow.

This allows the assistant to perform programmatic operations on data and files in addition to LLM-based reasoning.

### 🧠 Stateful Conversations

Auto maintains the context of the ongoing interaction, allowing users to progressively refine a task and enabling multi-step workflows that depend on information gathered during previous actions.

### 🧩 Extensible Tool Architecture

Auto is built around a modular tool-based architecture. New tools and API integrations can be added without fundamentally changing the orchestration layer.

This allows the assistant to progressively support additional services and workflows.

## 🏗️ Architecture

At a high level, Auto is composed of:

- **LLM layer** — interprets user requests and performs reasoning
- **Orchestration layer** — plans and coordinates multi-step workflows
- **API integrations** — provide access to La Suite services
- **File processing** — handles local files and documents
- **Python execution** — enables programmatic analysis when required
- **Conversation state** — preserves context throughout a workflow

The architecture allows Auto to dynamically combine these components depending on the task.

## 📋 Current Capabilities

Auto currently supports workflows involving:

- Natural-language task understanding
- Multi-step AI orchestration
- Integration with La Suite services through APIs
- Local file and PDF processing
- Document comparison and analysis
- Requirement/reference-based auditing
- Evidence analysis
- Automated report generation
- Python code execution for additional analysis
- Stateful interactions

## 🔮 Future Extensions

The architecture is intended to support additional capabilities and integrations over time, including:

- Web browsing and information retrieval
- Email management and automation
- Secure file sharing through France Transfert
- Additional La Suite services and external tools
- More advanced autonomous workflows

## 📚 Documentation

For detailed setup, architecture, and technical documentation, see the [`docs/`](./docs/) directory.

## 🏗️ Project Structure

```text
app/
backend/
docs/