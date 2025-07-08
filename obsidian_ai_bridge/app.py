import os
import toml
import logging
import traceback
import sys
from datetime import datetime
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any

from .handlers import PerplexityHandler, GeminiEmbeddingHandler

# Configure logging
import tempfile
log_file = os.getenv('OBSIDIAN_AI_BRIDGE_LOG', os.path.join(os.getcwd(), 'obsidian-ai-bridge.log'))

# Create log directory if it doesn't exist
log_dir = os.path.dirname(log_file)
if log_dir and not os.path.exists(log_dir):
    os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(log_file)
    ]
)
logger = logging.getLogger(__name__)

def create_app(config_path=None):
    """
    Factory to create FastAPI app with config.
    """
    try:
        logger.info("🚀 Starting Obsidian2AI Proxy application")
        
        app = FastAPI(title="Obsidian2AI Proxy", version="0.2.0")
        
        # Load config
        if config_path is None:
            config_path = os.getenv('CONFIG_PATH', 'config.default.toml')
        
        config = {}
        if os.path.exists(config_path):
            config = toml.load(config_path)
            routing_cfg = config.get('routing', {})
            allowed_origins = routing_cfg.get('ALLOWED_ORIGINS', ['*'])
            perplexity_api_url = routing_cfg.get('PERPLEXITY_API_URL', None)
            gemini_embedding_api_url = routing_cfg.get('GEMINI_EMBEDDING_API_URL', None)
            server_cfg = config.get('server', {})
            host = server_cfg.get('HOST', 'localhost')
            port = server_cfg.get('PORT', 8000)
            ssl_cert = server_cfg.get('SSL_CERTFILE', None)
            ssl_key = server_cfg.get('SSL_KEYFILE', None)
        else:
            logger.warning("Config file not found, using default values")
            allowed_origins = ['*']
            perplexity_api_url = "https://api.perplexity.ai/chat/completions"
            gemini_embedding_api_url = "https://generativelanguage.googleapis.com/v1/models/{model}:embedContent"
            host = 'localhost'
            port = 8000
            ssl_cert = None
            ssl_key = None

        # Initialize handlers
        handlers = {}
        if perplexity_api_url:
            handlers["perplexity"] = PerplexityHandler(perplexity_api_url)
            logger.info("✅ Perplexity handler created")
        if gemini_embedding_api_url:
            handlers["gemini_embedding"] = GeminiEmbeddingHandler(gemini_embedding_api_url)
            logger.info("✅ Gemini Embedding handler created")
        
        # Configure CORS
        if isinstance(allowed_origins, str):
            allowed_origins = [allowed_origins]
        
        app.add_middleware(
            CORSMiddleware,
            allow_origins=allowed_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"]
        )
        
        # Store in app state
        app.state.handlers = handlers
        app.state.host = host
        app.state.port = port
        app.state.ssl_cert = ssl_cert
        app.state.ssl_key = ssl_key

        logger.info("✅ Application created successfully")
        return app
        
    except Exception as e:
        logger.error(f"💥 CRITICAL ERROR during app creation: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise

def register_routes(app: FastAPI):
    @app.api_route("/perplexity{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
    async def proxy_perplexity(path: str, request: Request):
        """Proxy all requests starting with /perplexity to Perplexity API"""
        try:
            if "perplexity" not in app.state.handlers:
                raise HTTPException(status_code=500, detail="Perplexity handler not configured")
            
            handler = app.state.handlers["perplexity"]
            
            # Get request data and headers
            try:
                if request.method in ["POST", "PUT", "PATCH"]:
                    request_data = await request.json()
                else:
                    request_data = {}
            except Exception:
                request_data = {}
            
            headers = dict(request.headers)
            
            # Process request
            response = await handler.process_request(request_data, headers)
            return response
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"❌ Perplexity request failed: {e}")
            raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")
    
    @app.post("/gemini/embeddings/")
    @app.post("/gemini/embeddings")
    async def proxy_gemini_embedding(request: Request):
        """Proxy requests to Gemini Embedding API"""
        try:
            if "gemini_embedding" not in app.state.handlers:
                raise HTTPException(status_code=500, detail="Gemini Embedding handler not configured")
            
            handler = app.state.handlers["gemini_embedding"]
            
            # Get request data and headers
            try:
                request_data = await request.json()
            except Exception:
                request_data = {}
            
            headers = dict(request.headers)
            
            # Process request
            response = await handler.process_request(request_data, headers)
            return response
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"❌ Gemini Embedding request failed: {e}")
            raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")
    
    @app.get("/health")
    async def health_check():
        """Health check endpoint"""
        return {
            "status": "healthy",
            "services": list(app.state.handlers.keys()),
            "version": "0.2.0",
            "timestamp": datetime.now().isoformat()
        }
