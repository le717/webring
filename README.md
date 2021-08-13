# Arcana Webring

> Because everything on the Web eventually loops back onto itself.

## Features

- View all entries in the ring
- Create, update, and delete entries
- Linkrot checking, with Web Archive fallback url for dead links (when possible)
- Optional event logging to [Discord](https://discord.com/) channel

## Required Secrets

- Flask secret key (`SECRET_KEY`)
- SQLite path (`DB_PATH`)
- JSON list of auth keys for all non-GET operations (`AUTH_KEYS`)
- Integer number of times supposed rotted links should be checked (`TIMES_FAILED_THRESHOLD`)
- Discord event logging boolean (`ENABLE_DISCORD_LOGGING`)
  - Optional Discord webhook URL (`DISCORD_WEBHOOK_URL`)

## Development

1. Install Python 3.9+, [Poetry](https://poetry.eustace.io/) 1.1.0+, and VS Code
1. Create required secret keys
1. Run `poetry install`
1. Launch the API using the provided VS Code launch configuration
1. Auto-generated API docs are available at `/docs`

## Build

1. `docker build -t webring:latest .`
1. `docker-compose up -d`

## License

2021 Caleb Ely

[MIT](LICENSE)
