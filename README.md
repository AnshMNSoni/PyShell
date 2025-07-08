# 🧠 PyBot – Natural Language to Shell Command Converter

> A terminal-based assistant that converts natural language into safe and efficient Linux shell commands using OpenAI’s LLM.


## 🚀 Features 

- 🔁 **LLM Conversion**: Translates English queries into shell commands using OpenAI's Chat API.
- 🧠 **Few-shot Prompting**: Uses example inputs and outputs from `prompt_templates.json`.
- 🔐 **Secure API key management** with `.env` and `python-dotenv`.
- ✅ **Safe & extendable**: Designed to integrate with memory and safety checker modules.


## 📁 Project Structure

pybot/
├── llm_converter.py # Main logic to convert input → shell command
├── prompt_templates.json # Few-shot examples used in prompts
├── .env # Stores OpenAI API key (not committed to Git)
└── README.md # You are here
