# 🧠 Zack – AI Desktop Assistant for macOS

Zack is a smart, lightweight AI-powered desktop assistant built in Python. It can open macOS applications, search the web, manage tasks, and respond to natural language — all through a clean GUI powered by Tkinter and OpenAI's GPT.

## ✨ Features
- 🔍 Natural Language Understanding (via OpenAI GPT)
- 📁 Opens macOS applications with simple commands
- 🌐 Searches YouTube, Amazon, Google, LinkedIn directly from the assistant
- ✅ Task manager (add/show to-do items)
- 🌙 Light & Dark theme toggle
- 🖼️ Custom background support
- ⚡ Fast, responsive, and Pythonic
- 
 🚀 Getting Started

### ✅ Prerequisites
- macOS (tested on M1/M3)
- Python 3.10+ (3.13 recommended)
- `pip` (Python package manager)

### 📦 Installation

```bash
git clone https://github.com/yourusername/zack-assistant.git
cd zack-assistant

## Install dependences
pip install -r requirements.txt

💡 Example Commands
open chrome
search iPhone 15 on amazon
find AI jobs on linkedin
add task Complete project report
show tasks

🧠 Tech Stack
Python 3.13
Tkinter (GUI)
OpenAI GPT-3.5 Turbo
Pillow (for background image)
dotenv (API key handling)
macOS subprocess (app launcher)
