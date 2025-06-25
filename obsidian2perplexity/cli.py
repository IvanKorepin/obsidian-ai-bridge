import sys
import os
import uvicorn
import click
from . import create_app, register_routes

def find_default_config():
    # 1. Try current working directory
    cwd_config = os.path.join(os.getcwd(), "config.default.toml")
    if os.path.exists(cwd_config):
        return cwd_config
    # 2. Try package default
    pkg_config = os.path.join(os.path.dirname(__file__), "config.default.toml")
    if os.path.exists(pkg_config):
        return pkg_config
    return None

@click.command()
@click.argument("config_path", required=False, default='')
@click.option('--host', default='127.0.0.1', help='Host to bind.')
@click.option('--port', default=8000, help='Port to run on.')
def main(host, port, config_path):
    """
    Simple proxy server for Obsidian AI chat plugin to Perplexity with optional config overrides.

    config_path: Path to config file. If not provided, will search for config.default.toml
    in current directory or package.
    """
    if not config_path:
        config_path = find_default_config()
        if not config_path:
            click.echo("No config.default.toml found. Please provide a config file.")
            sys.exit(1)
    app = create_app(config_path)
    register_routes(app)
    host = host if host else getattr(app.state, 'host', '127.0.0.1')
    port = port if port else getattr(app.state, 'port', 8000)
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
