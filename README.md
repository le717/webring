# WebRing

> Because.

## Required Secrets

- Flask secret key (`SECRET_KEY`)
- SQLite path (`DB_PATH`)
- Auth key for all non-GET operations (`AUTH_KEY`)

## Features

- View all entries in the ring
- Create, update, and delete entries
- Basic linkrot checking

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
