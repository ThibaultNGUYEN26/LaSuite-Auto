# Auto: AI Assistant for La Suite

> An intelligent AI assistant that connects to La Suite tools to answer questions and automate workflows.

## 🎯 What is Auto?

**Auto** is an AI-powered orchestrator designed to work seamlessly with La Suite applications. It leverages Model Context Protocol (MCP) to access multiple La Suite tools and can:

- **Answer Questions:** Query Drive, Messages, Conversations, and other La Suite apps to provide informed responses
- **Automate Tasks:** Execute multi-step workflows by orchestrating APIs across different services
- **Understand Context:** Maintain conversation history and leverage files, emails, and structured data from La Suite

## 🚀 Key Features

- 🤖 **Multi-LLM Support:** Supports different LLM backends with capabilities for text, image, and file processing
- 🔗 **La Suite Integration:** Native connections to Drive, Messages, Conversations, Docs, Meet, and Grist via MCP
- 🧠 **Intelligent Orchestration:** Automatically breaks down complex tasks and executes them across multiple services
- 💾 **Stateful Conversations:** Maintains memory of previous interactions for context-aware responses
- 🛠️ **Extensible Tools:** Modular architecture for adding new capabilities and tool integrations

## 📋 Use Cases

- **Email Organization:** Auto receives files in emails and intelligently downloads and organizes them in Drive
- **Information Retrieval:** Ask Auto questions about your data across La Suite and get instant answers
- **Workflow Automation:** Define tasks and let Auto execute them across multiple La Suite services
- **Content Analysis:** Process files, images, and documents using multi-modal LLM capabilities

## 📚 Documentation

For detailed setup, architecture, and reference information, see:

- **[Setup & Technical Docs](./docs/driveAPI.md)** - Environment setup for the Drive API


## 🏗️ Project Structure

```
backend/
frontend/
docs/
```
