from typing import Dict, Any
import logging
from .base import BaseHandler

logger = logging.getLogger(__name__)

class PerplexityHandler(BaseHandler):
    """Handler for Perplexity API requests"""
    
    def transform_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform request for Perplexity API (minimal transformation needed)"""
        return request_data
    
    def transform_response(self, response_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform Perplexity response (minimal transformation needed)"""
        return response_data
    
    def get_headers(self, original_headers: Dict[str, str]) -> Dict[str, str]:
        """Transform headers for Perplexity API"""
        headers = {"Content-Type": "application/json"}
        
        # Copy authorization header
        if "authorization" in original_headers:
            headers["Authorization"] = original_headers["authorization"]
        elif "Authorization" in original_headers:
            headers["Authorization"] = original_headers["Authorization"]
        else:
            logger.warning("🔧 PerplexityHandler: No authorization header found!")
        
        return headers
