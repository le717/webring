# Webring

> Because everything on the Web eventually loops back onto itself.

## Features

- Create, update, view, and delete entries
- Automatically provided JavaScript to embed a simple rendering of all entries
- Linkrot checking, with Web Archive fallback url for dead links (when possible)
- Optional linkrot event logging to [Discord](https://discord.com/) channel

### Rotting links checking

Because websites can and will eventually vanish, even after
[a few months](https://brisray.com/web/linkrot.htm), link rot is a real
problem for webrings. As they are manually curated and maintained, knowing if an entry is
no longer available can be a maintenance burden. To that end, this webring has built-in rotten link
detection. However, it is not automatically set up and must be configured on your server.

The entire webring can be checked for rotten links by issuing an authenticated `POST` request to
the `/linkrot/` endpoint. Each entry that has not previously been determined to be dead will
be checked for a 200, 201, 204, or 304 HTTP response. If a URL fails that check, that failure
will be recorded. Once the check has failed more than the configured `TIMES_FAILED_THRESHOLD` limit,
the [Web Archive](https://web.archive.org/) will be checked for an archived version. If found,
the entry will be updated to use that link and the title will be adjusted to note such.
If there is no archived version, the entry will be recorded as dead and the title adjusted.

Individual entries, including dead entries, can also be checked.

One way to configure the linkrot check to run automatically is to create a Python script that
makes the aforementioned `POST` request and schedule it to automatically run via some scheduler.

Starting with version 1.4.1, a full history of linkrot checks are available for individual entries
by making an authenticated `GET` request to `/linkrot/<uuid>/history`.

### Filtering webring entries

Starting with version 1.3.0, new filtering options are available to restrict the provided webring
entries. These filters are supported on both the root URL and the simple embed endpoints. These
options are provided through query parameters to the URLs.

- `include_rotted: bool = "yes"`: Include entries that have been determined to be rotten
- `include_web_archive: bool = "yes"`: Include entries that can only be accessed through
  the Web Archive (added in version 1.4.0)
- `exclude_origin: bool = "yes"`: Remove the site requesting the webring from the entries,
if present

These values can also be set globally through the app configuration but will be overridden by
individual requests.

### Automatic simple embed

Starting with version 1.3.0, a JavaScript file is provided to generate and embed a simple rendering
of the webring into your site. It includes all entries in the script, preventing any additional
HTTP requests.

To use it, create an HTML element in your page with a CSS ID of `webring-embed-area`.
If the selector is found and there are entries to display, the webring will be injected
into that area of your site. A simple setup might look as follows:

```html
<!-- Create an area to display the webring -->
<section id="webring-embed-area">
  <noscript>
    The webring could not be loaded because your browser doesn't support JavaScript.
  </noscript>
</section>

<!-- Load the webring -->
<script defer src="https://example.com/webring-embed.js"></script>
```

As illustrated, a no-js fallback is recommended for visitors to your site that may have JavaScript
execution disabled or do not have JavaScript support.

Note that using the simple embed could potentially be slow and increase the page load time,
depending on the number of entries. This script is also not minified, which could also increase the
page load time. If greater control over loading and displaying the webring is desired, it is
suggested to manually call the root URL to fetch and display the entries, or put the webring on a
non-heavily trafficked page of your site.

### Discord channel logger

If the [Discord](https://discord.com) logger is enabled and configured, entries that are found to be
rotting or rotted will be reported in a Discord channel. This can be helpful for keeping up with
the webring's health and ensuring entries are available. Configuring the Discord logger
is kept as simple as possible.

1. Set the `ENABLE_DISCORD_LOGGING` secret value to `True` to enable the logger
1. Follow the Discord documentation for [creating a webhook](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks)
1. Get the Discord webhook URL from the configuration and set it as the value for
the `DISCORD_WEBHOOK_URL` secret key

A text file logger for events is always configured.

### Auth key creation/management

All administrative operations (effectively anything except fetching the webring entries) are
protected by an auth key which is intentionally kept extremely simple. Any string of characters
can be used as a key. All keys are defined as a JSON list called `AUTH_KEYS`. The key is to be
passed to the request via the `auth_key` query parameter. If the given key is in the defined list,
the operation succeeds. If it is not, a `422 UNPROCESSABLE ENTITY` HTTP error is raised.

## Required Secret/Configuration Keys

- Flask secret key (`SECRET_KEY`)
- Flask app environment (`FLASK_ENV`) set to `"production"`
- Absolute path to SQLite file (`DB_PATH`)
- JSON list of auth keys for all administrative operations (`AUTH_KEYS`)
- Integer number of times supposed rotted links should be checked (`TIMES_FAILED_THRESHOLD`, default: 10)
- Discord linkrot event logging boolean (`ENABLE_DISCORD_LOGGING`, default: `False`)
  - Discord webhook URL (`DISCORD_WEBHOOK_URL`)
- Webring entry filtering
  - `FILTER_INCLUDE_ROTTED`, default: `True`
  - `FILTER_INCLUDE_WEB_ARCHIVE`, default: `True`
  - `FILTER_EXCLUDE_ORIGIN`, default: `True`

## Development

1. Install Python 3.12+, [Poetry](https://python-poetry.org/) 1.8.0+, and VS Code
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
