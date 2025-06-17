# Obsidian to Perplexity Proxy

This project is a Python-based proxy server that relays requests from Obsidian to Perplexity, handling CORS issues. It is containerized with Docker and supports both local development and production deployment. Designed for local use and deployment via GitHub Actions.

## Features
- Proxies requests from Obsidian to Perplexity
- Handles CORS (Cross-Origin Resource Sharing)
- Dockerized for easy deployment
- Ready for CI/CD with GitHub Actions

## Getting Started

### Prerequisites
- Docker
- Python 3.9+

### Setup
1. Copy `.env` from the provided example or create your own `.env` in the project root:
   ```env
   PERPLEXITY_API_URL=https://api.perplexity.ai/chat/completions
   ALLOWED_ORIGINS=app://obsidian.md
   ```
2. Build and run the container (development):
   ```bash
   docker-compose -f docker-compose.dev.yml up --build
   ```
3. For production, use:
   ```bash
   docker-compose -f docker-compose.prod.yml up --build
   ```

### Running with GitHub Actions
- See `.github/workflows/` for CI/CD setup. Set environment variables in your workflow or provide a `.env` file as needed.

## License
MIT
