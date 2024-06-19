# 1.4.0

_Released June 19, 2024_

- Add ability to filter out Web Archive entries
  - Entries flagged as Web Archive only are included by default
  - Accessible on individual requests via `include_web_archive` query param
  - Globally controlled via `FILTER_INCLUDE_WEB_ARCHIVE` app configuration key
- Rewrite linkrot checking to create a full audit history of all checks
  - This simplifies the linkrot checking and creates full insight into the check
  - History may be exposed through an auth key protected endpoint in the future
- An off-by-one error was corrected during a linkrot check when comparing to
  `TIMES_FAILED_THRESHOLD`. An entry must now fail the linkrot check `TIMES_FAILED_THRESHOLD + 1`
  times to be considered and flagged as a dead link
- Include rotted entries when checking all entries for linkrot
- Exclude Web Archive entries when checking all entries for linkrot
- Improve linkrot check all efficiency by not looking up entries twice
- Revise database to use `AUTOINCREMENT PRIMARY KEY INT` for the `id` field
  - The previous UUID value has been moved to the `uuid` field
  - This change was made to support future planned features
  - **No request or response formats and structures have changed**
- Include timezone in linkrot log messages
- Include application version in comment in simple embed JavaScript
  - This will help consumers better determine what version of the webring is being run
    and what features are supported
- Add test to create and check for an entry only available via the Web Archive
- Add readme section to explain auth keys
- Ensure all `422 UNPROCESSABLE ENTITY` errors are auto-documented
- Ensure Web Archive links are always `https://`
- Dependency updates

# 1.3.1

_Released June 9, 2024_

- Add `FILTER_INCLUDE_ROTTED` and `FILTER_EXCLUDE_ORIGIN` app configuration keys
  - These allow changing the default filtering options for all requests
  - These values are overridden by individual requests
- Various fixes and alterations based on enabled ruff rules

# 1.3.0

_Released June 8, 2024_

- **Possible breaking change**: `FLASK_ENV=production` is a required environment variable due to
Flask changes
  - This is automatically handled for you if using the included `docker-compose` file
- Add new `/webring-embed.js` route to automatically generate and embed a simple webring listing
- Add ability to control showing rotted and same-origin results for root entrypoint and simple embed
- Add readme sections to explain new filtering and embed features
- Add readme section to explain setting up the Discord linkrot logger
- Add readme section to explain the linkrot check functionality
- Ensure the `date_added` field is expressed in UTC
- Fix error when linkrot checking with an ID that does not exist in the webring
- Always enable the linkrot text file logger
- Fix broken tests by better using `pytest`'s temporary testing data directory
- Replace `requests` with `python-httpx`
- Switch to [ruff](https://docs.astral.sh/ruff/) for linting and formatting
- Update `get-requirements.py` for Poetry changes
- Move new database creation into own script
- Update minimum Python version to 3.11
- Update Docker image to `python:3.11-slim`
- Update to Flask v3
- Update to SQLAlchemy v2 and API
- Update all dependencies to their latest versions
- Update OpenAPI spec version
- Various internal tweaks and adjustments

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
