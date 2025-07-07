import requests
import streamlit as st
from typing import Optional
import re

# Page configuration
st.set_page_config(
    page_title="AI Assistant Chatbot",
    layout="centered"
)




# Custom CSS for minimalistic design
st.markdown("""
<style>
.main-header {
    text-align: center;
    font-size: 2.5rem;
    font-weight: 600;
    margin-bottom: 2rem;
    color: #1f2937;
}

.stButton > button {
    border-radius: 8px;
    border: none;
    
    padding: 0.75rem 2rem;
    font-weight: 500;
    font-size: 1rem;
    width: 100%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.mode-indicator {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.875rem;
    font-weight: 500;
    margin-bottom: 1rem;
}

.cloud-mode {
    background-color: #dbeafe;
    color: #1e40af;
}

.local-mode {
    background-color: #fef3c7;
    color: #b45309;
}

.stSpinner > div {
    border-top-color: #667eea !important;
}

.footer {
    text-align: center;
    color: #6b7280;
    font-size: 0.875rem;
    margin-top: 3rem;
    padding-top: 1rem;
    border-top: 1px solid #e5e7eb;
}

.response-container {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
}

.thinking-container {
    background: #f3f4f6;
    border: 1px solid #d1d5db;
    border-radius: 8px;
    padding: 1rem;
    margin: 1rem 0;
    border-left: 4px solid #6b7280;
}

.thinking-text {
    color: #6b7280;
    font-style: italic;
    font-size: 0.95rem;
}

.main-response {
    color: #1f2937;
    line-height: 1.6;
}

.server-status {
    padding: 0.5rem 1rem;
    border-radius: 8px;
    margin-bottom: 1rem;
    font-size: 0.875rem;
    text-align: center;
}

.server-online {
    background-color: #d1fae5;
    color: #065f46;
    border: 1px solid #a7f3d0;
}

.server-offline {
    background-color: #fee2e2;
    color: #991b1b;
    border: 1px solid #fecaca;
}

.model-refresh {
    font-size: 0.875rem;
    color: #6b7280;
    margin-top: 0.5rem;
}

/* Improve markdown rendering */
.main-response h1, .main-response h2, .main-response h3 {
    color: #1f2937;
    margin-top: 1.5rem;
    margin-bottom: 0.5rem;
}

.main-response h1 {
    font-size: 1.5rem;
    font-weight: 600;
    border-bottom: 2px solid #e5e7eb;
    padding-bottom: 0.5rem;
}

.main-response h2 {
    font-size: 1.25rem;
    font-weight: 600;
}

.main-response h3 {
    font-size: 1.125rem;
    font-weight: 600;
}

.main-response ul, .main-response ol {
    margin-left: 1.5rem;
    margin-bottom: 1rem;
}

.main-response li {
    margin-bottom: 0.25rem;
}

.main-response p {
    margin-bottom: 1rem;
}

.main-response blockquote {
    border-left: 4px solid #e5e7eb;
    margin-left: 0;
    padding-left: 1rem;
    color: #6b7280;
    font-style: italic;
}

.main-response code {
    background-color: #f3f4f6;
    color: #dc2626;
    padding: 0.125rem 0.25rem;
    border-radius: 0.25rem;
    font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
    font-size: 0.875rem;
}

.main-response pre {
    background-color: #1f2937;
    color: #f9fafb;
    padding: 1rem;
    border-radius: 0.5rem;
    overflow-x: auto;
    margin: 1rem 0;
}

.main-response pre code {
    background-color: transparent;
    color: #f9fafb;
    padding: 0;
}

.main-response table {
    width: 100%;
    border-collapse: collapse;
    margin: 1rem 0;
}

.main-response th, .main-response td {
    border: 1px solid #e5e7eb;
    padding: 0.5rem;
    text-align: left;
}

.main-response th {
    background-color: #f9fafb;
    font-weight: 600;
}

.main-response strong {
    font-weight: 600;
    color: #1f2937;
}

.main-response em {
    font-style: italic;
    color: #4b5563;
}
</style>
""", unsafe_allow_html=True)

def format_response_with_thinking(response: str) -> dict:
    """Format the response to separate thinking sections from main content"""
    # Find all <think></think> blocks
    think_pattern = r'<think>(.*?)</think>'
    
    # Extract thinking content
    thinking_blocks = re.findall(think_pattern, response, flags=re.DOTALL)
    
    # Remove thinking blocks from main response
    main_response = re.sub(think_pattern, '', response, flags=re.DOTALL)
    
    # Clean up any remaining <think> or </think> tags
    main_response = re.sub(r'</?think>', '', main_response)
    
    # Clean up extra whitespace
    main_response = main_response.strip()
    
    return {
        "thinking": thinking_blocks,
        "main_response": main_response
    }

