import os
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import datetime
import httpx

# Load environment variables
if os.path.exists('.env'):
    load_dotenv('.env', override=True)

ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', '*').split(',')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.api_route("/proxy/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
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
    # Get base Perplexity API URL
    perplexity_url = os.getenv('PERPLEXITY_API_URL')
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

    # Send actual request to Perplexity via httpx
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

    # Return Perplexity response to the client (as JSON)
    return Response(content=resp.content, status_code=resp.status_code, media_type=resp.headers.get('content-type', 'application/json'))
