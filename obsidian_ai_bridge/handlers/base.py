from abc import ABC, abstractmethod
from typing import Dict, Any
import httpx
import logging

logger = logging.getLogger(__name__)

class BaseHandler(ABC):
    """Base class for AI service handlers"""
    
    def __init__(self, api_url: str):
        self.api_url = api_url
    
    @abstractmethod
    def transform_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform incoming request to match target API format"""
        pass
    
    @abstractmethod
    def transform_response(self, response_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform target API response to expected format"""
        pass
    
    @abstractmethod
    def get_headers(self, original_headers: Dict[str, str]) -> Dict[str, str]:
        """Get headers for the target API request"""
        pass
    
    async def process_request(self, request_data: Dict[str, Any], headers: Dict[str, str]) -> Dict[str, Any]:
        """Process the complete request flow"""
        try:
            # Transform request
            transformed_request = self.transform_request(request_data)
            
            # Get headers
            api_headers = self.get_headers(headers)
            
            # Get the final URL
            final_url = self.get_api_url(request_data)
            
            logger.info(f"🔧 {self.__class__.__name__}: Requesting {final_url}")
            
            # Make request
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    final_url,
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
    
    def get_api_url(self, request_data: Dict[str, Any]) -> str:
        """Get the final API URL, with any necessary substitutions"""
        return self.api_url
