# Webring

> Because everything on the Web eventually loops back onto itself.

## Features

- View all entries in the ring
- Automatically provided JavaScript to embed a simple rendering of all entries
- Create, update, and delete entries
- Linkrot checking, with Web Archive fallback url for dead links (when possible)
- Optional linkrot event logging to [Discord](https://discord.com/) channel
  - Text error log fallback if disabled

### Auto-embed JavaScript

Starting with version 1.3.0, TODO: write me!

## Required Secrets

- Flask secret key (`SECRET_KEY`)
- Flask app environment (`FLASK_ENV`) set to `"production"`
- Absolute path to SQLite file (`DB_PATH`)
- JSON list of auth keys for all non-GET operations (`AUTH_KEYS`)
- Integer number of times supposed rotted links should be checked (`TIMES_FAILED_THRESHOLD`, default: 10)
- Discord linkrot event logging boolean (`ENABLE_DISCORD_LOGGING`, default: `False`)
  - Discord webhook URL (`DISCORD_WEBHOOK_URL`)

## Development

1. Install Python 3.10+, [Poetry](https://python-poetry.org/) 1.2.0+, and VS Code
1. Create required secret keys (default: `/app/secrets` or environment)
1. Run `poetry install`
1. Launch the API using the provided VS Code launch configuration
1. Auto-generated API docs are available at `/docs`
1. Run tests with `poetry run pytest` or through VS Code

## Build

1. `docker build -t webring:latest .`
1. `docker-compose up -d`

## License

2021-2024 Caleb

[MIT](LICENSE)
