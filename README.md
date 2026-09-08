# 🤖 Multi-Agent Research & Reporting System

An interactive web application built with **Streamlit**, **LangGraph**, **Groq (latest model)**, and **Tavily Search** that automates the process of gathering web data, summarizing insights, and generating comprehensive markdown reports through a multi-agent workflow.

---


----
# live demo
----



https://github.com/user-attachments/assets/f9b49cec-3d91-4656-b911-58e487197b6b


----

## ✨ Features

*   **Multi-Agent Workflow Architecture:** Powered by LangGraph to orchestrate distinct specialized agents:
    *   **Research Agent:** Queries the web using Tavily Search to fetch up-to-date data.
    *   **Summarizer Agent:** Distills raw web results into clean, organized bullet points.
    *   **Reporter Agent:** Transforms the summarized data into a professional markdown research report.
*   **Interactive Streamlit UI:** Features a sidebar for API key configuration, live execution logs, and clean rendering of the final output.
*   **High-Speed Inference:** Leverages Groq's ultra-fast Llama 3.3-70b model for rapid content synthesis.

---

## 🛠️ Prerequisites & Tech Stack

*   **Python** (v3.10 or higher recommended)
*   **Streamlit**
*   **LangGraph**
*   **LangChain-Groq** & **LangChain-Community**

---

## 📦 Installation & Setup

### 1. Clone or Download the Repository
Save your application code into a file named `app.py`.

### 2. Install Dependencies
Run the following command in your terminal to install the necessary Python packages:

```bash
pip install streamlit langgraph langchain-groq langchain-community python-dotenv tavily-python'''

3. Configure API Keys

You will need API keys from two services:

    Groq API Key: Get one from the Groq Console.

    Tavily API Key: Get one from Tavily AI.






```bash
pip install streamlit langgraph langchain-groq langchain-community python-dotenv tavily-python
