# Import Langchain libraries
from langchain_groq import ChatGroq
from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langserve import add_routes

# Import FastAPI libraries
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# Import system libraries
import os
from dotenv import load_dotenv
import uvicorn


class ChatInput(BaseModel):
    question: str
    model: str


class ChatResponse(BaseModel):
    output: str


class LangchainAPIApp:
    def __init__(self):
        self._load_env_variables()
        self.app = self._create_fastapi_app()
        self.groq_api_key = os.environ.get('GROQ_API_KEY')
        self.output_parser = StrOutputParser()

        # Initialize components
        self.story_prompt = self._create_prompt_template()
        self.local_story_prompt = self._create_prompt_template()

        # Setup routes
        self._add_routes()

    def _load_env_variables(self):
        load_dotenv()

    def _create_fastapi_app(self):
        return FastAPI(
            title="Langchain API",
            description="A simple API to generate text using Langchain",
            version="0.0.1",
        )

    def _create_prompt_template(self):
        return ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant. Please respond to the user queries."),
            ("user", "Question: {question}"),
        ])

    def _create_groq_llm(self, model_name: str):
        """Create Groq LLM with specified model"""
        if not self.groq_api_key:
            raise HTTPException(status_code=500, detail="GROQ_API_KEY not found in environment variables")
        
        return ChatGroq(
            api_key=self.groq_api_key,
            model=model_name
        )

    def _create_local_llm(self, model_name: str):
        """Create local Ollama LLM with specified model"""
        return OllamaLLM(model=model_name)

    async def chat_endpoint(self, chat_input: ChatInput):
        """Handle cloud AI chat requests"""
        try:
            # Create LLM with the specified model
            groq_llm = self._create_groq_llm(chat_input.model)
            
            # Create chain
            chain = self.story_prompt | groq_llm | self.output_parser
            
            # Generate response
            response = await chain.ainvoke({"question": chat_input.question})
            
            return {"output": response}
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")

    async def local_chat_endpoint(self, chat_input: ChatInput):
        """Handle local AI chat requests"""
        try:
            # Create local LLM with the specified model
            local_llm = self._create_local_llm(chat_input.model)
            
            # Create chain
            chain = self.local_story_prompt | local_llm | self.output_parser
            
            # Generate response
            response = await chain.ainvoke({"question": chat_input.question})
            
            return {"output": response}
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")

    def _add_routes(self):
        """Add custom routes for dynamic model selection"""
        
        @self.app.post("/chat/invoke")
        async def chat_invoke(request: dict):
            """Cloud AI chat endpoint"""
            try:
                input_data = request.get("input", {})
                question = input_data.get("question", "")
                model = input_data.get("model", "llama3-70b-8192")  # Default model
                
                chat_input = ChatInput(question=question, model=model)
                result = await self.chat_endpoint(chat_input)
                
                return result
                
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/local_chat/invoke")
        async def local_chat_invoke(request: dict):
            """Local AI chat endpoint"""
            try:
                input_data = request.get("input", {})
                question = input_data.get("question", "")
                model = input_data.get("model", "qwen3:0.6b")  # Default model
                
                chat_input = ChatInput(question=question, model=model)
                result = await self.local_chat_endpoint(chat_input)
                
                return result
                
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        # Health check endpoint
        @self.app.get("/health")
        async def health_check():
            return {"status": "healthy"}

        # List available models endpoint
        @self.app.get("/models")
        async def list_models():
            return {
                "cloud_models": [
                    "qwen/qwen3-32b",
                    "llama3-70b-8192",
                    "compound-beta",
                    "gemma2-9b-it",
                    "mistral-saba-24b",
                    "qwen/qwen3-32b",
                    "whisper-large-v3-turbo"
                ],
                "local_models": [
                    "qwen3:0.6b",
                    "deepseek-r1:1.5b",
                ]
            }

    def run(self):
        uvicorn.run(self.app, host="localhost", port=8000)


if __name__ == "__main__":
    api = LangchainAPIApp()
    api.run()