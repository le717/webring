# 1.3.0

_Released TDB_

- **Breaking change**: `FLASK_ENV=production` is a required environment variable due to Flask changes
  - This is automatically handled for you if using the included `docker-compose` file
- Update minimum Python version to 3.11
- Update to Flask v3
- ~~Update SQLAlchemy to v2~~ _update pending_
- Update all dependencies to their latest versions
- Switch to ruff for linting and formatting

# 1.2.0

_Released November 20, 2022_

- Switch to Docker image `python:3.10-slim`
- Update Poetry dependency process to v1.2.0+
- Update all dependencies to their latest versions
- Minor fixes to conform to third-party libraries updates


# 1.1.1

_Released  April 15, 2022_

- Update Python version to 3.10
- Update all dependencies to their latest versions

# 1.1.0

_Released October 28, 2021_

- Remove `rotted` property from a link
- Add new `is_dead` and `is_web_archive` properties to a link
- Update link title to indicate Web Archive/dead link on the fly, not in the database
- Update linkrot endpoint response to present updated information
- Add [`Flask-DB`](https://github.com/nickjj/flask-db) to handle database migrations
- Run database migrations automatically when needed
- Rename gunicorn logs to match traditional web server log names
- Remove duplicated error log

# 1.0.5

_Released August 31, 2021_

- Expand positive responses for dead link checking

# 1.0.4

_Released August 19, 2021_

- Remove currently viewed site from webring (#10)
- Provide default `TIMES_FAILED_THRESHOLD` value
- Add logging events when a link is added, updated, and removed

# 1.0.3

_Released August 17, 2021_

- Escape link info on update
- Rename gunicorn logs to not clobber other logs with the same name
- Do not update a link ID on link update

# 1.0.2

_Released August 16, 2021_

- Remove auto linkrot check on link add/update
- Fallback to text log for linkrot events if Discord logging is disabled (#8)
- Linkrot event messages are more informative
- Update dead link title to indicate Web Archive link when available
- Update link title to remove Web Archive link if revived (#9)
- Fix inconsistent linkrot status record cleanup
- Switch to Alpine Linux Python container

# 1.0.1

_Released August 13, 2021_

- Fix one-off error with `TIMES_FAILED_THRESHOLD`
- Fix linkrot record count not being deleted on status "yes"
- Add `pytest` based testing
