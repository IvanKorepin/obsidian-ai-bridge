from typing import Dict, Any
import logging
from .base import BaseHandler

logger = logging.getLogger(__name__)

class GeminiEmbeddingHandler(BaseHandler):
    """Handler for Gemini Embedding API requests"""
    
    def get_api_url(self, request_data: Dict[str, Any]) -> str:
        """Get the final API URL with model substitution"""
        # Extract model from request data
        model = "text-embedding-004"  # default model
        if "model" in request_data:
            model = request_data["model"]
            # Remove 'models/' prefix if present
            if model.startswith("models/"):
                model = model.replace("models/", "")
        
        # Build URL: https://generativelanguage.googleapis.com/v1/models/{model}:embedContent
        base_url = "https://generativelanguage.googleapis.com/v1/models"
        return f"{base_url}/{model}:embedContent"
    
    def transform_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform request for Gemini Embedding API"""
        # Extract model
        model = "text-embedding-004"
        if "model" in request_data:
            model = request_data["model"]
            
        # Extract text content
        text = ""
        if "input" in request_data:
            # Standard embedding input
            if isinstance(request_data["input"], str):
                text = request_data["input"]
            elif isinstance(request_data["input"], list) and len(request_data["input"]) > 0:
                text = str(request_data["input"][0])
        elif "content" in request_data:
            # Direct content
            if isinstance(request_data["content"], dict) and "parts" in request_data["content"]:
                # Already in Gemini format
                return request_data
            else:
                text = str(request_data["content"])
        elif "messages" in request_data:
            # Extract from messages
            text = " ".join([msg.get("content", "") for msg in request_data["messages"]])
        
        # Build Gemini format
        return {
            "model": f"models/{model}",
            "content": {
                "parts": [{"text": text}]
            }
        }
    
    def transform_response(self, response_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform Gemini response to OpenAI-style embedding format"""
        # Gemini returns: {"embedding": {"values": [0.1, 0.2, ...]}}
        # OpenAI expects: {"data": [{"embedding": [0.1, 0.2, ...], "index": 0}], "model": "...", "usage": {...}}
        
        if "embedding" in response_data and "values" in response_data["embedding"]:
            return {
                "object": "list",
                "data": [{
                    "object": "embedding",
                    "embedding": response_data["embedding"]["values"],
                    "index": 0
                }],
                "model": "text-embedding-004",
                "usage": {
                    "prompt_tokens": 0,
                    "total_tokens": 0
                }
            }
        
        # If response doesn't match expected format, return as-is
        return response_data
    
    def get_headers(self, original_headers: Dict[str, str]) -> Dict[str, str]:
        """Transform headers for Gemini API - no Authorization header needed"""
        # Gemini uses API key as query parameter, not in headers
        return {
            "Content-Type": "application/json"
        }
    
    async def process_request(self, request_data: Dict[str, Any], headers: Dict[str, str]) -> Dict[str, Any]:
        """Override to add API key as query parameter"""
        import httpx
        
        try:
            # Transform request
            transformed_request = self.transform_request(request_data)
            
            # Get headers (no auth header needed)
            api_headers = self.get_headers(headers)
            
            # Get the final URL
            final_url = self.get_api_url(request_data)
            
            # Extract API key from Authorization header
            api_key = None
            if "authorization" in headers:
                auth_header = headers["authorization"]
                if auth_header.startswith("Bearer "):
                    api_key = auth_header.replace("Bearer ", "")
            elif "Authorization" in headers:
                auth_header = headers["Authorization"]
                if auth_header.startswith("Bearer "):
                    api_key = auth_header.replace("Bearer ", "")
            
            if not api_key:
                raise ValueError("No API key found in Authorization header")
            
            # Add API key as query parameter
            final_url_with_key = f"{final_url}?key={api_key}"
            
            logger.info(f"🔧 {self.__class__.__name__}: Requesting {final_url}")
            logger.info(f"🔧 {self.__class__.__name__}: Full URL with key: {final_url_with_key[:80]}...{api_key[-4:]}")  # Log partial for security
            
            # Make request
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    final_url_with_key,
                    json=transformed_request,
                    headers=api_headers
                )
                response.raise_for_status()
                response_data = response.json()
            
            # Transform response
            return self.transform_response(response_data)
            
        except httpx.HTTPStatusError as e:
            logger.error(f"🔧 {self.__class__.__name__}: HTTP error {e.response.status_code}: {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"🔧 {self.__class__.__name__}: Request failed: {e}")
            raise
