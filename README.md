# Webring

> Because everything on the Web eventually loops back onto itself.

## Features

- View all entries in the ring
- Automatically provided JavaScript to embed a simple rendering of all entries
- Create, update, and delete entries
- Linkrot checking, with Web Archive fallback url for dead links (when possible)
- Optional linkrot event logging to [Discord](https://discord.com/) channel

### Rotting links checking

Because websites can and will eventually vanish, even after
[a few months](https://www.theregister.com/2024/05/20/webpages_vanish_decade/), linkrot is a real
problem for webrings. Because they are manually curated and maintained, knowing if an entry is
no longer available can be a maintenance burden. To that end, this webring has built-in rotten link
detection. However, it is not automatically set up and must be configured on your server.

The entire webring can be checked for rotten links by issuing an authenticated `POST` request to
the `/linkrot/` endpoint. Each entry that has not previously been determined to be dead will
be checked for a 200, 201, 204, or 304 HTTP response. If a URL fails that check, that failure
will be recorded. Once the check has failed more than the configured `TIMES_FAILED_THRESHOLD` limit,
the [Web Archive](http://web.archive.org/) site will be checked for an archived version. If found,
the entry will be updated to use that link and the entry title will be adjusted to note such.
If there is no archived version, the site will be recorded as dead and the entry title adjusted.

Individual entries, including dead entries, can also be checked.

One way to configure the linkrot check to run automatically is to create a Python script that
makes the aforementioned `POST` request and schedule it to automatically run via some scheduler.

### Filtering webring items

Starting with version 1.3.0, new filtering options are available to restrict the provided webring
items. These filters are supported on both the root URL and the simple embed endpoints. These
options are provided through query parameters to the URLs.

- `include_rotted: bool = "yes"`: Include links that have been determined to be rotten
- `exclude_origin: bool = "yes"`: Remove the site requested the webring from the results, if present

### Automatic simple embed

Starting with version 1.3.0, a JavaScript file is provided to generate and embed a simple rendering
of the webring into your site. It includes the entire ring in the script, preventing any additional
requests to fetch ring entries.

To use it, create an HTML element in your page with a CSS ID of `webring-embed-area`.
If the selector is found and there are webring items to display, the webring will be injected
into that area of your site. A simple setup might look as follows:

```html
<section id="webring-embed-area">
  <noscript>The webring could be loaded because your browser doesn't support running JavaScript.</noscript>
</section>

<!-- Load the webring -->
<script src="https://example.com/webring-embed.js"></script>
```

As illustrated, a no-js fallback is recommended for visitors to your site that may have JavaScript
execution disabled or lack JS support completely in their browser.

Note this could potentially be slow, depending on the number of entries in the ring. This script is
also not minified, which could also increase your page load time. If you want or need greater
control over loading and displaying the ring, it is suggested to manually call the ring's root URL
to fetch the entries and display them as you desire.

### Discord channel logger

If the [Discord](https://discord.com) logger is enabled and configured, links that are found to be
rotting or rotted will be reported in a Discord channel. This can be helpful for keeping up with
the webring's health and ensuring recorded sites are available. Configuring the Discord logger
is kept as simple as possible.

1. Set the `ENABLE_DISCORD_LOGGING` secret value to `True` to enable the logger
1. Follow the Discord documentation for [creating a webhook](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks)
1. Get the Discord webhook URL from the configuration and set it as the value for
the `DISCORD_WEBHOOK_URL` secret key

A text file logger for events is always configured.

## Required Secrets

- Flask secret key (`SECRET_KEY`)
- Flask app environment (`FLASK_ENV`) set to `"production"`
- Absolute path to SQLite file (`DB_PATH`)
- JSON list of auth keys for all non-GET operations (`AUTH_KEYS`)
- Integer number of times supposed rotted links should be checked (`TIMES_FAILED_THRESHOLD`, default: 10)
- Discord linkrot event logging boolean (`ENABLE_DISCORD_LOGGING`, default: `False`)
  - Discord webhook URL (`DISCORD_WEBHOOK_URL`)

## Development

1. Install Python 3.11+, [Poetry](https://python-poetry.org/) 1.6.0+, and VS Code
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
