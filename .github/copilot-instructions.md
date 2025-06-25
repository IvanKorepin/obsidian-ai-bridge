p<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Project context
- Python-based proxy server for relaying requests from Obsidian to Perplexity.
- Handles CORS issues (Perplexity does not support CORS, but Obsidian requires it).
- Runs in a container (Docker), with dev and prod environments.
- Intended for local and GitHub Actions deployment.

# Coding guidelines
- Use FastAPI or Flask for the proxy server.
- Provide clear separation for dev/prod configs (e.g., via .env files).
- Ensure Dockerfile and docker-compose.yml support both environments.
- Add scripts for local and CI/CD (GitHub Actions) deployment.