def check_server_status() -> bool:
    """Check if the API server is running"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def get_available_models() -> dict:
    """Get available models from the server"""
    try:
        response = requests.get("http://localhost:8000/models", timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "cloud_models": [
                   "qwen/qwen3-32b",
                    "qwen-qwq-32b",
                    "llama3-70b-8192",
                    "llama-3.1-8b-instant",
                    "compound-beta",
                    "gemma2-9b-it",
                    "mistral-saba-24b",
                   
                ],
                "local_models": [
                    "qwen3:0.6b",
                    "deepseek-r1:1.5b",
                ]
            }
    except:
        # Fallback to hardcoded models if server is not available
        return {
            "cloud_models": [
                    "qwen/qwen3-32b",
                    "qwen-qwq-32b",
                    "llama3-70b-8192",
                    "llama-3.1-8b-instant",
                    "compound-beta",
                    "gemma2-9b-it",
                    "mistral-saba-24b",
                
            ],
            "local_models": [
                "qwen3:0.6b",
                "deepseek-r1:1.5b"
            ]
        }

def get_chat_response(input_text: str, model_name: str) -> Optional[str]:
    """Get response from the chat API with error handling"""
    try:
        with st.spinner("Thinking..."):
            response = requests.post(
                "http://localhost:8000/chat/invoke",
                json={
                    "input": {
                        'question': input_text,
                        'model': model_name
                    }       
                },
                timeout=60  # Increased timeout for cloud models
            )
            response.raise_for_status()
            
            response_data = response.json()
            
            # Handle the updated server response format
            if isinstance(response_data, dict) and "output" in response_data:
                output = response_data["output"]
                
                # The server now returns a simple string output
                if isinstance(output, str):
                    return output
                else:
                    return str(output)
            else:
                return str(response_data)
                
    except requests.exceptions.ConnectionError:
        st.error("❌ Connection failed. Please ensure the API server is running on localhost:8000")
        return None
    except requests.exceptions.Timeout:
        st.error("⏱️ Request timed out. The server might be busy or the model is taking longer to respond.")
        return None
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 500:
            st.error(f"🚨 Server error: {e.response.json().get('detail', 'Unknown error')}")
        else:
            st.error(f"❌ HTTP error: {e}")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Request failed: {str(e)}")
        return None
    except Exception as e:
        st.error(f"❌ An unexpected error occurred: {str(e)}")
        print(f"Full error details: {e}")
        return None

def get_localchat_response(input_text: str, model_name: str) -> Optional[str]:
    """Get response from the local chat API with error handling"""
    try:
        with st.spinner("Processing locally..."):
            response = requests.post(
                "http://localhost:8000/local_chat/invoke",
                json={
                    "input": {
                        'question': input_text,
                        'model': model_name
                    }       
                },
                timeout=120  # Increased timeout for local models
            )
            response.raise_for_status()
            
            response_data = response.json()
            
            # Handle the updated server response format
            if isinstance(response_data, dict) and "output" in response_data:
                output = response_data["output"]
                
                # The server now returns a simple string output
                if isinstance(output, str):
                    return output
                else:
                    return str(output)
            else:
                return str(response_data)
                
    except requests.exceptions.ConnectionError:
        st.error("❌ Connection failed. Please ensure the API server is running on localhost:8000")
        return None
    except requests.exceptions.Timeout:
        st.error("⏱️ Request timed out. Local model might be downloading or taking longer to respond.")
        return None
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 500:
            error_detail = e.response.json().get('detail', 'Unknown error')
            if "model" in error_detail.lower():
                st.error(f"🚨 Model error: {error_detail}")
                st.info("💡 Make sure the selected model is installed in Ollama. Run `ollama pull {model_name}` to download it.")
            else:
                st.error(f"🚨 Server error: {error_detail}")
        else:
            st.error(f"❌ HTTP error: {e}")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Request failed: {str(e)}")
        return None
    except Exception as e:
        st.error(f"❌ An unexpected error occurred: {str(e)}")
        print(f"Full error details: {e}")
        return None

def main():
    # Header
    st.markdown('<h1 class="main-header">🤖 AI Assistant Chatbot</h1>', unsafe_allow_html=True)
    
    # Check server status
    server_online = check_server_status()
    
    # Get available models
    available_models = get_available_models()
    
    # Sidebar with configuration
    with st.sidebar:
        st.markdown("### 🔧 Configuration")
        
        # Server status in sidebar
        st.markdown("**Server Status:**")
        if server_online:
            st.markdown('<div class="server-status server-online">✅ Server is online and ready</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="server-status server-offline">❌ Server is offline</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Mode selector in sidebar
        mode = st.selectbox(
            "🌐 Select AI Mode:",
            ["Cloud AI", "Local AI"],
            index=0
        )
        
        # Model selector based on mode in sidebar
        if mode == "Cloud AI":
            cloud_models = available_models["cloud_models"]
            selected_model = st.selectbox(
                "🤖 Select Cloud Model:",
                cloud_models,
                index=0
            )
        else:
            local_models = available_models["local_models"]
            selected_model = st.selectbox(
                "🤖 Select Local Model:",
                local_models,
                index=0
            )
        
        # Refresh models button in sidebar
        if st.button("🔄 Refresh Models", help="Refresh the list of available models from server"):
            st.rerun()
        
        st.markdown("---")
        
        # Input method selector in sidebar
        input_method = st.selectbox(
            "📝 Input Method:",
            ["Text Input", "Text Area"],
            index=0
        )
        
        st.markdown("---")
        
        # Quick start information
        st.markdown("**Quick Start:**")
        st.markdown("""
        1. Check server status above
        2. Select your AI mode (Cloud/Local)
        3. Choose a model
        4. Select input method
        5. Start chatting!
        """)
        
        
    # Main container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Display current mode and model
    if mode == "Cloud AI":
        st.markdown(f'<div class="mode-indicator cloud-mode">🌐 Cloud AI Mode - {selected_model}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="mode-indicator local-mode">💻 Local AI Mode - {selected_model}</div>', unsafe_allow_html=True)
    
    
    # Input based on selected method
    if input_method == "Text Input":
        input_text = st.text_input(
            "Ask me anything:",
            placeholder="e.g., How does machine learning work?",
            key="chat_input"
        )
    else:
        input_text = st.text_area(
            "Ask me anything:",
            placeholder="e.g., Write a detailed explanation about quantum computing...",
            key="chat_textarea",
            height=100
        )
    
    # Generate button
    col1, col2 = st.columns([3, 1])
    
    with col1:
        generate_button = st.button("Ask Assistant", type="primary", disabled=not server_online)
    
    with col2:
        if st.button("🗑️ Clear"):
            st.rerun()
         
    
    # Process the request
    if generate_button:
        if input_text.strip():
            if mode == "Cloud AI":
                response = get_chat_response(input_text, selected_model)
            else:
                response = get_localchat_response(input_text, selected_model)
            
            if response:
                # Format the response to separate thinking and main content
                formatted_response = format_response_with_thinking(response)
                
                # Display thinking sections if they exist
                if formatted_response["thinking"]:
                    for i, thinking in enumerate(formatted_response["thinking"]):
                        st.markdown(f'<div class="thinking-container">', unsafe_allow_html=True)
                        st.markdown(f'<div class="thinking-text">💭 <strong>Thinking {i+1}:</strong><br>{thinking.strip()}</div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                
                # Display main response
                st.markdown('<div class="response-container">', unsafe_allow_html=True)
                st.markdown(f"**🤖 Assistant ({selected_model}):**")
                
                # Use st.markdown to properly render markdown content
                st.markdown(formatted_response["main_response"])
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Action buttons
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    # Download button
                    st.download_button(
                        label="📥 Download Response",
                        data=response,
                        file_name=f"response_{selected_model}_{input_text[:15].replace(' ', '_')}.txt",
                        mime="text/plain"
                    )
                
                with col2:
                    # Copy to clipboard (using session state)
                    if st.button("📋 Copy Response"):
                        st.session_state.copied_text = response
                        st.success("Response copied to session!")
                
                
                
                # Show response statistics
                with st.expander("📊 Response Statistics"):
                    word_count = len(response.split())
                    char_count = len(response)
                    st.metric("Word Count", word_count)
                    st.metric("Character Count", char_count)
                    st.metric("Model Used", selected_model)
        else:
            st.warning("⚠️ Please enter a question or prompt.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown(
        '<div class="footer">AI Assistant Chatbot • Created by AdityaManojShinde</div>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()