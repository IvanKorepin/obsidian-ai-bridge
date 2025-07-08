# Project Backlog & Recommendations

## 1. Project Structure
- Keep all source code in a dedicated package directory (e.g., `obsidian-ai-bridge/`).
- Place tests in a separate `tests/` directory.
- Use `requirements.txt` for dev/CI dependencies, and `setup.py` for package dependencies.

## 2. Devcontainer Improvements
- Add VS Code extensions for testing (e.g., `ms-python.pytest`), Jupyter, and pre-commit.
- Add linters/formatters: `flake8`, `black`, `isort`.
- Add `tasks.json` for running tests, linting, and building the package.
- Use `postCreateCommand` to install dev tools and pre-commit hooks.

## 3. VS Code Configuration
- Configure `.vscode/launch.json` for running and debugging CLI and tests.
- Configure `.vscode/tasks.json` for common dev tasks (test, lint, build).

## 4. Testing
- Use `pytest` and `pytest-cov` for tests and coverage.
- Add a test badge to `README.md`.

## 5. Documentation
- Maintain a clear `README.md` with usage, install, and publish instructions.
- Add `CONTRIBUTING.md` for contribution guidelines.

## 6. CI/CD
- Set up GitHub Actions for linting, testing, and building on PRs.
- Add workflow for PyPI publishing (with secrets for `PYPI_TOKEN`).

## 7. .gitignore
- Ensure all temp/build/venv files are ignored: `.env`, `.vscode/settings.json`, `dist/`, `build/`, `*.egg-info`, etc.

## 8. Pre-commit
- Set up `pre-commit` for auto-formatting and linting before commit.

## 9. Security
- Never commit secrets, tokens, or private keys.

## 10. PyPI Publishing
- Fill out all metadata in `setup.py` (description, author, license, url, classifiers).
- Use `MANIFEST.in` to include necessary files (e.g., `config.default.toml`).

## 11. GitHub Integration
- Add `github.vscode-pull-request-github` extension for PR/issues management in VS Code.
- Mount `.ssh` and `.gitconfig` for seamless git/GitHub access in devcontainer.

## 12. Linting
- Use linters (flake8, pylint) to keep code clean and consistent.

---

_This backlog is auto-generated from Copilot recommendations. Update as you implement features or improve the workflow._
