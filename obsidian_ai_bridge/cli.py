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
@click.option('--host', default= None, help='Host to bind.')
@click.option('--port', default= None, type=int, help='Port to run on.')
@click.option('--ssl-cert', default=None, help='Path to SSL certificate file.')
@click.option('--ssl-key', default=None, help='Path to SSL key file.')
def main(host, port, config_path, ssl_cert, ssl_key):
    """
    Multi-service AI proxy server for Obsidian plugins with optional config overrides.
    
    Supports: Perplexity, Gemini Embedding
    
    CONFIG_PATH: Path to config file. If not provided, will search for config.default.toml
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
    ssl_cert = ssl_cert if ssl_cert else getattr(app.state, 'ssl_cert', None)
    ssl_key = ssl_key if ssl_key else getattr(app.state, 'ssl_key', None)
    
    click.echo(f"Starting multi-service AI proxy...")
    click.echo(f"Available endpoints:")
    click.echo(f"  - /perplexity/** (Perplexity chat completions)")
    click.echo(f"  - /gemini/embeddings (Gemini text embeddings)")
    click.echo(f"  - /health (health check)")
    
    if ssl_cert and ssl_key:
        click.echo(f"Running with SSL on {host}:{port}")
        uvicorn.run(app, host=host, port=int(port), ssl_certfile=ssl_cert, ssl_keyfile=ssl_key)
    else:
        click.echo(f"Running on {host}:{port} without SSL. This mode is recommended ONLY for localhost because your traffic is not protected.\n"
                   f"Please configure an external reverse proxy server, such as Nginx, for secure connections.")
        uvicorn.run(app, host=host, port=int(port))


if __name__ == "__main__":
    main()
