# 🤖 AI Assistant Chatbot

A modern, feature-rich AI chatbot application built with Streamlit that supports both cloud-based and local AI models. The application features a WhatsApp-style interface with comprehensive functionality including PDF generation, response formatting, and model management.

## 🌟 Features

- **Dual AI Mode Support**: Switch between cloud AI (via Groq API) and local AI (via Ollama)
- **Multiple Model Support**: Access to various state-of-the-art language models
- **WhatsApp-Style Interface**: Clean, modern chat interface with blue color scheme
- **PDF Export**: Generate professional PDFs from AI responses
- **Response Statistics**: Track word count, character count, and model usage
- **Thinking Process Display**: View AI reasoning process for supported models
- **Flexible Input Methods**: Choose between text input or text area for longer prompts
- **Real-time Server Status**: Monitor API server connectivity
- **Session Management**: Persistent chat history during session

## 🏗️ Project Structure

```
AI-Assistant-Chatbot/
├── client.py                 # Main application entry point
├── requirements.txt          # Python dependencies
├── README.md                # Project documentation
├── gui/                     # GUI components
│   ├── __init__.py
│   ├── app_controller.py    # Main application controller
│   ├── chat_interface.py    # Chat interface component
│   ├── sidebar.py           # Configuration sidebar
│   └── styles.py            # WhatsApp-style CSS styling
└── util/                    # Utility modules
    ├── __init__.py
    ├── api_client.py        # API communication handlers
    ├── config_manager.py    # Configuration management
    ├── pdf_generator.py     # PDF generation functionality
    └── response_formatter.py # Response processing
```

## 🛠️ Technologies Used

- **Frontend**: Streamlit (Web UI Framework)
- **Backend**: FastAPI (API Server - separate repository)
- **AI Models**: 
  - Cloud: Groq API (Qwen, Llama, Gemma, Mistral models)
  - Local: Ollama (Qwen, DeepSeek models)
- **PDF Generation**: ReportLab
- **Styling**: Custom CSS (WhatsApp-inspired design)
- **HTTP Client**: Requests
- **Markdown Processing**: Python-Markdown, BeautifulSoup4
- **Architecture**: SOLID Principles, Object-Oriented Programming

## 📋 Prerequisites

- Python 3.8 or higher
- Groq API account (for cloud models)
- Ollama installed (for local models)
- FastAPI server running (separate component)

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd AI-Assistant-Chatbot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Groq API (Cloud Models)

1. **Create Groq Account**:
   - Visit [Groq Console](https://console.groq.com/)
   - Sign up for a free account
   - Navigate to API Keys section

2. **Generate API Key**:
   - Click "Create API Key"
   - Give it a descriptive name
   - Copy the generated API key

3. **Configure API Key**:
   - Set the API key in your FastAPI server configuration
   - The server should handle authentication with Groq

### 4. Set Up Ollama (Local Models)

1. **Install Ollama**:
   ```bash
   # Windows (using PowerShell)
   winget install Ollama.Ollama
   
   # macOS
   brew install ollama
   
   # Linux
   curl -fsSL https://ollama.ai/install.sh | sh
   ```

2. **Start Ollama Service**:
   ```bash
   ollama serve
   ```

3. **Install Local Models**:
   ```bash
   # Install Qwen 3 (0.6B parameters)
   ollama pull qwen3:0.6b
   
   # Install DeepSeek R1 (1.5B parameters)
   ollama pull deepseek-r1:1.5b
   
   # Optional: Install other models
   ollama pull llama3.2:1b
   ollama pull phi3:mini
   ```

4. **Verify Installation**:
   ```bash
   ollama list
   ```

### 5. Start the Application

1. **Ensure FastAPI Server is Running**:
   - The application expects an API server on `http://localhost:8000`
   - Server should provide endpoints: `/health`, `/models`, `/chat/invoke`, `/local_chat/invoke`

2. **Run the Streamlit Application**:
   ```bash
   streamlit run client.py
   ```

3. **Access the Application**:
   - Open your browser to `http://localhost:8501`
   - The application will automatically check server status

## 📦 Requirements.txt

The application uses the following Python packages:

```txt

langchain_openai
langchain_core
python-dotenv
streamlit
langchain_community
langchain-ollama
langserve
fastapi
uvicorn
langchain-text-splitters
langchain-chroma
bs4
groq
langchain-groq
beautifulsoup4
sse_starlette
requests
reportlab
markdown

```

## 🎯 Usage

1. **Select AI Mode**: Choose between Cloud AI or Local AI in the sidebar
2. **Choose Model**: Select from available models based on your chosen mode
3. **Configure Input**: Choose between text input or text area for longer prompts
4. **Ask Questions**: Type your question and click "Ask Assistant"
5. **View Response**: See the AI's response with thinking process (if available)
6. **Export Results**: Download responses as PDF or copy to clipboard
7. **Monitor Usage**: Check response statistics in the expandable section

## 🔧 Configuration

### Available Cloud Models (Groq API)
- qwen/qwen3-32b
- qwen-qwq-32b
- llama3-70b-8192
- llama-3.1-8b-instant
- compound-beta
- gemma2-9b-it
- mistral-saba-24b

### Available Local Models (Ollama)
- qwen3:0.6b
- deepseek-r1:1.5b

### Customization
- Modify model lists in `util/config_manager.py`
- Adjust styling in `gui/styles.py`
- Configure API endpoints in `util/api_client.py`

## 🏛️ Architecture

The application follows SOLID principles and clean architecture:

- **Single Responsibility**: Each class has one clear purpose
- **Open/Closed**: Easy to extend with new models or features
- **Liskov Substitution**: Interfaces allow seamless component swapping
- **Interface Segregation**: Focused interfaces for specific functionality
- **Dependency Inversion**: High-level modules don't depend on low-level details

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Follow the existing code structure and SOLID principles
4. Ensure all components remain under 200 lines
5. Test your changes thoroughly
6. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Developer

**AdityaManojShinde**

---

*AI Assistant Chatbot - Bridging the gap between powerful AI models and user-friendly interfaces*
