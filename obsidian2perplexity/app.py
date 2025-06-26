import os
import toml
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import httpx

def create_app(config_path=None):
    """
    Factory to create FastAPI app with config.
    """
    # Load config
    if config_path is None:
        config_path = os.getenv('CONFIG_PATH', 'config.default.toml')
    if os.path.exists(config_path):
        config = toml.load(config_path)
        routing_cfg = config.get('routing', {})
        allowed_origins = routing_cfg.get('ALLOWED_ORIGINS', ['*'])
        perplexity_api_url = routing_cfg.get('PERPLEXITY_API_URL', None)
        server_cfg = config.get('server', {})
        host = server_cfg.get('HOST', 'localhost')
        port = server_cfg.get('PORT', 8000)
        ssl_cert = server_cfg.get('SSL_CERTFILE', None)
        ssl_key = server_cfg.get('SSL_KEYFILE', None)
    else:
        allowed_origins = ['*']
        perplexity_api_url = None
        host = 'localhost'  
        port = 8000
        ssl_cert = None
        ssl_key = None
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    app.state.perplexity_api_url = perplexity_api_url
    app.state.host = host
    app.state.port = port
    app.state.ssl_cert = ssl_cert
    app.state.ssl_key = ssl_key

    return app

def register_routes(app: FastAPI):
    @app.api_route("{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
    async def proxy_request(path: str, request: Request):
        method = request.method
        headers = dict(request.headers)
        # Remove all CORS-related headers
        cors_headers = [
            "origin", "access-control-request-method", "access-control-request-headers",
            "access-control-allow-origin", "access-control-allow-credentials",
            "access-control-allow-methods", "access-control-allow-headers",
            "access-control-expose-headers", "access-control-max-age"
        ]
        clean_headers = {k: v for k, v in headers.items() if k.lower() not in cors_headers}
        body = await request.body()
        perplexity_url = app.state.perplexity_api_url
        if not perplexity_url:
            return Response(content="PERPLEXITY_API_URL is not set", status_code=500)
        url = perplexity_url  # Do not append path
        # Prepare only required headers for Perplexity request
        forward_headers = {}
        if "accept" in clean_headers:
            forward_headers["accept"] = clean_headers["accept"]
        if "authorization" in clean_headers:
            forward_headers["authorization"] = clean_headers["authorization"]
        forward_headers["content-type"] = "application/json"
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.request(
                    method=method,
                    url=perplexity_url,
                    headers=forward_headers,
                    content=body
                )
        except Exception as e:
            return Response(content=f"Error sending request to Perplexity: {e}", status_code=500)
        return Response(content=resp.content, status_code=resp.status_code, media_type=resp.headers.get('content-type', 'application/json'))
