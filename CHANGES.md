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
